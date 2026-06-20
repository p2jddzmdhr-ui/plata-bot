import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MANAGER = "aikhang"

MARKUP = 0.10

CATALOG = {
    "iphone": {"name": "🍎 iPhone", "items": [
        {"name": "iPhone 13 128GB ⚫️", "price": 33000},
        {"name": "iPhone 13 512GB ⚪️", "price": 42000},
        {"name": "iPhone 14 128GB 🔴🟡", "price": 38000},
        {"name": "iPhone 14 128GB 🔵", "price": 41000},
        {"name": "iPhone 14 512GB ⚫️⚪️", "price": 46000},
        {"name": "iPhone 14 Plus 128GB 🟡", "price": 43000},
        {"name": "iPhone 15 128GB 🔵", "price": 46500},
        {"name": "iPhone 15 128GB ⚫️", "price": 47000},
        {"name": "iPhone 15 256GB ⚫️", "price": 53500},
        {"name": "iPhone 15 Plus 128GB 🟡", "price": 48000},
        {"name": "iPhone 15 Plus 128GB 🔵", "price": 48500},
        {"name": "iPhone 15 Pro 128GB 🔵", "price": 66500},
        {"name": "iPhone 15 Pro Max 1TB ⚫️⚙️🔵", "price": 96000},
        {"name": "iPhone 16e 256GB ⚪️", "price": 42000},
        {"name": "iPhone 16 128GB 🔵🟢", "price": 49500},
        {"name": "iPhone 16 128GB 💖⚪️", "price": 50000},
        {"name": "iPhone 16 256GB 💖", "price": 58500},
        {"name": "iPhone 16 Plus 128GB ⚫️⚪️🔵💖🟢", "price": 58000},
        {"name": "iPhone 16 Plus 256GB 💖", "price": 65000},
        {"name": "iPhone 16 Pro 128GB ⚪️", "price": 70500},
        {"name": "iPhone 16 Pro 128GB 🟠⚙️", "price": 74000},
        {"name": "iPhone 16 Pro 128GB ⚫️", "price": 75000},
        {"name": "iPhone 16 Pro 1TB ⚪️", "price": 104500},
        {"name": "iPhone 16 Pro Max 256GB 🟠", "price": 85000},
        {"name": "iPhone 16 Pro Max 512GB ⚫️", "price": 97000},
        {"name": "iPhone 16 Pro Max 512GB 🟠", "price": 101500},
        {"name": "iPhone 16 Pro Max 1TB 🟠", "price": 114000},
        {"name": "iPhone 17e 256GB 💖⚪️", "price": 44000},
        {"name": "iPhone 17e 256GB ⚪️", "price": 51000},
        {"name": "iPhone 17e 512GB ⚫️⚪️", "price": 57000},
        {"name": "iPhone 17e 512GB 💖", "price": 62000},
        {"name": "iPhone 17 256GB ⚫️🟣🔵⚪️🟢", "price": 61000},
        {"name": "iPhone 17 256GB EU ⚫️🔵⚪️🟢🟣", "price": 64500},
        {"name": "iPhone 17 512GB ⚫️", "price": 75500},
        {"name": "iPhone 17 Air 256GB 🔵", "price": 66500},
        {"name": "iPhone 17 Air 256GB ⚫️🟡⚪️", "price": 67500},
        {"name": "iPhone 17 Air 512GB 🔵", "price": 71000},
        {"name": "iPhone 17 Air 512GB 🟡", "price": 71500},
        {"name": "iPhone 17 Air 1TB 🔵", "price": 84500},
        {"name": "iPhone 17 Pro 256GB 🟠", "price": 82000},
        {"name": "iPhone 17 Pro 256GB ⚪️", "price": 83500},
        {"name": "iPhone 17 Pro 256GB 🔵", "price": 85000},
        {"name": "iPhone 17 Pro 512GB 🔵🟠", "price": 99500},
        {"name": "iPhone 17 Pro 512GB ⚪️", "price": 103000},
        {"name": "iPhone 17 Pro 1TB 🟠", "price": 116000},
        {"name": "iPhone 17 Pro 1TB 🔵", "price": 119000},
        {"name": "iPhone 17 Pro 1TB ⚪️", "price": 121000},
        {"name": "iPhone 17 Pro Max 256GB 🟠", "price": 86000},
        {"name": "iPhone 17 Pro Max 256GB 🔵", "price": 88000},
        {"name": "iPhone 17 Pro Max 256GB ⚪️", "price": 94000},
        {"name": "iPhone 17 Pro Max 512GB 🔵⚪️", "price": 108000},
        {"name": "iPhone 17 Pro Max 512GB 🟠", "price": 110000},
        {"name": "iPhone 17 Pro Max 1TB 🔵", "price": 123500},
        {"name": "iPhone 17 Pro Max 1TB ⚪️", "price": 124000},
        {"name": "iPhone 17 Pro Max 1TB 🟠", "price": 124500},
        {"name": "iPhone 17 Pro Max 2TB 🟠", "price": 140000},
        {"name": "iPhone 17 Pro Max 2TB 🔵", "price": 149000},
        {"name": "iPhone 17 Pro Max 2TB ⚪️", "price": 152000},
    ]},
    "samsung": {"name": "📱 Samsung", "items": [
        {"name": "Samsung A07 4/64GB ⚫️", "price": 6600},
        {"name": "Samsung A07 4/128GB ⚫️🟢", "price": 7600},
        {"name": "Samsung A26 8/256GB ⚫️", "price": 17000},
        {"name": "Samsung A36 8/128GB ⚫️", "price": 17500},
        {"name": "Samsung A37 6/128GB 🟢", "price": 21500},
        {"name": "Samsung A37 8/128GB ⚫️⚪️🟢", "price": 22000},
        {"name": "Samsung A37 8/256GB ⚪️🟣🟢", "price": 23100},
        {"name": "Samsung A37 12/256GB 🟢", "price": 25000},
        {"name": "Samsung A56 8/256GB 🟢", "price": 25000},
        {"name": "Samsung A57 8/128GB 🔵🟣⚙️", "price": 24500},
        {"name": "Samsung A57 8/256GB 🟣🔵⚙️", "price": 26600},
        {"name": "Samsung A57 12/512GB ⚙️🩵", "price": 31600},
        {"name": "Samsung S25 Fe 8/128GB ⚫️", "price": 32000},
        {"name": "Samsung S25 Fe 8/256GB 🔵⚪️", "price": 37000},
        {"name": "Samsung S25 12/128GB 🟢", "price": 37500},
        {"name": "Samsung S25 12/256GB 🔵", "price": 40500},
        {"name": "Samsung S25 Plus 12/256GB 🔵", "price": 47000},
        {"name": "Samsung S25 Edge 12/256GB ⚫️", "price": 43500},
        {"name": "Samsung S25 Edge 12/512GB ⚫️", "price": 50000},
        {"name": "Samsung S25 Ultra 12/256GB ⚫️", "price": 59500},
        {"name": "Samsung S25 Ultra 12/512GB ⚫️⚪️⚙️", "price": 64000},
        {"name": "Samsung S26 12/256GB ❄️", "price": 48300},
        {"name": "Samsung S26 12/256GB 💖🟣", "price": 48500},
        {"name": "Samsung S26 12/512GB ⚫️🔵⚪️", "price": 59500},
        {"name": "Samsung S26+ 12/256GB ⚫️🟣⚪️", "price": 57600},
        {"name": "Samsung S26+ 12/512GB ⚫️💖🟣", "price": 65000},
        {"name": "Samsung S26 Ultra 12/256GB 🟣🩵", "price": 67500},
        {"name": "Samsung S26 Ultra 12/512GB ⚪️🟣🩵", "price": 82000},
        {"name": "Samsung Z Flip 7 Fe 8/128GB ⚫️", "price": 45500},
        {"name": "Samsung Z Flip 7 12/256GB ⚫️🔵", "price": 62000},
        {"name": "Samsung Z Flip 7 12/512GB ⚫️", "price": 66000},
        {"name": "Samsung Z Fold 7 12/256GB ⚪️", "price": 92000},
        {"name": "Samsung Z Fold 7 12/256GB 🔵⚪️", "price": 92500},
        {"name": "Samsung Z Fold 7 12/512GB ⚫️🔵⚪️", "price": 104000},
        {"name": "Samsung Watch Fit 3 ⚪️💖", "price": 3000},
        {"name": "Samsung Watch 7 44 LTE 🟢", "price": 12500},
        {"name": "Samsung Watch 8 44 ⚫️", "price": 16000},
        {"name": "Samsung Watch 8 Ultra 2025 47 LTE", "price": 24000},
        {"name": "Samsung Galaxy Buds 4 ⚫️⚪️", "price": 8900},
        {"name": "Samsung Galaxy Buds 4 Pro ⚪️", "price": 12400},
        {"name": "Samsung Tab S10 Fe 12/256GB Wi-Fi", "price": 34000},
        {"name": "Samsung Tab S10 Fe+ 12/256GB Wi-Fi 🔵", "price": 40500},
    ]},
    "macbook": {"name": "💻 MacBook", "items": [
        {"name": "Mac Mini M4/16/256", "price": 52500},
        {"name": "Mac Mini M4/16/512", "price": 70000},
        {"name": "Mac Mini M4/24/512", "price": 89000},
        {"name": "MacBook Neo 2026 A18 Pro/8/256 🔵⚪️", "price": 48500},
        {"name": "MacBook Neo 2026 A18 Pro/8/512 🔵⚪️🟡", "price": 57000},
        {"name": "MacBook Air 13 M4/16/256 ⭐️", "price": 77000},
        {"name": "MacBook Air 13 M4/24/512 ⭐️", "price": 99500},
        {"name": "MacBook Air 13 M5/16/512 🔵⭐️⚫️", "price": 79500},
        {"name": "MacBook Air 13 M5/16/1TB ⚫️🔵⭐️⚪️", "price": 95000},
        {"name": "MacBook Air 13 M5/24/1TB ⚪️⚫️", "price": 112000},
        {"name": "MacBook Air 15 M4/16/256 🔵", "price": 82000},
        {"name": "MacBook Air 15 M5/16/512 ⚫️⭐️🔵⚪️", "price": 95500},
        {"name": "MacBook Air 15 M5/16/1TB 🔵⚪️⭐️", "price": 112000},
        {"name": "MacBook Air 15 M5/24/1TB ⚪️⭐️", "price": 128000},
        {"name": "MacBook Pro 14 M5/16/1TB ⚫️⚪️", "price": 129000},
        {"name": "MacBook Pro 14 M5/24/1TB ⚪️", "price": 145000},
        {"name": "MacBook Pro 14 M5 Pro/24/2TB CPU16 ⚫️⚪️", "price": 192000},
        {"name": "MacBook Pro 14 M5 Pro/24/2TB CPU20 ⚫️⚪️", "price": 207500},
        {"name": "MacBook Pro 14 M5 Max/36/2TB ⚫️⚪️", "price": 258000},
        {"name": "MacBook Pro 16 M5 Max/36/2TB ⚫️⚪️", "price": 280000},
    ]},
    "ipad": {"name": "📟 iPad", "items": [
        {"name": "iPad 11 A16 128GB 5G 🔵", "price": 36500},
        {"name": "iPad 11 A16 128GB 5G ⚪️", "price": 38000},
        {"name": "iPad 11 A16 128GB Wi-Fi 🔵", "price": 26500},
        {"name": "iPad 11 A16 128GB Wi-Fi 💖🟡⚪️", "price": 27000},
        {"name": "iPad 11 A16 256GB Wi-Fi 💖⚪️🟡", "price": 36000},
        {"name": "iPad 11 A16 256GB 5G ⚪️", "price": 48000},
        {"name": "iPad Air 8 11 M4 128GB ⚫️🔵⭐️", "price": 43500},
        {"name": "iPad Air 8 13 M4 128GB Wi-Fi ⚫️⭐️🟣🔵", "price": 59000},
        {"name": "iPad Air 8 13 M4 256GB Wi-Fi ⚫️", "price": 68000},
        {"name": "iPad Pro 11 M4 512GB Wi-Fi ⚫️", "price": 77000},
        {"name": "iPad Pro 11 M4 512GB 5G ⚪️", "price": 87500},
        {"name": "iPad Pro 11 M4 1TB Wi-Fi ⚫️", "price": 89000},
        {"name": "iPad Pro 11 M5 256GB Wi-Fi ⚫️⚪️", "price": 73000},
        {"name": "iPad Pro 11 M5 512GB Wi-Fi ⚫️⚪️", "price": 86000},
        {"name": "iPad Pro 13 M4 512GB Wi-Fi ⚫️", "price": 86000},
        {"name": "iPad Pro 13 M5 512GB Wi-Fi ⚫️", "price": 106000},
        {"name": "iPad Pro 13 M5 512GB 5G ⚫️⚪️", "price": 110000},
        {"name": "iPad Pro 13 M5 2TB 5G ⚪️", "price": 132000},
    ]},
    "airpods": {"name": "🎧 AirPods", "items": [
        {"name": "AirPods 4", "price": 8500},
        {"name": "AirPods 4 ANC", "price": 13300},
        {"name": "AirPods Pro 2", "price": 12500},
        {"name": "AirPods Pro 3", "price": 15500},
        {"name": "AirPods Max 2 🟠🔵⭐️🟣", "price": 36500},
        {"name": "AirPods Max 2 (2026) ⚫️🟣🔵⭐️🟠", "price": 41500},
    ]},
    "watch": {"name": "⌚️ Apple Watch", "items": [
        {"name": "Apple Watch SE 3 40 ⚫️ s/m", "price": 18000},
        {"name": "Apple Watch SE 3 40 ⭐️ m/l", "price": 19300},
        {"name": "Apple Watch SE 3 44 ⚫️⭐️", "price": 20500},
        {"name": "Apple Watch S10 46 💖 Sim", "price": 23500},
        {"name": "Apple Watch S11 42 ⚫️💖 s/m", "price": 26000},
        {"name": "Apple Watch S11 46 ⚫️💖 m/l", "price": 28000},
        {"name": "Apple Watch Ultra 2 49 Natural Ti 🩶", "price": 48500},
        {"name": "Apple Watch Ultra 3 49 Black Ocean Band 🖤", "price": 55000},
        {"name": "Apple Watch Ultra 3 49 Black Milanese Loop 🖤", "price": 65500},
    ]},
    "xiaomi": {"name": "🔥 Xiaomi / POCO", "items": [
        {"name": "POCO X7 12/512GB 🟢⚪️", "price": 21200},
        {"name": "POCO X7 Pro 12/512GB ⚫️🟡🟢", "price": 26000},
        {"name": "POCO X8 Pro 8/512GB ⚪️🟢", "price": 25500},
        {"name": "POCO X8 Pro 12/512GB 🟢⚪️", "price": 28000},
        {"name": "POCO X8 Pro Max 12/256GB ⚫️🔵", "price": 32000},
        {"name": "POCO X8 Pro Max 12/512GB 🔵", "price": 34500},
        {"name": "POCO F8 Pro 12/256GB ⚫️", "price": 37500},
        {"name": "POCO F8 Pro 12/512GB 🔵⚪️", "price": 40000},
        {"name": "POCO F8 Ultra 12/256GB ⚫️", "price": 50000},
        {"name": "Xiaomi Note 15 Pro 12/256GB ⚫️🔵", "price": 19900},
        {"name": "Xiaomi Mi 15T 12/512GB 🟡⚙️", "price": 36500},
        {"name": "Xiaomi Mi 15T Pro 12/256GB ⚫️", "price": 44000},
        {"name": "Xiaomi Mi 15T Pro 12/512GB ⚫️🟡", "price": 49000},
        {"name": "Xiaomi Mi 15 12/256GB ⚫️⚪️", "price": 47000},
        {"name": "Xiaomi Mi 15 12/512GB 🟢⚪️", "price": 49500},
        {"name": "Xiaomi Mi 17T Pro 12/256GB ⚫️", "price": 48500},
        {"name": "Xiaomi Mi 17T Pro 12/512GB ⚫️🔵🟣", "price": 52000},
        {"name": "Xiaomi Mi 17 Ultra 16/512GB ⚫️⚪️", "price": 85000},
        {"name": "Xiaomi Mi Pad 8 8/256GB ⚫️🔵", "price": 29000},
        {"name": "Xiaomi Mi Pad 8 Pro 8/256GB ⚫️🔵🟢", "price": 41000},
    ]},
    "honor": {"name": "🏅 Honor / Huawei", "items": [
        {"name": "HONOR 400 8/512GB ⚫️🟡", "price": 27500},
        {"name": "HONOR 600 8/256GB ⚫️⚪️🟠", "price": 30500},
        {"name": "HONOR Magic 8 Pro 12/512GB 🩵", "price": 69500},
        {"name": "HONOR Magic V5 16/512GB ⚪️", "price": 85500},
        {"name": "Huawei Pura 80 12/256GB ⚫️🟡", "price": 33500},
        {"name": "Huawei Pura 80 Pro 12/512GB ⚫️", "price": 47500},
        {"name": "Huawei Mate 80 Pro 16/512GB 🟢🟡", "price": 62500},
        {"name": "Huawei Mate X7 16/512GB ⚫️🔴", "price": 94000},
    ]},
    "pixel": {"name": "📸 Google Pixel", "items": [
        {"name": "Pixel 9a 8/128GB ⚫️", "price": 29600},
        {"name": "Pixel 9a 8/256GB ⚫️", "price": 31000},
        {"name": "Pixel 10a 8/256GB ⚫️🟣🟢", "price": 35700},
        {"name": "Pixel 10 12/128GB 🩵", "price": 44500},
        {"name": "Pixel 10 12/256GB ⚫️🩵🔵", "price": 46500},
        {"name": "Pixel 10 Pro XL 16/256GB ⚫️⚪️🔵🟢", "price": 66500},
        {"name": "Pixel Watch 4 41 🟠", "price": 22800},
        {"name": "Pixel Watch 4 46 ⚫️", "price": 26800},
    ]},
}

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_price(base_price: int) -> int:
    return round(base_price * (1 + MARKUP) / 100) * 100


def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("💬 Менеджер", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ])


def catalog_keyboard():
    kb = [[InlineKeyboardButton(cat["name"], callback_data=f"cat_{key}")]
          for key, cat in CATALOG.items()]
    kb.append([InlineKeyboardButton("🏠 Главная", callback_data="home")])
    return InlineKeyboardMarkup(kb)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "👋 Добро пожаловать в *Plata*!\n\nОригинальная техника по лучшим ценам 🔥\nДоставка по всей России 🚚\n\nВыберите раздел:"
    if update.message:
        await update.message.reply_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")


async def catalog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("📦 *Каталог*\n\nВыберите категорию:", reply_markup=catalog_keyboard(), parse_mode="Markdown")


async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat_key = q.data.replace("cat_", "")
    cat = CATALOG.get(cat_key)
    if not cat:
        await q.answer("Категория не найдена", show_alert=True)
        return
    lines = [f"*{cat['name']}*\n"]
    for item in cat["items"]:
        lines.append(f"• {item['name']} — *{get_price(item['price']):,} ₽*".replace(",", " "))
    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:4000] + "\n\n_...уточняйте у менеджера!_"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Заказать", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="catalog")],
    ])
    await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = "🏪 *Plata — оригинальная техника*\n\n✅ Только оригинальные устройства\n🚚 Доставка по всей России\n🔒 Гарантия на все товары"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Менеджер", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("🏠 Главная", callback_data="home")],
    ])
    await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")


async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = update.callback_query.data
    if d == "home": await start(update, context)
    elif d == "catalog": await catalog_handler(update, context)
    elif d.startswith("cat_"): await category_handler(update, context)
    elif d == "about": await about_handler(update, context)


app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
print("Bot started!")
app.run_polling()
