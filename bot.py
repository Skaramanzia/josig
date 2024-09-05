from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, send_followers, send_following, handle_document, quit_process, check_followers, check_following, empty_followers, empty_following, not_following_back
from utils import load_settings
from database import init_db

def main():
    settings = load_settings()
    init_db()  # Initialize the database

    application = Application.builder().token(settings['api_key']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_followers", send_followers))
    application.add_handler(CommandHandler("send_following", send_following))
    application.add_handler(CommandHandler("quit_process", quit_process))
    application.add_handler(CommandHandler("check_followers", check_followers))
    application.add_handler(CommandHandler("check_following", check_following))
    application.add_handler(CommandHandler("empty_followers", empty_followers))
    application.add_handler(CommandHandler("empty_following", empty_following))
    application.add_handler(CommandHandler("not_following_back", not_following_back))

    # Handle documents
    application.add_handler(MessageHandler(filters.Document.MimeType("text/html"), handle_document))

    print("Bot started successfully")
    application.run_polling()

if __name__ == "__main__":
    main()
