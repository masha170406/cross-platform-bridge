import telebot 
import requests 
import threading
import discord
from discord.ext import commands 
import logging 
from dotenv import load_dotenv
import os
import io

load_dotenv()
ds_token = os.getenv('DISCORD_TOKEN')
tg_api_key= os.getenv('API_KEY')
tg_chat_id= os.getenv('CHAT_ID')
ds_webhook = os.getenv('WEBHOOK')

tg_bot = telebot.TeleBot(tg_api_key)

def run_telegram():
    
    tg_bot.send_message(tg_chat_id, "HI")

    @tg_bot.message_handler(commands=['start'])
    def start(message):
        tg_bot.reply_to(message, "I am listening.")

    @tg_bot.message_handler(func=lambda message: True)
    
    def send_to_discord(message):
        payload = {
            "username": f"{message.from_user.first_name}",
            "content": message.text
        }
        requests.post(ds_webhook, json=payload)

    @tg_bot.message_handler(content_types=['photo', 'document', 'video', 'video_note', 'sticker', 'animation'])
    def handle_telegram_media(message):
        if message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            file_name = "image.jpg"
        else:
            file_id = getattr(message, message.content_type).file_id
            file_name = getattr(message, message.content_type).file_name

        file_info = tg_bot.get_file(file_id)
        downloaded_file =tg_bot.download_file(file_info.file_path)

        files = {
            "file": (file_name, downloaded_file)
        }
        payload = {
            "content": f"**{message.from_user.first_name}** sent a file:",
            "username": f"{message.from_user.first_name} (TG)"
        }
        
        requests.post(ds_webhook, data=payload, files=files)

    tg_bot.infinity_polling()

def run_discord():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Ds bot here and ready")
    
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return 
    
        if message.author == bot.user:
            return
        
        if message.attachments:
            for attachment in message.attachments:
                attachment = message.attachments[0]
                response = requests.get(attachment.url)
                
                if response.status_code == 200:
                    file_data = io.BytesIO(response.content)
                    file_data.name = attachment.filename  
                    
                    try:
                        tg_bot.send_document(tg_chat_id, file_data)
                        print("Successfully sent to Telegram!")
                    except Exception as e:
                        print(f"Telegram Error: {e}")


        sender_name = message.author.display_name
        content = message.content

        formatted_text = f"👤 **{sender_name}**\n\n{content}"

        tg_bot.send_message(tg_chat_id, formatted_text, parse_mode='Markdown')

        await bot.process_commands(message)



    bot.run(ds_token, log_handler=handler, log_level=logging.DEBUG)



t1 = threading.Thread(target=run_telegram)
t1.start()

run_discord()