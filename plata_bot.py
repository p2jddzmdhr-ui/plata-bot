import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8610839804:AAE4zbJHJYvghtjJvvEkqC183zZeWLqFtY"
MANAGER_USERNAME = "@aikhang"

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

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("💬 Менеджер", url=f"https://t.me/{MANAGER_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ]
    text = "👋 Добро пожаловать в <b>Plata</b>!\n\n🍎 Техника Apple по лучшим ценам\n\nВыберите раздел:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def catalog(update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(c["name"], callback_data=f"cat_{k}")] for k, c in CATALOG.items()]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="home")])
    await query.edit_message_text("📦 <b>Каталог</b>\n\nВыберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def category(update, context):
    query = update.callback_query
    await query.answer()
    cat = CATALOG.get(query.data.replace("cat_", ""))
    lines = [f"<b>{cat['name']}</b>\n"] + [f"• {i['name']} — <b>{i['price']}</b>" for i in cat["items"]]
    lines.append(f"\n💬 Для заказа: {MANAGER_USERNAME}")
    keyboard = [[InlineKeyboardButton("💬 Заказать", url=f"https://t.me/{MANAGER_USERNAME.lstrip('@')}")], [InlineKeyboardButton("🔙 Назад", callback_data="catalog")]]
    await query.edit_message_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def about(update, context):
    query = update.callback_query
    await query.answer()
    text = "ℹ️ <b>Plata</b>\n\n✅ Оригинальная техника Apple\n🚚 Доставка по России\n💳 Рассрочка\n🔧 Гарантия"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="home")]]), parse_mode="HTML")

async def router(update, context):
    data = update.callback_query.data
    if data == "home": await start(update, context)
    elif data == "catalog": await catalog(update, context)
    elif data.startswith("cat_"): await category(update, context)
    elif data == "about": await about(update, context)

logging.basicConfig(level=logging.INFO)
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
print("✅ Бот Plata запущен!")
app.run_polling()
