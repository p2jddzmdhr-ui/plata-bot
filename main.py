"""
main.py — Telegram бот Plata
Цены читаются из prices.json с наценкой
"""

import json
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MANAGER = "aikhang"
PRICES_FILE = "prices.json"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# ─── Загрузка цен ─────────────────────────────────────────
def load_prices():
    """Читает prices.json каждый раз — всегда актуальные цены"""
    with open(PRICES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_price_with_markup(base_price: int, markup: float) -> int:
    """Применяет наценку и округляет до 100"""
    return round(base_price * (1 + markup) / 100) * 100


# ─── Клавиатуры ───────────────────────────────────────────
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("💬 Менеджер", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ])


def catalog_keyboard(categories: dict):
    icons = {
        "iphone": "🍎",
        "samsung": "📱",
        "macbook": "💻",
        "ipad": "📟",
        "airpods": "🎧",
        "watch": "⌚️",
        "xiaomi": "🔥",
        "honor": "🏅",
        "pixel": "📸",
    }
    kb = []
    for key, cat in categories.items():
        icon = icons.get(key, "📦")
        kb.append([InlineKeyboardButton(
            f"{icon} {cat['name']}",
            callback_data=f"cat_{key}"
        )])
    kb.append([InlineKeyboardButton("🏠 Главная", callback_data="home")])
    return InlineKeyboardMarkup(kb)


def back_keyboard(back_to="catalog"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Заказать", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=back_to)],
    ])


# ─── Хэндлеры ─────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Добро пожаловать в *Plata*!\n\n"
        "Оригинальная техника по лучшим ценам 🔥\n"
        "Доставка по всей России 🚚\n\n"
        "Выберите раздел:"
    )
    kb = main_keyboard()
    if update.message:
        await update.message.reply_text(text, reply_markup=kb, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")


async def catalog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = load_prices()
    await q.edit_message_text(
        "📦 *Каталог*\n\nВыберите категорию:",
        reply_markup=catalog_keyboard(data["categories"]),
        parse_mode="Markdown"
    )


async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    cat_key = q.data.replace("cat_", "")
    data = load_prices()
    markup = data.get("markup", 0.10)
    cat = data["categories"].get(cat_key)

    if not cat:
        await q.answer("Категория не найдена", show_alert=True)
        return

    lines = [f"*{cat['name']}*\n"]
    for item in cat["items"]:
        final_price = get_price_with_markup(item["price"], markup)
        lines.append(f"• {item['name']} — *{final_price:,} ₽*".replace(",", " "))

    # Telegram limit 4096 chars — разбиваем если нужно
    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:4000] + "\n\n_...и другие модели. Уточняйте у менеджера!_"

    await q.edit_message_text(
        text,
        reply_markup=back_keyboard("catalog"),
        parse_mode="Markdown"
    )


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "🏪 *Plata — оригинальная техника*\n\n"
        "✅ Только оригинальные устройства\n"
        "🚚 Доставка по всей России\n"
    "💳 Рассрочка и кредит\n"
        "🔒 Гарантия на все товары\n\n"
        "По всем вопросам — наш менеджер:"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Написать менеджеру", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("🏠 Главная", callback_data="home")],
    ])
    await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")


async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = update.callback_query.data
    if d == "home":
        await start(update, context)
    elif d == "catalog":
        await catalog_handler(update, context)
    elif d.startswith("cat_"):
        await category_handler(update, context)
    elif d == "about":
        await about_handler(update, context)


# ─── Запуск ───────────────────────────────────────────────
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))

print("✅ Bot started!")
app.run_polling()
