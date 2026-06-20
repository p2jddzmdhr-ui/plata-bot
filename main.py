mport os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MANAGER = "aikhang"

CATALOG = {
    "iphone": {"name": "📱 iPhone", "items": [
        {"name": "iPhone 15 Pro Max 256GB", "price": "119 990 ₽"},
        {"name": "iPhone 15 128GB", "price": "79 990 ₽"},
    ]},
    "macbook": {"name": "💻 MacBook", "items": [
        {"name": "MacBook Air M2 8/256GB", "price": "109 990 ₽"},
    ]},
    "airpods": {"name": "🎧 AirPods", "items": [
        {"name": "AirPods Pro 2", "price": "24 990 ₽"},
    ]},
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("💬 Менеджер", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ]
    text = "👋 Добро пожаловать в <b>Plata</b>!\n\n🍎 Техника Apple по лучшим ценам"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def catalog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(c["name"], callback_data=f"cat_{k}")] for k, c in CATALOG.items()]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="home")])
    await query.edit_message_text("📦 <b>Каталог</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = CATALOG.get(query.data.replace("cat_", ""))
    lines = [f"<b>{cat['name']}</b>\n"] + [f"• {i['name']} — <b>{i['price']}</b>" for i in cat["items"]]
    keyboard = [[InlineKeyboardButton("💬 Заказать", url=f"https://t.me/{MANAGER}")], [InlineKeyboardButton("🔙 Назад", callback_data="catalog")]]
    await query.edit_message_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "ℹ️ <b>Plata</b>\n\n✅ Оригинальная техника Apple\n🚚 Доставка по России\n💳 Рассрочка"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="home")]]), parse_mode="HTML")

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "home": await start(update, context)
    elif data == "catalog": await catalog_handler(update, context)
    elif data.startswith("cat_"): await category_handler(update, context)
    elif data == "about": await about_handler(update, context)

if name == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(router))
    print("✅ Бот Plata запущен!")
    app.run_polling()
