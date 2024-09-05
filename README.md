# Instagram Followers and Following Bot

This bot interacts with Instagram followers and following lists using the Telegram Bot API. It allows users to upload their followers and following lists in HTML format, check their lists, and perform various operations on the data.

## Features

- **Send Followers**: Upload an HTML file containing Instagram followers. If the list isn't empty, you'll see who unfollowed you and who started following you since the last update.
- **Send Following**: Upload an HTML file containing Instagram accounts you are following. If the list isn't empty, you'll see who you unfollowed and who you started following since the last update.
- **Check Followers**: View the list of followers with a count.
- **Check Following**: View the list of following accounts with a count.
- **Empty Followers**: Clear the list of followers.
- **Empty Following**: Clear the list of following accounts.
- **Not Following Back**: Find accounts you are following but who are not following you back.

## Requirements

Ensure you have Python 3.8 or later installed. Install the required libraries using `pip`:

pip install -r requirements.txt

## Configuration

1. Edit the `settings.json` file in the project directory with the following format:
    `
    {
        "api_key": "YOUR_API_KEY"
    }
    `
   Replace `"YOUR_API_KEY"` with your Telegram Bot API token.

2. Initialize the SQLite database by running the bot script once. This will create the `user_data.db` file with the necessary tables.

## Usage

1. **Start the Bot**: Run the bot script.

    python bot.py

2. **Interact with the Bot**:
    - **/start**: Welcome message and usage instructions.
    - **/send_followers**: Prepare to upload your followers list.
    - **/send_following**: Prepare to upload your following list.
    - **/check_followers**: Get the list of your followers with a count.
    - **/check_following**: Get the list of accounts you are following with a count.
    - **/empty_followers**: Clear your followers list.
    - **/empty_following**: Clear your following list.
    - **/not_following_back**: Find accounts you follow but who don’t follow you back.

## Notes

- The bot requires HTML files to be formatted correctly. Ensure the HTML contains the Instagram profile links for accurate extraction.
- Large lists might result in the bot sending files instead of text messages due to Telegram's message length limit.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. [TODO]
