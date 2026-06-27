import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MANAGER = "plata_mgr"
ORDER_URL = "https://t.me/plata_mgr?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%0A%0A%D0%A5%D0%BE%D1%87%D1%83%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%3A%0A%0A%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%3A%20%0A%D0%A6%D0%B2%D0%B5%D1%82%3A%20%0A%D0%9F%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%3A%20%0A%D0%A4%D0%BB%D0%B0%D0%B3%3A%20"
OWNER_ID = 294265601
MARKUP = {
    "iphone": 0.10,
    "samsung": 0.10,
    "samsung_watch": 0.15,
    "macbook": 0.10,
    "ipad": 0.10,
    "airpods": 0.15,
    "watch": 0.15,
    "xiaomi": 0.15,
    "poco": 0.15,
    "honor": 0.15,
    "pixel": 0.15,
    "oneplus": 0.15,
    "realme": 0.15,
    "dyson": 0.20,
    "vacuum": 0.20,
    "laptops": 0.15,
    "cameras": 0.20,
    "garmin": 0.20,
    "gaming": 0.15,
    "speakers": 0.20,
    "rugged": 0.20,
    "accessories": 1.00,
}

CATALOG = {
    "iphone": {"name": "🍎 iPhone", "items": [
        {"name": "━━━ iPhone 13 ━━━", "price": 0},
        {"name": "🇪🇺🍎 iPhone 13 128GB ⚫️", "price": 33000},
        {"name": "🇪🇺🍎 iPhone 13 512GB ⚪️", "price": 42000},
        {"name": "━━━ iPhone 14 ━━━", "price": 0},
        {"name": "🇪🇺🍎 iPhone 14 128GB 🔴🟡", "price": 38000},
        {"name": "🇪🇺🍎 iPhone 14 128GB 🔵", "price": 41000},
        {"name": "🇪🇺🍎 iPhone 14 512GB ⚫️⚪️", "price": 46000},
        {"name": "🇪🇺🍎 iPhone 14 Plus 128GB 🟡", "price": 43000},
        {"name": "━━━ iPhone 15 ━━━", "price": 0},
        {"name": "🇪🇺🍎 iPhone 15 128GB ⚫️", "price": 47000},
        {"name": "🇪🇺🍎 iPhone 15 256GB ⚫️", "price": 53500},
        {"name": "🇪🇺🍎 iPhone 15 Plus 128GB 🟡", "price": 48000},
        {"name": "🇪🇺🍎 iPhone 15 Plus 128GB 🔵", "price": 48500},
        {"name": "🇭🇰🍎 iPhone 15 Pro 128GB 🔵", "price": 66500},
        {"name": "🇯🇵🍎 iPhone 15 Pro Max 1TB ⚫️⚙️🔵", "price": 96000},
        {"name": "━━━ iPhone 16 ━━━", "price": 0},
        {"name": "🇪🇺🍎 iPhone 16e 256GB ⚪️", "price": 42000},
        {"name": "🇪🇺🇯🇵🍎 iPhone 16 128GB 🟢", "price": 49500},
        {"name": "🇪🇺🍎 iPhone 16 128GB 💖⚪️", "price": 50000},
        {"name": "🇪🇺🍎 iPhone 16 256GB 💖", "price": 58000},
        {"name": "🇪🇺🍎 iPhone 16 Plus 128GB 🔵💖🟢", "price": 58000},
        {"name": "🇪🇺🍎 iPhone 16 Plus 256GB 💖", "price": 65000},
        {"name": "🇭🇰🍎 iPhone 16 Pro 128GB ⚪️", "price": 70500},
        {"name": "🇭🇰🍎 iPhone 16 Pro 128GB 🟠⚙️", "price": 74000},
        {"name": "🇭🇰🍎 iPhone 16 Pro 128GB ⚫️", "price": 75000},
        {"name": "🇪🇺🍎 iPhone 16 Pro 1TB ⚪️", "price": 104500},
        {"name": "🇪🇺🍎 iPhone 16 Pro Max 256GB 🟠", "price": 84500},
        {"name": "🇺🇸🍎 iPhone 16 Pro Max 512GB ⚫️", "price": 97000},
        {"name": "🇪🇺🍎 iPhone 16 Pro Max 512GB 🟠", "price": 101500},
        {"name": "🇪🇺🍎 iPhone 16 Pro Max 1TB 🟠", "price": 114000},
        {"name": "━━━ iPhone 17 ━━━", "price": 0},
        {"name": "🇯🇵🍎 iPhone 17e 256GB 💖", "price": 43500},
        {"name": "🇪🇺🍎 iPhone 17e 256GB ⚪️", "price": 50500},
        {"name": "🇯🇵🍎 iPhone 17e 512GB ⚫️⚪️", "price": 57000},
        {"name": "🇯🇵🍎 iPhone 17 256GB ⚫️🟣🔵⚪️🟢", "price": 61000},
        {"name": "🇪🇺🍎 iPhone 17 256GB ⚫️🔵⚪️🟣", "price": 64000},
        {"name": "🇯🇵🍎 iPhone 17 512GB ⚫️", "price": 75500},
        {"name": "🇯🇵🍎 iPhone 17 Air 256GB 🔵", "price": 66500},
        {"name": "🇯🇵🍎 iPhone 17 Air 256GB ⚫️🟡⚪️", "price": 67500},
        {"name": "🇯🇵🍎 iPhone 17 Air 512GB 🔵", "price": 71000},
        {"name": "🇯🇵🍎 iPhone 17 Air 512GB 🟡", "price": 71500},
        {"name": "🇯🇵🍎 iPhone 17 Air 1TB 🔵", "price": 84500},
        {"name": "🇯🇵🍎 iPhone 17 Pro 256GB 🟠", "price": 82000},
        {"name": "🇯🇵🍎 iPhone 17 Pro 256GB ⚪️", "price": 84000},
        {"name": "🇯🇵🍎 iPhone 17 Pro 256GB 🔵", "price": 85000},
        {"name": "🇪🇺🍎 iPhone 17 Pro 256GB 🟠", "price": 90500},
        {"name": "🇪🇺🍎 iPhone 17 Pro 256GB 🔵⚪️", "price": 92000},
        {"name": "🇯🇵🍎 iPhone 17 Pro 512GB 🔵🟠", "price": 99500},
        {"name": "🇯🇵🍎 iPhone 17 Pro 512GB ⚪️", "price": 102000},
        {"name": "🇪🇺🍎 iPhone 17 Pro 512GB 🔵🟠⚪️", "price": 107000},
        {"name": "🇯🇵🍎 iPhone 17 Pro 1TB 🟠", "price": 116000},
        {"name": "🇯🇵🍎 iPhone 17 Pro 1TB 🔵", "price": 118500},
        {"name": "🇯🇵🍎 iPhone 17 Pro 1TB ⚪️", "price": 121000},
        {"name": "🇪🇺🍎 iPhone 17 Pro 1TB ⚪️", "price": 128000},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 256GB 🔵", "price": 88000},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 256GB 🟠", "price": 99500},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 256GB 🔵", "price": 100500},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 512GB 🔵⚪️🟠", "price": 108000},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 512GB 🔵⚪️🟠", "price": 117000},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 1TB 🔵", "price": 123000},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 1TB 🟠⚪️", "price": 124000},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 1TB 🔵⚪️", "price": 136000},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 1TB 🟠", "price": 136500},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 2TB 🟠", "price": 140000},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 2TB 🔵", "price": 149000},
        {"name": "🇯🇵🍎 iPhone 17 Pro Max 2TB ⚪️", "price": 152000},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 2TB 🔵🟠", "price": 160000},
        {"name": "🇪🇺🍎 iPhone 17 Pro Max 2TB ⚪️", "price": 162000},
    ]},
    "samsung": {"name": "📱 Samsung", "items": [
        {"name": "━━━ Samsung A серия ━━━", "price": 0},
        {"name": "🇷 Samsung A07 4/64GB ⚫️", "price": 6600},
        {"name": "🇷🇺 Samsung A07 4/128GB ⚫️🟢", "price": 7600},
        {"name": "🇷🇺 Samsung A26 6/128GB ⚫️", "price": 14800},
        {"name": "🇷🇺 Samsung A26 8/256GB ⚫️", "price": 17000},
        {"name": "🇷🇺 Samsung A36 8/128GB ⚫️", "price": 17500},
        {"name": "🇪🇺 Samsung A37 6/128GB 🟢", "price": 21500},
        {"name": "🇷🇺 Samsung A37 8/128GB ⚫️⚪️🟢", "price": 22000},
        {"name": "🇪🇺 Samsung A37 8/256GB ⚪🟣🟢", "price": 23100},
        {"name": "🇪🇺 Samsung A37 12/256GB 🟢", "price": 25000},
        {"name": "🇪🇺 Samsung A56 8/256GB 🟢", "price": 25000},
        {"name": "🇪🇺 Samsung A57 8/128GB 🔵🟣⚙️", "price": 24500},
        {"name": "🇷🇺🇪 Samsung A57 8/256GB 🔵⚙️", "price": 26600},
        {"name": "🇪🇺 Samsung A57 12/512GB 🔵⚙️🩵", "price": 31500},
        {"name": "━━━ Samsung S25 ━━━", "price": 0},
        {"name": "🇪🇺 Samsung S25 Fe 8/128GB ⚫️", "price": 31000},
        {"name": "🇪🇺 Samsung S25 Fe 8/256GB ⚫️⚪️🔵", "price": 36700},
        {"name": "🇪🇺 Samsung S25 12/128GB ⚪️🟢", "price": 37500},
        {"name": "🇪🇺 Samsung S25 12/256GB 🔵⚪️🩵", "price": 40500},
        {"name": "🇪🇺 Samsung S25 Edge 12/256GB ⚫️", "price": 43500},
        {"name": "🇪🇺 Samsung S25 Edge 12/512GB ⚫️", "price": 50000},
        {"name": "🇭🇰 Samsung S25 Ultra 12/256GB 🩵", "price": 58000},
        {"name": "🇪🇺 Samsung S25 Ultra 12/256GB ⚫️🩵", "price": 59500},
        {"name": "🇪🇺 Samsung S25 Ultra 12/512GB ⚫️⚪️", "price": 63500},
        {"name": "🇪🇺 Samsung S25 Ultra 12/1TB 🩵", "price": 68500},
        {"name": "━━━ Samsung S26 ━━━", "price": 0},
        {"name": "🇪🇺 Samsung S26 12/256GB ❄️", "price": 48000},
        {"name": "🇪🇺 Samsung S26 12/256GB ⚫️💖🟣", "price": 48500},
        {"name": "🇪🇺 Samsung S26 12/512GB ⚫️⚪️", "price": 59500},
        {"name": "🇪🇺 Samsung S26+ 12/256GB 🟣⚪️", "price": 57400},
        {"name": "🇪🇺 Samsung S26+ 12/512GB ⚫️❄️💖🟣", "price": 64500},
        {"name": "🇪🇺 Samsung S26 Ultra 12/256GB 🟣🩵", "price": 67000},
        {"name": "🇪🇺 Samsung S26 Ultra 12/512GB ⚪️🟣🩵", "price": 81500},
        {"name": "🇪🇺 Samsung S26 Ultra 16/1TB ❄️", "price": 94000},
        {"name": "🇪🇺 Samsung S26 Ultra 16/1TB ⚫️", "price": 96500},
        {"name": "━━━ Samsung Z Flip ━━━", "price": 0},
        {"name": "🇪🇺 Samsung Z Flip 7 Fe 8/128GB ⚫️", "price": 45500},
        {"name": "🇷🇺 Samsung Z Flip 7 12/256GB ⚫️🔵", "price": 62000},
        {"name": "🇷🇺 Samsung Z Flip 7 12/256GB 🔴", "price": 62500},
        {"name": "🇪🇺 Samsung Z Flip 7 12/512GB ⚫️", "price": 66000},
        {"name": "━━━ Samsung Z Fold ━━━", "price": 0},
        {"name": "🇭🇰 Samsung Z Fold 7 12/256GB ⚪️", "price": 90000},
        {"name": "🇪🇺 Samsung Z Fold 7 12/256GB ⚪", "price": 91000},
        {"name": "🇪🇺 Samsung Z Fold 7 12/256GB ⚫️🔵", "price": 92000},
        {"name": "🇪🇺 Samsung Z Fold 7 12/512GB 🔵", "price": 103000},
        {"name": "🇪🇺 Samsung Z Fold 7 12/512GB ⚫️⚪️", "price": 104000},
        {"name": "━━━ Samsung Tab ━━━", "price": 0},
        {"name": "🇪🇺 Samsung Tab S10 Fe 12/256GB Wi-Fi", "price": 34000},
        {"name": "🇪🇺 Samsung Tab S10 Fe+ 12/256GB Wi-Fi 🔵", "price": 40500},
    ]},
    "samsung_watch": {"name": "⌚️ Samsung Watch & Buds", "items": [
        {"name": "━━━ Samsung Watch ━━━", "price": 0},
        {"name": "🇪🇺 Samsung Watch Fit 3 ⚪️", "price": 3000},
        {"name": "🇪🇺 Samsung Watch 7 44 LTE 🟢", "price": 12500},
        {"name": "🇪🇺 Samsung Watch 8 40 ⚫️", "price": 14000},
        {"name": "🇪🇺 Samsung Watch 8 40 ⚪️", "price": 15000},
        {"name": "🇷🇺🇪🇺 Samsung Watch 8 44 ⚫️", "price": 16000},
        {"name": "🇪🇺 Samsung Watch 8 46 Classic ⚪️", "price": 17000},
        {"name": "🇪🇺 Samsung Watch 8 46 Classic ⚫️", "price": 18500},
        {"name": "🇪🇺 Samsung Watch 8 Ultra 2025 47 LTE 🔵⚪️⚙️🟠", "price": 24000},
        {"name": "🇪🇺 Samsung Watch 8 Ultra 2025 47 LTE ⚫️", "price": 24500},
        {"name": "━━━ Samsung Galaxy Buds ━━━", "price": 0},
        {"name": "🇪🇺 Samsung Galaxy Buds Core ⚫️⚪️", "price": 3000},
        {"name": "🇪🇺 Samsung Galaxy Buds 3 Fe ⚫️⚙", "price": 5200},
        {"name": "🇪🇺 Samsung Galaxy Buds 3 ⚙️", "price": 6500},
        {"name": "🇪🇺 Samsung Galaxy Buds 3 Pro ⚙️", "price": 9200},
        {"name": "🇪🇺 Samsung Galaxy Buds 4 ⚫️⚪️", "price": 8900},
        {"name": "🇪🇺 Samsung Galaxy Buds 4 Pro ⚫️⚪️", "price": 12400},
    ]},
    "macbook": {"name": "💻 MacBook", "items": [
        {"name": "━━━ Mac Mini ━━━", "price": 0},
        {"name": "🔥 Mac Mini M4/16/256", "price": 55000},
        {"name": "🔥 Mac Mini M4/16/512", "price": 71000},
        {"name": "🔥 Mac Mini M4/24/512", "price": 91000},
        {"name": "━━━ MacBook Neo 2026 ━━━", "price": 0},
        {"name": "💻 MacBook Neo 2026 A18 Pro/8/256 🔵⚪️🟡", "price": 55000},
        {"name": "💻 MacBook Neo 2026 A18 Pro/8/512 🔵", "price": 63000},
        {"name": "━━━ MacBook Air 13 ━━━", "price": 0},
        {"name": "🍎💻 MacBook Air 13 M4/16/256 ⭐️", "price": 77000},
        {"name": "🍎💻 MacBook Air 13 M4/24/512 ⭐️", "price": 99500},
        {"name": "🍎💻 MacBook Air 13 M5/16/512 🔵⭐️⚫️", "price": 79500},
        {"name": "🍎💻 MacBook Air 13 M5/16/1TB ⚫️⭐️ ", "price": 103000},
        {"name": "🍎💻 MacBook Air 13 M5/24/1TB ⚪️⚫️", "price": 112000},
        {"name": "━━━ MacBook Air 15 ━━━", "price": 0},
        {"name": "🍎💻 MacBook Air 15 M4/16/256 🔵", "price": 82000},
        {"name": "🍎💻 MacBook Air 15 M5/16/512 ⚫️⭐️🔵⚪️", "price": 105000},
        {"name": "🍎💻 MacBook Air 15 M5/16/1TB ⭐️", "price": 119000},
        {"name": "🍎💻 MacBook Air 15 M5/24/1TB ⚪️⭐️", "price": 128000},
        {"name": "━━━ MacBook Pro ━━━", "price": 0},
        {"name": "🍎💻 MacBook Pro 14 M5/24/1TB ⚪️", "price": 145000},
        {"name": "🍎💻 MacBook Pro 14 M5 Pro/24/2TB CPU16 ⚫️⚪️", "price": 197000},
        {"name": "🍎💻 MacBook Pro 14 M5 Pro/24/2TB CPU20 ⚫️⚪", "price": 207000},
        {"name": "🍎💻 MacBook Pro 14 M5 Max/36/2TB ⚫️", "price": 261000},
        {"name": "🍎💻 MacBook Pro 16 M5 Max/36/2TB ⚫️⚪️", "price": 289000},
        {"name": "━━━ Аксессуары ━━━", "price": 0},
        {"name": "🖱️ Magic Mouse ⚪️", "price": 6400},
    ]},
   "ipad": {"name": "📟 iPad", "items": [
        {"name": "━━━ iPad 11 ━━━", "price": 0},
        {"name": "🍎 iPad 11 A16 128 Wi-Fi 🔵🟡⚪️💖", "price": 30500},
        {"name": "🍎 iPad 11 A16 256 Wi-Fi 🔵💖⚪️🟡", "price": 38500},
        {"name": "🍎 iPad 11 A16 512 Wi-Fi ⚪️", "price": 48000},
        {"name": "━━━ iPad Air ━━━", "price": 0},
        {"name": "🍎 iPad Air 6 11 M2 256 5G ⭐️", "price": 47000},
        {"name": "🍎 iPad Air 6 11 M2 512 5G ⚫️🟣", "price": 50000},
        {"name": "🍎 iPad Air 6 11 M2 1TB 5G 🔵🟣", "price": 53000},
        {"name": "🍎 iPad Air 7 11 M3 128 ⭐️", "price": 41000},
        {"name": "🍎 iPad Air 7 11 M3 512 ⚫️", "price": 59000},
        {"name": "🍎 iPad Air 8 11 M4 256 🔵", "price": 58000},
        {"name": "🍎 iPad Air 6 13 M2 512 5G 🟣", "price": 58000},
        {"name": "🍎 iPad Air 6 13 M2 1TB 5G ⭐️🟣", "price": 62000},
        {"name": "🆕🍎 iPad Air 8 13 M4 128 Wi-Fi ⭐️", "price": 60000},
        {"name": "━━━ iPad Pro 11 ━━━", "price": 0},
        {"name": "🍎 iPad Pro 11 M4 256 5G ⚫️", "price": 77000},
        {"name": "🍎 iPad Pro 11 M4 512 Wi-Fi ⚫️", "price": 80000},
        {"name": "🍎 iPad Pro 11 M4 512 5G ⚫️⚪", "price": 89000},
        {"name": "🍎 iPad Pro 11 M4 1TB Wi-Fi ⚫️", "price": 92000},
        {"name": "🍎 iPad Pro 11 M4 1TB 5G ⚫️⚪️", "price": 110000},
        {"name": "🍎 iPad Pro 11 M5 256 Wi-Fi ⚫️⚪️", "price": 78000},
        {"name": "🍎 iPad Pro 11 M5 256 5G ⚫️", "price": 87000},
        {"name": "🍎 iPad Pro 11 M5 512 Wi-Fi ⚪️", "price": 89000},
        {"name": "━━━ iPad Pro 13 ━━━", "price": 0},
        {"name": "🍎 iPad Pro 13 M4 2TB 5G ⚫️⚪️", "price": 120000},
        {"name": "🍎 iPad Pro 13 M5 512 5G ⚫️", "price": 112000},
        {"name": "🍎 iPad Pro 13 M5 2TB 5G ⚪️", "price": 134000},
        {"name": "━━━ Аксессуары ━━━", "price": 0},
        {"name": "⌨️ Keyboard for iPad 11 A16", "price": 14500},
        {"name": "⌨️ Keyboard for iPad Pro 11 2024 ⚪️⚫️", "price": 26500},
        {"name": "🖊️ Apple Pencil USB-C", "price": 6200},
        {"name": "🖊️ Apple Pencil Pro", "price": 8300},
    ]},
    "airpods": {"name": "🎧 AirPods", "items": [
        {"name": "━━━ EarPods ━━━", "price": 0},
        {"name": "🇪🇺🎧 EarPods Lightning", "price": 1273},
        {"name": "🇪🇺🎧 EarPods USB-C", "price": 1273},
        {"name": "━━━ AirPods ━━━", "price": 0},
        {"name": "🇪🇺🎧 AirPods 4", "price": 8200},
        {"name": "🇪🇺🎧 AirPods 4 ANC", "price": 12300},
        {"name": "━━━ AirPods Pro ━━━", "price": 0},
        {"name": "🇪🇺🎧 AirPods Pro 2", "price": 11800},
        {"name": "🇪🇺🎧 AirPods Pro 3", "price": 14700},
        {"name": "━━━ AirPods Max ━━━", "price": 0},
        {"name": "🇪🇺🎧 AirPods Max 2 ⭐️🟣", "price": 33600},
        {"name": "🆕🇪🇺🎧 AirPods Max 2 2026 ⚫️🟣🔵⭐️🟠", "price": 38600},
    ]},
    "watch": {"name": "⌚️ Apple Watch", "items": [
        {"name": "━━━ Apple Watch SE ━━━", "price": 0},
        {"name": "⌚️ Apple Watch SE 3 40 ⚫️ s/m", "price": 18000},
        {"name": "⌚️ Apple Watch SE 3 40 ⭐️ m/l", "price": 19300},
        {"name": "⌚️ Apple Watch SE 3 44 ⚫️ m/l", "price": 20500},
        {"name": "━━━ Apple Watch S10/S11 ━━━", "price": 0},
        {"name": "⌚️ Apple Watch S10 46 💖 Sim", "price": 23500},
        {"name": "⌚️ Apple Watch S11 42 ⚫️💖 s/m", "price": 26500},
        {"name": "⌚️ Apple Watch S11 46 ⚫️💖 m/l", "price": 28500},
        {"name": "━━━ Apple Watch Ultra 2 ━━━", "price": 0},
        {"name": "⌚️ Apple Watch Ultra 2 49 Natural Ti 🩶", "price": 48500},
        {"name": "⌚️ Apple Watch Ultra 2 49 Black Ti dark green", "price": 46500},
        {"name": "⌚️ Apple Watch Ultra 2 49 Black Milanese", "price": 50000},
        {"name": "━━━ Apple Watch Ultra 3 ━━━", "price": 0},
        {"name": "⌚️ Apple Watch Ultra 3 49 Black Ocean Band 🖤", "price": 55000},
        {"name": "⌚️ Apple Watch Ultra 3 49 Black Ti Black 🖤", "price": 55500},
        {"name": "⌚️ Apple Watch Ultra 3 49 Black Milanese Loop 🖤", "price": 65500},
    ]},
    "xiaomi": {"name": "🔥 Xiaomi", "items": [
        {"name": "━━━ Xiaomi Note 14 ━━━", "price": 0},
        {"name": "🇷🇺 Note 14 6/128 🟢", "price": 11000},
        {"name": "🇪🇺 Note 14 8/256 🟣", "price": 13500},
        {"name": "🇷🇺 Note 14S 8/128 🔵🟣", "price": 13000},
        {"name": "🇪🇺 Note 14S 8/256 ⚫️", "price": 15200},
        {"name": "🇪🇺 Note 14S 12/512 ⚫️", "price": 19400},
        {"name": "🇷🇺 Note 14 Pro+ 12/512 5G 🟡", "price": 28700},
        {"name": "━━━ Xiaomi Note 15 ━━━", "price": 0},
        {"name": "🇷🇺 Note 15 6/128 ⚫️🔵🟢", "price": 12500},
        {"name": "🇪🇺 Note 15 Pro 8/256 ⚫️", "price": 19100},
        {"name": "🇪🇺 Note 15 Pro 12/512 ⚫️", "price": 24000},
        {"name": "🇷🇺 Note 15 Pro+ 12/512 ⚫️", "price": 32400},
        {"name": "━━━ Xiaomi Mi 15 ━━━", "price": 0},
        {"name": "🇪🇺 Mi 15T 12/512 🟡⚙️", "price": 38700},
        {"name": "🇪🇺 Mi 15T Pro 12/256 ⚫️", "price": 46500},
        {"name": "🇪🇺 Mi 15T Pro 12/512 ⚫️🟡", "price": 51700},
        {"name": "🇪🇺 Mi 15 12/256 ⚫️⚪️", "price": 49600},
        {"name": "🇪🇺 Mi 15 12/512 🟢⚪️", "price": 51700},
        {"name": "━━━ Xiaomi Mi 17 ━━━", "price": 0},
        {"name": "🇷🇺 Mi 17T 12/512 ⚫️", "price": 41300},
        {"name": "🇷🇺 Mi 17T Pro 12/256 ⚫️🟣🔵", "price": 50200},
        {"name": "🇷🇺 Mi 17T Pro 12/512 🟣⚫️", "price": 54900},
        {"name": "🇷🇺🇪🇺 Mi 17T Pro 12/1TB ⚫️🟣", "price": 62200},
        {"name": "🇪🇺 Mi 17 Ultra 16/512 ⚪️", "price": 89900},
        {"name": "🇪🇺 Mi 17 Ultra 16/1TB ⚫️⚪️", "price": 99300},
        {"name": "━━━ Xiaomi Планшеты ━━━", "price": 0},
        {"name": "🔥🇷🇺 Mi Pad 8 8/128 ⚫️🔵🟢", "price": 28200},
        {"name": "🔥🇷🇺🇪🇺 Mi Pad 8 Pro 8/256 ⚫️🔵🟢", "price": 42800},
        {"name": "━━━ Xiaomi Другое ━━━", "price": 0},
        {"name": "⌚️ Xiaomi Watch S5 46 ⚫️⚪️", "price": 9500},
        {"name": "🇷🇺🏠 Xiaomi Робот Vacuum X20 Max ⚫️", "price": 37600},
    ]},
   "poco": {"name": "🔥 POCO", "items": [
        {"name": "━━━ POCO C серия ━━━", "price": 0},
        {"name": "🇷🇺 POCO C85 6/128 ⚫️🟢🟣", "price": 7700},
        {"name": "🇷🇺 POCO C85 8/256 ⚫️🟢", "price": 8700},
        {"name": "━━━ POCO M серия ━━━", "price": 0},
        {"name": "🇪🇺 POCO M8 8/256 ⚫️", "price": 15200},
        {"name": "🇷🇺🇪🇺 POCO M8 Pro 12/512 ⚪️🟢", "price": 24500},
        {"name": "━━━ POCO X серия ━━━", "price": 0},
        {"name": "🇷🇺🇪🇺 POCO X7 12/512 🟢⚪️", "price": 21500},
        {"name": "🇪🇺 POCO X7 Pro 12/512 ⚫️🟡🟢", "price": 26000},
        {"name": "🆕🇷🇺 POCO X8 Pro 8/256 ⚫️", "price": 24400},
        {"name": "🆕🇷🇺🇪🇺 POCO X8 Pro 8/512 🟢⚪", "price": 26300},
        {"name": "🆕🇷🇺 POCO X8 Pro 12/512 🟢⚪️", "price": 28200},
        {"name": "🆕🇷🇺 POCO X8 Pro Max 12/256 🔵", "price": 32700},
        {"name": "🆕🇷🇺 POCO X8 Pro Max 12/512 🔵", "price": 35200},
        {"name": "━━━ POCO F серия ━━━", "price": 0},
        {"name": "🇷🇺 POCO F6 Pro 12/512 ⚫️", "price": 26600},
        {"name": "🇪🇺 POCO F8 Pro 12/256 ⚫️", "price": 38100},
        {"name": "🇪🇺 POCO F8 Pro 12/512 🔵⚪️", "price": 40600},
        {"name": "🇪🇺 POCO F8 Ultra 12/256 ⚫️", "price": 50700},
        {"name": "🇪🇺 POCO F8 Ultra 16/512 ⚫️🔵", "price": 56700},
        {"name": "━━━ POCO Планшеты ━━━", "price": 0},
        {"name": "🔥🇪🇺 POCO Pad M1 8/256 ⚫️", "price": 18000},
        {"name": "🔥🇪🇺 POCO Pad X1 8/512 ⚫️", "price": 25000},
    ]},
   "honor": {"name": "🏅 Honor / Huawei", "items": [
        {"name": "━━━ HONOR ━━━", "price": 0},
        {"name": "🔥🇷🇺 HONOR X9d 12/256 ⚪️", "price": 23000},
        {"name": "🔥🇪 HONOR 400 Smart 8/256 ⚫️", "price": 14500},
        {"name": "🔥🇪🇺 HONOR 400 8/512 ⚫️🟡", "price": 27500},
        {"name": "🔥🇷 HONOR 600 Lite 8/256 ⚫️⚙️🟡", "price": 19000},
        {"name": "🔥🇷🇺 HONOR 600 8/256 ⚫️⚪️🟠", "price": 30500},
        {"name": "━━━ HONOR Magic ━━━", "price": 0},
        {"name": "🔥🇪 HONOR Magic 7 Pro 12/512 ⚫️", "price": 56500},
        {"name": "🔥🇪🇺 HONOR Magic 8 Lite 8/256 ⚫️🟢", "price": 25000},
        {"name": "🔥🇪🇺 HONOR Magic 8 Lite 8/512 ⚫️", "price": 26500},
        {"name": "🔥🇪 HONOR Magic 8 Pro 12/512 ⚫️🟡❄️🟢", "price": 69500},
        {"name": "🔥🇪 HONOR Magic 8 Pro 16/1TB ⚫️🟡", "price": 77000},
        {"name": "🔥🇪🇺 HONOR Magic V3 12/512 ⚫️🤎💚", "price": 73500},
        {"name": "━━━ Huawei ━━━", "price": 0},
        {"name": "🇷🇺 Huawei Pura 80 12/256 ⚫️🟡", "price": 33500},
        {"name": "🇷🇺 Huawei Pura 80 Pro 12/512 ⚫️", "price": 47500},
        {"name": "🇷🇺 Huawei Mate 70 Pro 12/512 ⚫️🟢", "price": 48000},
        {"name": "🇷🇺🇪🇺 Huawei Mate 80 Pro 16/512 🟢🟡", "price": 62500},
        {"name": "🇷🇺 Huawei Mate X6 12/512 🔴", "price": 78000},
        {"name": "🇷🇺 Huawei Mate X7 16/512 🔴", "price": 94000},
        {"name": "━━━ HONOR Планшеты ━━━", "price": 0},
        {"name": "🔥🇪🇺 HONOR Pad X8b Wi-Fi 4/64 ⚫️", "price": 11000},
        {"name": "🔥🇪🇺 HONOR Pad X8b Wi-Fi 4/128 ⚫️", "price": 13500},
        {"name": "🔥🇪🇺 HONOR Pad X8b Wi-Fi 6/256 ⚫️", "price": 15000},
        {"name": "🔥🇪🇺 HONOR Magic Pad 4 Wi-Fi 16/512 ⚫️", "price": 59000},
        {"name": "━━━ Huawei Планшеты ━━━", "price": 0},
        {"name": "🔥🇷🇺 Huawei Mate Pad SE 11 4/128 Wi-Fi ⚫️", "price": 10000},
        {"name": "🔥🇷🇺 Huawei Mate Pad 11.5 8/128 ⚙️", "price": 20000},
        {"name": "🔥🇷🇺 Huawei Mate Pad 11.5 8/256 Wi-Fi ⚫️", "price": 21500},
        {"name": "🔥🇷🇺 Huawei Mate Pad 11.5 8/256 Wi-Fi ⚫️🟣", "price": 24000},
        {"name": "🔥🇷 Huawei Mate Pad 11.5S 12/256 ⚫️", "price": 31000},
        {"name": "━━━ Huawei Watch ━━━", "price": 0},
        {"name": "⌚️🇪🇺 Huawei Watch Band 10 💖", "price": 3000},
        {"name": "⌚️🇪🇺 Huawei Watch GT5 Pro 46 ⚫️", "price": 13000},
        {"name": "⌚️🇷 Huawei Watch GT6 46 ⚫️🟢", "price": 13500},
    ]},
    "pixel": {"name": "📸 Google Pixel", "items": [
        {"name": "━━━ Pixel 6 ━━━", "price": 0},
        {"name": "🔥🇨🇦 Pixel 6a 6/128 🟢", "price": 16500},
        {"name": "━━━ Pixel 9 ━━━", "price": 0},
        {"name": "🔥🇯 Pixel 9a 8/128 ⚫️", "price": 29600},
        {"name": "🔥🇬🇧 Pixel 9a 8/256 ⚫️", "price": 31000},
        {"name": "━━━ Pixel 10 ━━━", "price": 0},
        {"name": "🔥🇮🇳 Pixel 10a 8/256 ⚫️🟣🟢", "price": 35700},
        {"name": "🔥🇬🇧 Pixel 10 12/128 🩵", "price": 44500},
        {"name": "🔥🇮🇳 Pixel 10 12/256 ⚫️🩵🔵", "price": 46500},
        {"name": "🔥🇨🇦 Pixel 10 Pro XL 16/256 ⚪️🟢", "price": 66500},
        {"name": "━━━ Pixel Watch ━━━", "price": 0},
        {"name": "🔥⌚️ Pixel Watch 4 41 🟠", "price": 22800},
        {"name": "🔥⌚️ Pixel Watch 4 46 ⚫️", "price": 26800},
        {"name": "━━━ Аксессуары ━━━", "price": 0},
        {"name": "🔌 Adapter Google Pixel 30W", "price": 1200},
    ]},
    "oneplus": {"name": "🟢 OnePlus", "items": [
        {"name": "━━━ OnePlus Смартфоны ━━━", "price": 0},
        {"name": "🇪🇺 OnePlus 13s 12/256 💖", "price": 36500},
        {"name": "🇪🇺 OnePlus 13s 12/512 ⚫️🟢", "price": 39500},
        {"name": "🇪🇺 OnePlus 13 16/512 ⚪️", "price": 50000},
        {"name": "🇪🇺 OnePlus Nord 5 12/512 🩶", "price": 29500},
        {"name": "🇪🇺 OnePlus Nord 6 12/512 🟢", "price": 37000},
        {"name": "━━━ OnePlus Планшеты ━━━", "price": 0},
        {"name": "🇪 OnePlus Pad Go2 8/256 ⚫️", "price": 25500},
        {"name": "🇪🇺 OnePlus Pad 2 16/512 Wi-Fi ⚫️🟢", "price": 34000},
        {"name": "🇪🇺 OnePlus Pad 4 12/256 Wi-Fi 🟢", "price": 45500},
        {"name": "🇪🇺 OnePlus Pad 4 12/512 Wi-Fi 🤎💚", "price": 52500},
        {"name": "━━━ OnePlus Наушники ━━━", "price": 0},
        {"name": "🇪🇺🎧 OnePlus Buds Nord 4 Pro ⚫️⚙️", "price": 3500},
        {"name": "🇪🇺🎧 OnePlus Buds 4 🟢", "price": 5500},
        {"name": "🇪🇺🎧 OnePlus Buds 3 Pro ⚫️", "price": 9000},
        {"name": "━━━ OnePlus Watch ━━━", "price": 0},
        {"name": "🔥⌚️ OnePlus Watch 3 43 Silver Steel", "price": 15600},
    ]},
   "realme": {"name": "🍋 Realme", "items": [
        {"name": "━━━ Realme C серия ━━━", "price": 0},
        {"name": "🍋🇷🇺 Realme C100i 4/128 ⚫️🟣", "price": 12000},
        {"name": "🍋🇷🇺 Realme C100X 4/256 🔵⚪️", "price": 13500},
        {"name": "━━━ Realme P серия ━━━", "price": 0},
        {"name": "🍋🇷🇺 Realme P3 Ultra 12/512 🔵", "price": 28000},
        {"name": "🍋🇷🇺 Realme 16 Pro+ 5G 12/512 ⚫️🟡", "price": 39000},
        {"name": "━━━ Realme GT серия ━━━", "price": 0},
        {"name": "🍋🇷🇺 Realme GT7T 12/512 ⚫️🔵", "price": 34000},
        {"name": "🍋🇷🇺 Realme GT8 Pro 12/256 🔵⚪️", "price": 58000},
    ]},
    "dyson": {"name": "♥️ Dyson & Dreame", "items": [
        {"name": "━━━ Dyson Фены ━━━", "price": 0},
        {"name": "🇬🇧 Dyson HT01 Ceramic Apricot/topaz", "price": 27000},
        {"name": "🇰🇷 Dyson HD18 Pro Vinca Blue/topaz", "price": 30500},
        {"name": "━━━ Dyson Стайлеры ━━━", "price": 0},
        {"name": "🇭🇰 Dyson Long HS08 Vinca Blue/topaz", "price": 28500},
        {"name": "🇭🇰 Dyson HS09 Jasper Plum", "price": 41000},
        {"name": "🇪🇺 Dyson HS09 Apricot Topaz", "price": 42000},
        {"name": "🇪 Dyson HS09 Red Velvet", "price": 42500},
        {"name": "━━━ Dyson Пылесосы ━━━", "price": 0},
        {"name": "🇪🇺🏠 Dyson V12s SV46 Моющий", "price": 40000},
        {"name": "🇪🇺🏠 Dyson Pencil Wash WR04 Моющий", "price": 35000},
        {"name": "🇬🇧🏠 Dyson V16 DS60", "price": 53500},
        {"name": "🇪🇺🏠 Dyson V16s SV53A Submarine Моющий", "price": 66500},
        {"name": "━━━ Dyson Очистители ━━━", "price": 0},
        {"name": "🇪🇺🔥 Dyson SP01 Очиститель воздуха ⚫️", "price": 34000},
        {"name": "🇪🇺🔥 Очиститель+Увлажнитель PH05", "price": 57000},
        {"name": "━━━ Dreame Стайлеры ━━━", "price": 0},
        {"name": "🆕🔥 Dreame AirStyle AMF17A 🟠", "price": 11500},
        {"name": "🆕🔥 Dreame AirStyle Pro AMF18A 🟠", "price": 16500},
        {"name": "🆕🔥 Dreame Aero Straight AMA10A", "price": 16000},
        {"name": "━━━ Dreame Пылесосы ━━━", "price": 0},
        {"name": "🇷🇺🏠 Dreame G10 Pro Моющий", "price": 15500},
        {"name": "🇷🇺🏠 Dreame V12 Pro Вертикальный", "price": 19500},
        {"name": "🇷🇺🏠 Dreame R20 Вертикальный", "price": 20000},
        {"name": "🇷🇺🏠 Dreame H12 Dual Моющий", "price": 27300},
        {"name": "🇷🇺🏠 Dreame H14 Dual Моющий", "price": 35700},
        {"name": "🇷🇺🏠 Dreame H15 Pro Heat Моющий", "price": 40000},
        {"name": "━━━ Dreame Роботы ━━━", "price": 0},
        {"name": "🇷🇺🏠 Dreame Робот F10 ⚪️", "price": 12000},
        {"name": "🇷🇺🏠 Dreame L40s Ultra ⚪️", "price": 51000},
        {"name": "🇪🇺🏠 Dreame X50 Master ⚫️", "price": 76000},
        {"name": "🇪🇺🏠 Dreame X50 Ultra Complete ⚫️", "price": 77000},
        {"name": "🇷🇺🏠 Dreame X60 Ultra Complete ⚫️", "price": 97500},
    ]},
    "vacuum": {"name": "🏠 Пылесосы", "items": [
        {"name": "━━━ Вертикальные ━━━", "price": 0},
        {"name": "🇷🇺🏠 Red Solution V3060 250Вт", "price": 9500},
        {"name": "🇷🇺🏠 Roborock Flexi Моющий ⚪️", "price": 17000},
        {"name": "🇷🇺🏠 Roborock F25 LT Моющий ⚫️", "price": 20000},
        {"name": "🇷🇺🏠 Roborock F25 ALT Моющий ⚫️", "price": 22000},
        {"name": "🇷🇺🏠 Roborock F25 Combo Моющий ⚫️", "price": 30000},
        {"name": "🇷🇺🏠 Roborock F25 Ace Pro", "price": 33000},
        {"name": "🇷🇺🏠 Roborock F25 Ultra", "price": 39000},
        {"name": "━━━ Roborock Роботы Q серия ━━━", "price": 0},
        {"name": "🇷🇺🏠 Roborock Q8 Plus ⚪️", "price": 15500},
        {"name": "🇷🇺🏠 Roborock Q8 Max Pro ⚪️", "price": 13000},
        {"name": "🇷🇺🏠 Roborock Q8 Max Pro Gen2 ⚪️⚫️", "price": 17000},
        {"name": "🇷🇺🏠 Roborock Q8 Max Pro Plus ⚫️⚪️", "price": 18000},
        {"name": "🇷🇺🏠 Roborock Q10 PF ⚪️", "price": 12000},
        {"name": "🇷🇺🏠 Roborock Q10 VF ⚫️⚪️", "price": 13000},
        {"name": "━━━ Roborock Роботы S серия ━━━", "price": 0},
        {"name": "🇷🇺🏠 Roborock S8 ⚫️", "price": 11000},
        {"name": "🇷🇺🏠 Roborock S8 Pro ⚫️⚪️", "price": 15000},
        {"name": "🇷🇺🏠 Roborock S8 Pro Plus ⚫️⚪️", "price": 20000},
        {"name": "🇷🇺🏠 Roborock S9 Max V Ultra ⚪️", "price": 89500},
        {"name": "━━━ Roborock Роботы Q Revo ━━━", "price": 0},
        {"name": "🇷🇺🏠 Roborock Q Revo S ⚪️", "price": 27000},
        {"name": "🇷🇺🏠 Roborock QV 35A ⚪️", "price": 31000},
        {"name": "🇷🇺🏠 Roborock Q Revo L ⚪️", "price": 33500},
        {"name": "🇷🇺🏠 Roborock Q Revo C ⚫️⚪️", "price": 35500},
        {"name": "🇷🇺🏠 Roborock Q Revo C Pro ⚫️", "price": 44000},
        {"name": "🇷🇺🏠 Roborock Q Revo Edge T ⚪️", "price": 62000},
        {"name": "🇷🇺🏠 Roborock Saros Z70 ⚪️", "price": 93000},
    ]},
   "laptops": {"name": "💻 Ноутбуки", "items": [
        {"name": "━━━ Игровые консоли ━━━", "price": 0},
        {"name": "❗️🇪🇺 Asus ROG Xbox Ally Z2 A 16/512", "price": 42500},
        {"name": "━━━ Обычные ноутбуки ━━━", "price": 0},
        {"name": "💻🇷🇺 Гравитон Н15И 15.6 i5/8/256", "price": 30000},
        {"name": "💻🇷🇺 Asus VivoBook 17.3 AU982 i5/16/512", "price": 55000},
        {"name": "💻🇷🇺 Asus VivoBook 17.3 AU1017 i5/16/512", "price": 56000},
        {"name": "💻🇷🇺 HP ProBook 440 G8 14 i7/8/512 ⚪️", "price": 41000},
        {"name": "💻🇷🇺 Lenovo IdeaPad 3 Slim 15.6 i3/8/256", "price": 32500},
        {"name": "💻🇷🇺 Machcreator One D5 15.6 R5/16/512", "price": 37500},
        {"name": "━━━ Игровые ноутбуки ━━━", "price": 0},
        {"name": "💻🇷🇺 Acer Nitro V15 i5/16/512 RTX5050", "price": 74000},
        {"name": "💻🇷🇺 Asus TUF Gaming F16 i5/16/1TB RTX5050", "price": 90000},
        {"name": "💻🇷🇺 Asus TUF Gaming F16 i5/16/1TB RTX5060", "price": 100000},
        {"name": "💻🇷🇺 Asus TUF A18 R7/32/1TB RTX5060", "price": 129000},
        {"name": "💻🇷🇺 Asus ROG Strix G18 Ultra7/32/2TB RTX5070", "price": 175000},
        {"name": "💻🇷🇺 Gigabyte Gaming A16 R7/16/1TB RTX5060", "price": 103000},
        {"name": "💻🇷🇺 Lenovo Legion Pro 5 16 Ultra7/16/1TB RTX5060", "price": 115000},
        {"name": "💻🇷🇺 MSI Katana 17 i5/16/1TB RTX4050", "price": 72000},
        {"name": "💻🇷🇺 MSI Katana 15.6 i7/16/1TB RTX5070", "price": 100000},
        {"name": "💻🇷🇺 MSI Vector 16 Ultra9/32/2TB RTX5070", "price": 157500},
        {"name": "💻🇷🇺 MSI Raider 18 Ultra9/32/1TB RTX5070", "price": 170000},
        {"name": "💻🇷🇺 MSI Titan 18 Ultra9/64/4TB RTX5080", "price": 260000},
        {"name": "💻🇷🇺 Samsung Book 6 Ultra 16 Ultra7/32/1TB RTX5070", "price": 250000},
    ]},
   "cameras": {"name": "📹 Камеры / DJI", "items": [
        {"name": "━━━ Insta360 ━━━", "price": 0},
        {"name": "🇪🇺📹 Insta 360 Go 3S 4K 128GB ⚫️⚪️", "price": 22000},
        {"name": "🇪🇺📹 Insta 360 X4 8K", "price": 26500},
        {"name": "🇪🇺📹 Insta 360 Ace Pro 2 Dual Battery", "price": 30500},
        {"name": "🇪🇺📹 Insta 360 Go Ultra ⚫️⚪️", "price": 30000},
        {"name": "🇪🇺📹 Insta 360 Go Ultra Creator Bundle", "price": 35000},
        {"name": "━━━ DJI ━━━", "price": 0},
        {"name": "🇪🇺 DJI MIC 3 Microphone 2TX+1RX", "price": 21000},
        {"name": "🇪🇺📹 DJI Osmo 360 Standard Combo", "price": 28000},
        {"name": "🇪🇺📹 DJI Osmo Pocket 3", "price": 29000},
        {"name": "🇪🇺📹 DJI Osmo Action 5 Pro Adventure Combo", "price": 30200},
        {"name": "🇪🇺 DJI Osmo Mobile 7 Стабилизатор", "price": 5400},
    ]},
    "garmin": {"name": "⌚️ Garmin", "items": [
        {"name": "🇪🇺⌚️ GARMIN Forerunner 570 47 ⚫️", "price": 39000},
        {"name": "🇪🇺⌚️ GARMIN Instinct Crossover Amoled 47 ⚫️", "price": 42000},
    ]},
    "gaming": {"name": "🎮 Sony PS5", "items": [
        {"name": "🇪🇺 Sony PS5 Digital 1TB 2 ревизия", "price": 41500},
        {"name": "🔥 Дисковод на Sony PS5", "price": 7900},
        {"name": "🇪🇺 Sony PS5 Джойстик 💙🩵💜🤍", "price": 5300},
    ]},
    "speakers": {"name": "🎼 Колонки / Наушники", "items": [
        {"name": "━━━ Умные колонки ━━━", "price": 0},
        {"name": "🇷🇺🎼 SberBoom Mini ⚪️", "price": 1800},
        {"name": "🇷🇺🎼 SberBoom 40Вт ⚫️", "price": 5500},
        {"name": "🇷🇺🎼 VK Капсула Мини с Марусей ⚫️", "price": 2200},
        {"name": "🇷🇺🎼 Яндекс Станция Мини 3 ⚫️⚙🟣", "price": 7200},
        {"name": "🇷🇺🎼 Яндекс Станция Миди 🟠", "price": 11000},
        {"name": "🇷🇺🎼 Яндекс Станция 3 ⚫️", "price": 18000},
        {"name": "🇷🇺🎼 Яндекс Станция Макс Дуо ⚫️🟢🔴", "price": 33200},
        {"name": "━━━ JBL Колонки ━━━", "price": 0},
        {"name": "🇪🇺🎼 JBL Xtreme 4 🔵", "price": 18200},
        {"name": "🇪🇺🎼 JBL Boombox 3 Camouflage", "price": 25000},
        {"name": "🇪🇺🎼 JBL PartyBox 130", "price": 30300},
        {"name": "🇪🇺🎼 JBL PartyBox 320", "price": 36300},
        {"name": "━━━ Наушники ━━━", "price": 0},
        {"name": "🇪🇺🎧 Sennheiser Momentum 4 ⚫️🔵⚪️⚙️", "price": 14900},
        {"name": "🇪🇺🎧 Marshall Major 5 🤎⚪️🔵", "price": 5500},
        {"name": "🇪🇺🎧 Marshall Minor 4 ⚫️", "price": 8000},
        {"name": "🇪🇺🎧 JBL Tune 520 BT ⚫️", "price": 2500},
        {"name": "🇪🇺🎧 Sony WH-1000XM6 ⚪️", "price": 25000},
    ]},
    "rugged": {"name": "💦🔨 Противоударные / Влагозащищённые", "items": [
        {"name": "━━━ Unihertz ━━━", "price": 0},
        {"name": "🇪🇺💦 Unihertz Tank 3 16/512GB", "price": 33000},
        {"name": "🇪🇺💦 Unihertz Tank 3 Pro 16/512GB Проектор", "price": 41500},
        {"name": "━━━ Blackview BV ━━━", "price": 0},
        {"name": "🇪🇺💦 BV 6200 Plus 8/128GB 🟢", "price": 11500},
        {"name": "🇪🇺💦 BV BL7000 8/256GB ⚫️", "price": 16900},
        {"name": "🇪🇺💦 BL 9000 Pro 12/512GB Тепловизор ⚫️", "price": 34500},
        {"name": "━━━ DOOGEE ━━━", "price": 0},
        {"name": "🇪💦 DOOGEE Fire 7 Pro 8/256GB ⚫️", "price": 19300},
        {"name": "🇪🇺💦 DOOGEE Fire 7 Ultra 8/256GB ⚫️", "price": 20300},
        {"name": "🇪🇺💦 DOOGEE V Max Plus 16/512GB ⚙️", "price": 28800},
        {"name": "🇪🇺💦 DOOGEE V Max LR 16/512GB ⚫️", "price": 34000},
        {"name": "🇪🇺💦 DOOGEE S200 VIP 12/256GB", "price": 23500},
        {"name": "🇪🇺💦 DOOGEE S300 Plus 12/1TB", "price": 35000},
        {"name": "🇪🇺💦 DOOGEE S300 Pro 16/512GB", "price": 32500},
        {"name": "━━━ Oukitel ━━━", "price": 0},
        {"name": "🇪🇺💦 Oukitel WP35 Pro 12/512GB 🟢", "price": 18000},
        {"name": "🇪🇺💦 Oukitel WP58 Pro 8/512GB ⚫️", "price": 17300},
        {"name": "🇪🇺💦 Oukitel WP62 16/512GB ⚫️", "price": 21000},
        {"name": "🇪🇺💦 Oukitel WP200 Pro 24/1TB ⚫️🟢", "price": 35000},
        {"name": "🇪🇺💦 Oukitel WP210 12/512GB ⚫", "price": 22800},
        {"name": "🇪🇺💦 Oukitel WP300 12/512GB ⚫️", "price": 25000},
        {"name": "━━━ Ulefone ━━━", "price": 0},
        {"name": "🇪🇺💦 Ulefone Armor 25T Pro 6/256GB Тепловизор ⚫️", "price": 24500},
        {"name": "🇪🇺💦 Ulefone Power Armor 27 Pro 12/256GB Тепловизор", "price": 25800},
        {"name": "🇪🇺💦 Ulefone Power Armor 27T Plus 12/256GB Тепловизор", "price": 25800},
        {"name": "🇪🇺💦 Ulefone Armor 29 Pro 16/512GB Тепловизор ⚫️", "price": 34000},
        {"name": "🇪🇺💦 Ulefone Armor 30 Pro 16/512GB", "price": 29000},
    ]},
    "accessories": {"name": "🔆 Аксессуары", "items": [
        {"name": "━━━ Чехлы ━━━", "price": 0},
        {"name": "🔆 Чехол Pitaka 14 Plus", "price": 3200},
        {"name": "🔆 Чехол Pitaka 15 Pro", "price": 4800},
        {"name": "━━━ Apple Аксессуары ━━━", "price": 0},
        {"name": "⚡️ Battery Pack Apple", "price": 1760},
        {"name": "💫 MagSafe Original", "price": 2560},
        {"name": "🇪🇺 Apple Adapter USB-C 20W", "price": 2240},
        {"name": "🇪🇺 Apple Adapter USB-C 35W", "price": 2560},
        {"name": "🇪🇺 Apple Adapter USB-C 40W", "price": 2720},
        {"name": "🇪🇺 СЗУ Apple Watch USB/USB-C", "price": 3200},
        {"name": "━━━ СЗУ MacBook ━━━", "price": 0},
        {"name": "🇪🇺 СЗУ MacBook 67W USB-C", "price": 3200},
        {"name": "🇪🇺 СЗУ MacBook 87W USB-C", "price": 3520},
        {"name": "🇪 СЗУ MacBook 96W USB-C", "price": 3840},
        {"name": "🇪🇺 СЗУ MacBook 140W USB-C", "price": 5920},
        {"name": "━━━ Samsung Аксессуары ━━━", "price": 0},
        {"name": "🇪🇺 Samsung СЗУ 25W ⚫️⚪️", "price": 1760},
        {"name": "🇪🇺 Samsung СЗУ 45W ⚫️⚪️", "price": 1920},
        {"name": "🇪🇺 Samsung СЗУ 60W ⚫️", "price": 2560},
        {"name": "🇪🇺 Samsung СЗУ 65W Trio ⚫️", "price": 3040},
        {"name": "🇪🇺 Samsung АЗУ 45W", "price": 1280},
        {"name": "━━━ Другое ━━━", "price": 0},
        {"name": "🔥 Amazon Kindle 7 32GB 12gen", "price": 23200},
    ]},
}
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def get_price(base_price: int, category: str = "iphone") -> int:
    markup = MARKUP.get(category, 0.10)
    return round(base_price * (1 + markup) / 100) * 100

def parse_price_line(line: str):
    line = line.strip()
    if not line:
        return None
    price_match = re.search(r'-(\d{4,6})', line)
    if not price_match:
        return None
    price = int(price_match.group(1))
    if price < 1000:
        return None
    name = line[:price_match.start()].strip()
    if not name:
        return None
    return name, price

def detect_category(line: str):
    if any(x in line for x in ['Nitro', 'VivoBook', 'ZenBook', 'TUF', 'ROG', 'Legion', 'Katana', 'Vector', 'Titan', 'MateBook', 'ProBook', 'IdeaPad', 'Гравитон', 'Gigabyte', 'Machcreator', 'Raider', 'Samsung Book', 'Book 6']):
        return 'laptops'
    if any(x in line for x in ['HONOR', 'Huawei']):
        return 'honor'
    if any(x in line for x in ['Galaxy Buds', 'Watch Fit', 'Samsung Watch']):
        return 'samsung_watch'
    if 'Watch 8' in line and 'Huawei' not in line:
        return 'samsung_watch'
    if 'Watch 7' in line and 'Huawei' not in line and 'Pixel' not in line:
        return 'samsung_watch'
    if any(x in line for x in ['MacBook', 'Mac Mini', 'MacMini', 'MU9D3', 'MU9E3', 'MCYT4', 'MHFF4', 'MC6A4', 'MDHF4', 'MDVH4', 'MJLW4', 'MGDT4', 'MGDU4', 'MGED4']):
        return 'macbook'
    if any(x in line for x in ['iPhone', 'iphone', '🍎']):
        if not any(x in line for x in ['iPad', 'ipad']):
            return 'iphone' 
    if any(x in line for x in ['iPad', 'ipad']):
        return 'ipad'
    if 'AirPods' in line:
        return 'airpods'
    if any(x in line for x in ['Watch SE', 'Watch S1', 'Watch Ultra', 'Watch S10', 'Watch S11', 'Se 2 ', 'Se 3 ', 'S10 4', 'S11 4', 'Ultra 3 4', 'Ultra 2 4']):
        return 'watch'
    if any(x in line for x in ['Samsung', 'A07', 'A26', 'A36', 'A37', 'A56', 'A57', 'S25', 'S26', 'Z Flip', 'Z Fold', 'Galaxy', 'Tab S']):
        return 'samsung'
    if 'POCO' in line:
        return 'poco'
    if any(x in line for x in ['Xiaomi', 'Redmi', 'Mi Pad', 'Mi 15', 'Mi 17', 'Note 14', 'Note 15']):
        return 'xiaomi'
    if 'Pixel' in line:
        return 'pixel'
    if 'OnePlus' in line:
        return 'oneplus'
    if 'Realme' in line:
        return 'realme'
    if any(x in line for x in ['Roborock', 'Vacuum', 'Red Solution']):
        return 'vacuum'
    if 'Робот' in line and 'Dreame' not in line:
        return 'vacuum'
    if any(x in line for x in ['Dyson', 'Dreame', 'HT01', 'HD18', 'HS08', 'HS09']):
        return 'dyson'
    if any(x in line for x in ['Insta', 'DJI', 'Osmo']):
        return 'cameras'
    if 'GARMIN' in line:
        return 'garmin'
    if any(x in line for x in ['PS5', 'Джойстик', 'Дисковод']):
        return 'gaming'
    if any(x in line for x in ['JBL', 'Станция', 'SberBoom', 'Marshall', 'Sennheiser', 'Sony WH', 'Momentum', 'Капсула']):
        return 'speakers'
    if any(x in line for x in ['Unihertz', 'DOOGEE', 'Oukitel', 'Ulefone', 'BV BL', 'Tank 3']):
        return 'rugged'
    return None
    
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("💬 Менеджер", url=ORDER_URL)],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ])
def catalog_keyboard():
    kb = [
        [InlineKeyboardButton("💻 MacBook", callback_data="cat_macbook"), InlineKeyboardButton("📟 iPad", callback_data="cat_ipad")],
        [InlineKeyboardButton("⌚️ Apple Watch", callback_data="cat_watch"), InlineKeyboardButton("🎧 AirPods", callback_data="cat_airpods")],
        [InlineKeyboardButton("⌚️ Samsung Watch & Buds", callback_data="cat_samsung_watch"), InlineKeyboardButton("📸 Pixel", callback_data="cat_pixel")],
        [InlineKeyboardButton("🟢 OnePlus", callback_data="cat_oneplus"), InlineKeyboardButton("🍋 Realme", callback_data="cat_realme")],
        [InlineKeyboardButton("🍎 iPhone", callback_data="cat_iphone")],
        [InlineKeyboardButton("📱 Samsung", callback_data="cat_samsung")],
        [InlineKeyboardButton("🔥 Xiaomi", callback_data="cat_xiaomi")],
        [InlineKeyboardButton("🔥 POCO", callback_data="cat_poco")],
        [InlineKeyboardButton("🏅 Honor / Huawei", callback_data="cat_honor")],
        [InlineKeyboardButton("♥️ Dyson & Dreame", callback_data="cat_dyson"), InlineKeyboardButton("🏠 Пылесосы", callback_data="cat_vacuum")],
        [InlineKeyboardButton("💻 Ноутбуки", callback_data="cat_laptops"), InlineKeyboardButton("📹 Камеры", callback_data="cat_cameras")],
        [InlineKeyboardButton("⌚️ Garmin", callback_data="cat_garmin"), InlineKeyboardButton("🎮 PS5", callback_data="cat_gaming")],
        [InlineKeyboardButton("🎼 Колонки", callback_data="cat_speakers"), InlineKeyboardButton("💦 Защищённые", callback_data="cat_rugged")],
        [InlineKeyboardButton("🔆 Аксессуары", callback_data="cat_accessories")],
        [InlineKeyboardButton("🏠 Главная", callback_data="home")],
    ]
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "👋 Добро пожаловать в *Plata*!\n\nОригинальная техника по лучшим ценам 🔥\n\n📱💻🖥⌚️🎧🖱⌨️🎮\n\n📍 Москва, ТК Митинский Радиорынок, пав. 450\n🚚 Доставка по всей России\n✅ Гарантия на все товары\n\nВыберите раздел:"
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
        if item['price'] == 0:
            lines.append(f"\n{item['name']}")
        else:
            price_str = f"{get_price(item['price'], cat_key):,}".replace(",", " ")
            lines.append(f"• {item['name']}\n   💰 {price_str} ₽")
    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:4000] + "\n\n_...уточняйте у менеджера!_"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Заказать", url=ORDER_URL)],
        [InlineKeyboardButton("◀️ Назад", callback_data="catalog")],
    ])
    await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = "🏪 *Plata — оригинальная техника*\n\nМы помогаем выбрать и купить технику, которой можно доверять. Только оригинальные устройства, честные цены и живая консультация.\n\n✅ Гарантия на все товары\n🚚 Доставка по всей России\n\n📍 Москва, Пятницкое шоссе д.18\nТК Митинский Радиорынок\n0 вход, 1 этаж, павильон 450\n\n🕗 Самовывоз: 9:00 — 18:00\n✍️ Заказы: 9:00 — 20:00\n⏰ Без выходных\n\n🆘 помощь: @plata\\_mgr"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Менеджер", url=ORDER_URL)],
        [InlineKeyboardButton("🏠 Главная", callback_data="home")],
    ])
    await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")
price_buffer = {}

async def handle_price_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        return
    text = update.message.text or update.message.caption or ""

    if text.strip() == '/done':
        if not price_buffer:
            await update.message.reply_text("⚠️ Буфер пустой — сначала скинь прайс")
            return

        for category in CATALOG:
            CATALOG[category]["items"] = [
                item for item in CATALOG[category]["items"]
                if item["price"] == 0
            ]

        updated = []
        for category, items in price_buffer.items():
            if category in CATALOG:
                markup = MARKUP.get(category, 0.10)
                for new_item in items:
                    base_price = round(new_item["price"] / (1 + markup) / 100) * 100
                    new_name = new_item["name"]
                    cat_items = CATALOG[category]["items"]
                    
                    # Найти подходящий разделитель
                    best_sep_idx = None
                    name_lower = new_name.lower()
                    sep_keywords = {
                        "macbook": [("mac mini", ["mac mini","macmini","mu9d3","mu9e3","mcyt4"]), ("neo", ["neo 2026","mhff4","mhfg4","mhfa4","mhfd4","a18 pro"]), ("air 13", ["air 13"]), ("air 15", ["air 15"]), ("pro", ["pro 14","pro 16","mjlw4","mgdt4","mgdu4","mged4"])],
                        "watch": [("se", ["se 3","se 2","se 44","se 40"]), ("s10", ["s10","s11"]), ("ultra 3", ["ultra 3","black ocean","black ti black","black milanese"]), ("ultra 2", ["ultra 2","natural ti","black ti dark","milanese"])],
                        "samsung_watch": [("watch", ["watch fit","watch 7","watch 8","ultra"]), ("buds", ["buds"])],
                        "ipad": [("ipad 11", ["ipad 11"]), ("air", ["air"]), ("pro 11", ["pro 11"]), ("pro 13", ["pro 13"]), ("аксессуары", ["pencil","keyboard"])],
                        "airpods": [("earpods", ["earpods"]), ("airpods", ["airpods 4","airpods anc"]), ("airpods pro", ["airpods pro"]), ("airpods max", ["airpods max"])],
                        "xiaomi": [("note 14", ["note 14"]), ("note 15", ["note 15"]), ("mi 15", ["15t","mi 15"]), ("mi 17", ["17t","mi 17"]), ("планшет", ["pad","mi pad"]), ("другое", ["watch","робот","vacuum"])],
                        "poco": [("poco c", ["c85","c100"]), ("poco m", ["m8"]), ("poco x", ["x7","x8"]), ("poco f", ["f6","f8"]), ("планшет", ["poco pad"])],
                        "honor": [("honor", ["x9d","honor 400","honor 600"]), ("honor magic", ["magic 7","magic 8","magic v"]), ("huawei", ["pura","mate 70","mate 80","mate x6","mate x7"]), ("honor планшет", ["pad x8b","magic pad"]), ("huawei планшет", ["mate pad se","mate pad 11"]), ("huawei watch", ["watch band","watch gt"])],
                        "dyson": [("фен", ["ht01","hd18"]), ("стайлер", ["hs08","hs09","long hs"]), ("пылесос", ["v10 sv","v12s sv","v15s sv","v16 ds","pencil wash","sv50"]), ("очист", ["sp01","ph05"]), ("dreame стайлер", ["airstyle","aero straight"]), ("dreame пылесос", ["dreame g10","dreame v12","dreame r20","dreame h12","dreame h14","dreame h15"]), ("dreame робот", ["trouver","dreame d9","dreame l10","робот f10","dreame x50","dreame x60"])],
                        "vacuum": [("вертикальн", ["red solution","flexi","roborock f25","roborock f"]), ("q серия", ["q7","q8","q10"]), ("s серия", ["s8","s9"]), ("revo", ["revo","qv","saros"])],
                        "laptops": [("консол", ["ally","xbox"]), ("обычные", ["гравитон","vivobook","probook","ideapad","machcreator","hp probook"]), ("игровые", ["nitro","tuf gaming","rog strix","legion pro","katana","vector","titan","gigabyte","raider","msi","thunderobot","samsung book"])],
                        "pixel": [("pixel 6", ["6a","pixel 6"]), ("pixel 9", ["9a","pixel 9"]), ("pixel 10", ["10a","pixel 10"]), ("pixel watch", ["pixel watch"]), ("аксессуары", ["adapter","кабель"])],
                        "oneplus": [("смартфон", ["oneplus 13","oneplus nord"]), ("планшет", ["pad"]), ("наушник", ["buds"]), ("watch", ["watch"])],
                        "realme": [("realme c", ["c100"]), ("realme p", ["p3","16 pro"]), ("realme gt", ["gt7","gt8"])],
                        "speakers": [("умные", ["sber","яндекс","vk","капсула"]), ("jbl", ["jbl"]), ("наушник", ["sennheiser","marshall","sony wh","tune"])],
                        "rugged": [("unihertz", ["unihertz","tank"]), ("blackview", ["bv bl","bv 6200","bl 9000"]), ("doogee", ["doogee"]), ("oukitel", ["oukitel","wp"]), ("ulefone", ["ulefone","armor"])],
                        "cameras": [("insta360", ["insta","360"]), ("dji", ["dji","osmo","mic"])],
                    }
                    if category == "iphone":
                        for i, item in enumerate(cat_items):
                            if item["price"] == 0:
                                sep = item["name"].lower()
                                for num in ["17 pro max", "17 pro", "17 air", "17e", "17", "16 pro max", "16 pro", "16e", "16 plus", "16", "15 pro max", "15 pro", "15 plus", "15", "14 pro max", "14 pro", "14 plus", "14", "13 pro max", "13 pro", "13 mini", "13"]:
                                    if num in name_lower and num.split()[0] in sep:
                                        best_sep_idx = i
                                        break
                    elif category == "samsung":
                        for i, item in enumerate(cat_items):
                            if item["price"] == 0:
                                sep = item["name"].lower()
                                if any(x in name_lower for x in ["a07","a17","a26","a36","a37","a56","a57"]) and "a серия" in sep:
                                    best_sep_idx = i
                                elif any(x in name_lower for x in ["s25"]) and "s25" in sep:
                                    best_sep_idx = i
                                elif any(x in name_lower for x in ["s26"]) and "s26" in sep:
                                    best_sep_idx = i
                                elif any(x in name_lower for x in ["z flip"]) and "flip" in sep:
                                    best_sep_idx = i
                                elif any(x in name_lower for x in ["z fold"]) and "fold" in sep:
                                    best_sep_idx = i
                                elif any(x in name_lower for x in ["tab"]) and "tab" in sep:
                                    best_sep_idx = i
                    elif category in sep_keywords:
                        for i, item in enumerate(cat_items):
                            if item["price"] == 0:
                                sep = item["name"].lower()
                                for sep_key, name_keys in sep_keywords[category]:
                                    if sep_key in sep and any(k in name_lower for k in name_keys):
                                        best_sep_idx = i
                                        break
                                if best_sep_idx is not None:
                                    break

                    if best_sep_idx is None and category not in ["iphone", "samsung"]:
                        cat_items.append({"name": new_name, "price": base_price})
                        continue
                        
                    # Вставить после разделителя
                    if best_sep_idx is not None:
                        # Найти позицию после разделителя (перед следующим разделителем)
                        insert_idx = best_sep_idx + 1
                        while insert_idx < len(cat_items) and cat_items[insert_idx]["price"] != 0:
                            insert_idx += 1
                        cat_items.insert(insert_idx, {"name": new_name, "price": base_price})
                    else:
                        cat_items.append({"name": new_name, "price": base_price})
                
                updated.append(f"{CATALOG[category]['name']} — {len(items)} позиций")

        price_buffer.clear()
        report = "\n".join(updated)
        await update.message.reply_text(f"✅ *Цены обновлены!*\n\n{report}", parse_mode="Markdown")
        return

    if len(text) < 50:
        return

    count = 0
    for line in text.split('\n'):
        parsed = parse_price_line(line)
        if not parsed:
            continue
        name, price = parsed
        category = detect_category(line)
        if category:
            if category not in price_buffer:
                price_buffer[category] = []
            price_buffer[category].append({"name": name, "price": price})
            count += 1

    if count > 0:
        await update.message.reply_text(f"➕ Добавлено {count} позиций в буфер. Скидывай следующую часть или напиши /done чтобы сохранить.")

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = update.callback_query.data
    if d == "home": await start(update, context)
    elif d == "catalog": await catalog_handler(update, context)
    elif d.startswith("cat_"): await category_handler(update, context)
    elif d == "about": await about_handler(update, context)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("done", handle_price_update))
app.add_handler(CallbackQueryHandler(router))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price_update))
print("Bot started!")
app.run_polling()
