import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MANAGER = "aikhang"
CATALOG = {
    "iphone": {"name": "iPhone", "items": [
        {"name": "iPhone 15 Pro Max 256GB", "price": "119 990 р"},
        {"name": "iPhone 15 128GB", "price": "79 990 р"},
    ]},
    "macbook": {"name": "MacBook", "items": [
        {"name": "MacBook Air M2 8/256GB", "price": "109 990 р"},
    ]},
    "airpods": {"name": "AirPods", "items": [
        {"name": "AirPods Pro 2", "price": "24 990 р"},
    ]},
}
logging.basicConfig(level=logging.INFO)
async def start(update, context):
    kb = [[InlineKeyboardButton("Каталог", callback_data="catalog")],[InlineKeyboardButton("Менеджер", url=f"https://t.me/{MANAGER}")],[InlineKeyboardButton("О нас", callback_data="about")]]
    text = "Добро пожаловать в Plata! Техника Apple по лучшим ценам"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
async def catalog_h(update, context):
    q = update.callback_query
    await q.answer()
    kb = [[InlineKeyboardButton(c["name"], callback_data=f"cat_{k}")] for k, c in CATALOG.items()]
    kb.append([InlineKeyboardButton("Назад", callback_data="home")])
    await q.edit_message_text("Каталог", reply_markup=InlineKeyboardMarkup(kb))
async def category_h(update, context):
    q = update.callback_query
    await q.answer()
    cat = CATALOG.get(q.data.replace("cat_", ""))
    lines = [cat["name"]] + [f"{i['name']} - {i['price']}" for i in cat["items"]]
    kb = [[InlineKeyboardButton("Заказать", url=f"https://t.me/{MANAGER}")],[InlineKeyboardButton("Назад", callback_data="catalog")]]
    await q.edit_message_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(kb))
async def about_h(update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("Plata - оригинальная техника Apple. Доставка по России. Рассрочка.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="home")]]))
async def router(update, context):
    d = update.callback_query.data
    if d == "home": await start(update, context)
    elif d == "catalog": await catalog_h(update, context)
    elif d.startswith("cat_"): await category_h(update, context)
    elif d == "about": await about_h(update, context)
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
print("Bot started!")
app.run_polling()
