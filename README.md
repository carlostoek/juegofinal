# juegofinal

## Project Overview

juegofinal is a small Telegram bot built with [aiogram](https://docs.aiogram.dev/) 3.0. It showcases simple command handlers and how to persist user data with SQLite. The bot supports registering users via the `/start` command and displaying profile details with `/profile`.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd juegofinal
   ```
2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your bot token**
   Create a `.env` file or export the `BOT_TOKEN` environment variable with the token provided by [BotFather](https://t.me/BotFather):
   ```bash
   echo "BOT_TOKEN=your-telegram-bot-token" > .env
   ```
5. **Run the bot**
   ```bash
   python main.py
   ```

## Features

- `/start` command that stores basic user information in SQLite and sends a welcome message with an inline menu.
- `/profile` command that replies with the user's level, points and join date.
- `PointService` utility for managing registration and daily bonus points.
- Basic echo handler for all other messages.
- Configuration via `pydantic-settings` and a local `.env` file.

## Development Instructions

- Make sure all Python files compile:
  ```bash
  python -m py_compile $(git ls-files '*.py')
  ```
- Run the bot locally using `python main.py` while developing new handlers or services.
- Contributions are welcome via pull requests.

## Notes

- `PointService` guarda los puntos de los usuarios en memoria, por lo que se pierden al reiniciar el bot.

