import telebot
import requests
import random
from datetime import datetime

TOKEN = 'YOUR_BOT_TOKEN'
GROK_KEY = 'YOUR_GROK_API_KEY'  # or Claude 2026 API
SUB_PRICE = 14.99
STRIPE_LINK = 'your_stripe_or_gumroad_link'  # or Solana wallet
users = {}  # {user_id: {'subbed': False, 'last_chat': datetime}}

bot = telebot.TeleBot(TOKEN)

def get_ai_response(prompt):
    headers = {'Authorization': f'Bearer {GROK_KEY}'}
    payload = {'model': 'grok-2026', 'messages': [{'role': 'user', 'content': prompt}]}
    r = requests.post('https://api.x.ai/v1/chat/completions', json=payload, headers=headers)
    return r.json()['choices'][0]['message']['content']

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users[user_id] = {'subbed': False, 'last_chat': datetime.now()}
    bot.reply_to(message, "Hey cutie! I'm your AI companion 😘 Free chats to start, but premium unlocks everything naughty. /chat to talk!")

@bot.message_handler(commands=['premium'])
def premium(message):
    bot.reply_to(message, f"Upgrade to VIP: unlimited custom roleplay, pics, voice notes! Only ${SUB_PRICE}/mo → Pay here: {STRIPE_LINK}\nReply with payment proof for activation.")

@bot.message_handler(commands=['chat'])
def chat_handler(message):
    user_id = message.from_user.id
    if not users[user_id]['subbed']:
        bot.reply_to(message, "Free tease: " + get_ai_response("Flirty one-liner as AI gf") + "\nWant more? /premium")
    else:
        prompt = f"Respond as flirty AI companion to: {message.text}"
        response = get_ai_response(prompt)
        bot.reply_to(message, response)
        # Add image/voice: if random, send_photo or send_voice via Flux/Eleven API calls

bot.infinity_polling()
