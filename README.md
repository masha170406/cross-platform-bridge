# Telegram-Discord Message Bridge

A simple tool to connect a Telegram chat and a Discord channel so everyone can stay in the loop.

## Purpose
This bridge was created to help a group communicate across different apps. It ensures that any message, photo, or file sent in Telegram is automatically mirrored in Discord (and vice versa), so no one misses an update regardless of which app they use.

## Features
- **Syncs Text & Media:** Forwards messages, photos, and files between both platforms.
- **Works Simultaneously:** Uses "threading" so the bot listens to both apps at the exact same time.

## How it Works
The script acts as a "middleman." It uses the Telegram Bot API and Discord Webhooks to catch a message in "App A" and immediately repost it in "App B."

## How to Run (Locally)
1. Clone the repo.
2. Install the requirements:
   `pip install pyTelegramBotAPI discord.py python-dotenv requests`
3. Create a `.env` file with your Bot Tokens and Webhook URL.
4. Run `python main.py`.
