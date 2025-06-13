# juegofinal

## Overview

juegofinal is a small Telegram bot built with [aiogram](https://docs.aiogram.dev/) 3.0. It shows how to implement basic command handlers, persist user data in SQLite and log updates. The bot lets users register with `/start` and check their stats with `/profile`, `/level` and `/badges`.

## Setup instructions

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
   Copy `.env.example` to `.env` and put the token given by [BotFather](https://t.me/BotFather):
   ```bash
   cp .env.example .env
   # edit .env and set BOT_TOKEN
   ```

## How to run the bot

Run the main module:
```bash
python main.py
```

## Features

- `/start` registers the user in SQLite and displays an inline menu.
- `/profile` shows a user's level, points and join date.
- `/level` reports the current level and points.
- `/badges` lists earned badges.
- `/ranking` shows the top users by points.
- `/help` explains available commands.
- Basic echo handler for any other message.
- `PointService` for registration and daily bonus points.
- Logging middleware writes errors to `logs/errors.log`.

## Folder structure

```
├── bot.py            # Bot and dispatcher initialization
├── config.py         # pydantic settings loader
├── database/         # SQLAlchemy models and database setup
├── handlers/         # Command handlers grouped by feature
├── logs/             # Log files
├── services/         # Business logic such as PointService
├── utils/            # Middleware and helper utilities
├── main.py           # Entry point that starts polling
├── requirements.txt  # Python dependencies
└── .env.example      # Sample environment configuration
```

