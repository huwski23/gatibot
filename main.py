import discord
from discord.ext import commands
import os
import requests
import json

# Grok API ayarları
GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_URL = "https://api.x.ai/v1/chat/completions"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} AI modunda online la! Her mesajı okuyup cevap verecek.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": "Sen eğlenceli, küfürlü bir Türk la adamısın. Kısa ve samimi cevap ver, sohbeti devam ettir."},
                {"role": "user", "content": message.content}
            ],
            "max_tokens": 150,
            "temperature": 0.8
        }
        response = requests.post(GROK_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            ai_reply = result['choices'][0]['message']['content']
            await message.channel.send(f"{message.author.mention} {ai_reply}")
        else:
            print(f"Hata: {response.status_code}")
    except Exception as e:
        print(f"AI hatası: {e}")

bot.run(os.getenv('MTQ0MjA1MDYwNDMwMTE1NjM3Mg.GX3r2q.iiLvPRERVNe8pj_BytFYbgYkhM9PO0VnDqwuTw'))
