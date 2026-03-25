from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import json
import os

cards = [
    {"name": "Naruto", "rarity": "SSR"},
    {"name": "Luffy", "rarity": "SSR"},
    {"name": "Goku", "rarity": "SSR"},
    {"name": "Levi", "rarity": "SR"},
    {"name": "Gojo", "rarity": "SR"},
    {"name": "Tanjiro", "rarity": "R"}
]

DATA_FILE = "users.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎴 Anime Card Bot\nUse /draw")

async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = []

    card = random.choice(cards)
    data[user_id].append(card)

    save_data(data)

    await update.message.reply_text(
        f"🎉 You got: {card['name']} ({card['rarity']})"
    )

async def mycards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    data = load_data()

    if user_id not in data or len(data[user_id]) == 0:
        await update.message.reply_text("No cards yet 😢")
        return

    text = "🃏 Your Cards:\n"
    for card in data[user_id]:
        text += f"- {card['name']} ({card['rarity']})\n"

    await update.message.reply_text(text)

TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("draw", draw))
app.add_handler(CommandHandler("mycards", mycards))

app.run_polling()
