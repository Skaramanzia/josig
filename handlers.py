import os
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from utils import extract_usernames_from_html
from database import get_user_data, update_user_data, clear_user_data

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /send_followers or /send_following to upload an HTML file.")

async def send_followers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_states[user_id] = "waiting_for_followers"
    await update.message.reply_text("Please send the HTML file with your followers.")

async def send_following(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_states[user_id] = "waiting_for_following"
    await update.message.reply_text("Please send the HTML file with the accounts you are following.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = user_states.get(user_id)

    if state == "waiting_for_followers" or state == "waiting_for_following":
        document = update.message.document

        if document.mime_type == "text/html":
            file = await document.get_file()
            file_content = await file.download_as_bytearray()

            try:
                if isinstance(file_content, bytearray):
                    file_content = file_content.decode('utf-8')

                print(f"Received file content (first 100 bytes): {file_content[:100]}")
                usernames = extract_usernames_from_html(file_content)
            except ValueError as e:
                await update.message.reply_text(f"Error: {e}")
                return
            except Exception as e:
                await update.message.reply_text(f"An unexpected error occurred: {e}")
                return

            # Fetch old data
            old_data = get_user_data(user_id)

            # Update the relevant list
            if state == "waiting_for_followers":
                new_followers = usernames
                update_user_data(user_id, new_followers, old_data['following'])  # Aggiorna solo i followers
                await update.message.reply_text("Followers list updated.")

                # Calculate differences
                old_followers_set = set(old_data['followers'])
                new_followers_set = set(new_followers)

                added_followers = new_followers_set - old_followers_set
                removed_followers = old_followers_set - new_followers_set

                added_message = "\n".join(added_followers) if added_followers else "None"
                removed_message = "\n".join(removed_followers) if removed_followers else "None"
                response = (
                    f"New followers:\n{added_message}\n\n"
                    f"Lost followers:\n{removed_message}"
                )

            elif state == "waiting_for_following":
                new_following = usernames
                update_user_data(user_id, old_data['followers'], new_following)  # Aggiorna solo i following
                await update.message.reply_text("Following list updated.")

                # Calculate differences
                old_following_set = set(old_data['following'])
                new_following_set = set(new_following)

                added_following = new_following_set - old_following_set
                removed_following = old_following_set - new_following_set

                added_message = "\n".join(added_following) if added_following else "None"
                removed_message = "\n".join(removed_following) if removed_following else "None"
                response = (
                    f"New users followed:\n{added_message}\n\n"
                    f"Users unfollowed:\n{removed_message}"
                )

            # Check if response is too long and send it accordingly
            if len(response) > 4000:  # Telegram message limit is 4096 characters
                with open('update_list.txt', 'w') as file:
                    file.write(response)
                with open('update_list.txt', 'rb') as file:
                    await update.message.reply_document(document=InputFile(file, 'update_list.txt'))
                os.remove('update_list.txt')
            else:
                await update.message.reply_text(response)

            # Reset user state
            user_states[user_id] = None
        else:
            await update.message.reply_text("Error: The file must be an HTML file.")
    else:
        await update.message.reply_text("Error: Please use /send_followers or /send_following before sending a file.")

async def quit_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_states.get(user_id) in ["waiting_for_followers", "waiting_for_following"]:
        user_states[user_id] = None
        await update.message.reply_text("Process has been stopped. You can start again with /send_followers or /send_following.")
    else:
        await update.message.reply_text("You are not in the middle of any process.")

async def check_followers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = get_user_data(user_id)
    followers = data.get('followers', [])
    total_followers = len(followers)  # Counting followers

    if followers:
        followers_list = "\n".join(followers)
        message = f"Your followers ({total_followers}):\n{followers_list}\n\nTotal followers: {total_followers}"
        if len(followers_list) > 4000:  # Telegram message limit is 4096 characters
            with open('followers_list.txt', 'w') as file:
                file.write(message)
            with open('followers_list.txt', 'rb') as file:
                await update.message.reply_document(document=InputFile(file, 'followers_list.txt'))
            os.remove('followers_list.txt')
        else:
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("Your followers list is empty. Use /send_followers to upload your followers.")

async def check_following(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = get_user_data(user_id)
    following = data.get('following', [])
    total_following = len(following)  # Counting followings

    if following:
        following_list = "\n".join(following)
        message = f"Accounts you are following ({total_following}):\n{following_list}\n\nTotal following: {total_following}"
        if len(following_list) > 4000:  # Telegram message limit is 4096 characters
            with open('following_list.txt', 'w') as file:
                file.write(message)
            with open('following_list.txt', 'rb') as file:
                await update.message.reply_document(document=InputFile(file, 'following_list.txt'))
            os.remove('following_list.txt')
        else:
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("Your following list is empty. Use /send_following to upload the accounts you are following.")


async def empty_followers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    clear_user_data(user_id)
    await update.message.reply_text("Your followers list has been emptied.")

async def empty_following(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    clear_user_data(user_id)
    await update.message.reply_text("Your following list has been emptied.")

async def not_following_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = get_user_data(user_id)
    followers = set(data.get('followers', []))
    following = set(data.get('following', []))

    not_following_back = following - followers

    if not_following_back:
        not_following_back_list = "\n".join(not_following_back)
        if len(not_following_back_list) > 4000:  # Telegram message limit is 4096 characters
            with open('not_following_back_list.txt', 'w') as file:
                file.write(not_following_back_list)
            with open('not_following_back_list.txt', 'rb') as file:
                await update.message.reply_document(document=InputFile(file, 'not_following_back_list.txt'))
            os.remove('not_following_back_list.txt')
        else:
            await update.message.reply_text(f"Accounts you are following but not following you back:\n{not_following_back_list}")
    else:
        await update.message.reply_text("All accounts you are following are also following you back.")
