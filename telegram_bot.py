"""
Telegram Bot - Welcome + Language Selection + Services + Contact Us
Requirements: pip install python-telegram-bot==20.7
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ─────────────────────────────────────────────
# 🔑  توکن ربات خودت رو اینجا بذار
BOT_TOKEN = "8406682179:AAF0EU8Ve-wszntir5LdUa1iCNkJ0LXWvcU"

# ─────────────────────────────────────────────
# 📞  اطلاعات ارتباط با ما
CONTACT_FA = (
    "📞 *ارتباط با ما*\n\n"
    "👤 ادمین: @your\\_admin\n"
    "📧 ایمیل: support@example.com\n"
    "🌐 وبسایت: example.com"
)
CONTACT_EN = (
    "📞 *Contact Us*\n\n"
    "👤 Admin: @your\\_admin\n"
    "📧 Email: support@example.com\n"
    "🌐 Website: example.com"
)

# ─────────────────────────────────────────────
# خدمات - هر آیتم: (نام فارسی، نام انگلیسی، توضیح فارسی، توضیح انگلیسی)
SERVICES = [
    (
        "💻 طراحی وبسایت",
        "💻 Web Design",
        "طراحی سایت حرفه‌ای با بهترین قیمت و کیفیت بالا.",
        "Professional website design at the best price and quality.",
    ),
    (
        "📱 اپلیکیشن موبایل",
        "📱 Mobile App",
        "توسعه اپلیکیشن Android و iOS برای کسب‌وکار شما.",
        "Android & iOS app development for your business.",
    ),
    (
        "🤖 ربات تلگرام",
        "🤖 Telegram Bot",
        "ساخت ربات‌های هوشمند تلگرام با امکانات دلخواه.",
        "Building smart Telegram bots with custom features.",
    ),
    (
        "🎨 طراحی گرافیک",
        "🎨 Graphic Design",
        "طراحی لوگو، بنر، و هویت بصری برند شما.",
        "Logo, banner, and brand visual identity design.",
    ),
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# ─────────────────────────────────────────────
# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    first_name = user.first_name or "کاربر"

    keyboard = [
        [
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 سلام {first_name} عزیز! خوش آمدید!\n"
        f"Hello {first_name}! Welcome!\n\n"
        f"🌐 لطفاً زبان خود را انتخاب کنید:\n"
        f"Please select your language:",
        reply_markup=reply_markup,
    )


# ─────────────────────────────────────────────
# منوی اصلی
def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    if lang == "fa":
        buttons = [
            [InlineKeyboardButton("📋 خدمات ما", callback_data="services_fa")],
            [InlineKeyboardButton("📞 ارتباط با ما", callback_data="contact_fa")],
            [InlineKeyboardButton("🌐 تغییر زبان", callback_data="change_lang")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("📋 Our Services", callback_data="services_en")],
            [InlineKeyboardButton("📞 Contact Us", callback_data="contact_en")],
            [InlineKeyboardButton("🌐 Change Language", callback_data="change_lang")],
        ]
    return InlineKeyboardMarkup(buttons)


# ─────────────────────────────────────────────
# منوی خدمات
def services_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for i, svc in enumerate(SERVICES):
        label = svc[0] if lang == "fa" else svc[1]
        buttons.append([InlineKeyboardButton(label, callback_data=f"svc_{lang}_{i}")])

    back_label = "🔙 بازگشت" if lang == "fa" else "🔙 Back"
    buttons.append([InlineKeyboardButton(back_label, callback_data=f"menu_{lang}")])
    return InlineKeyboardMarkup(buttons)


# ─────────────────────────────────────────────
# هندلر callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # انتخاب زبان
    if data in ("lang_fa", "lang_en"):
        lang = "fa" if data == "lang_fa" else "en"
        context.user_data["lang"] = lang
        text = (
            "✅ زبان فارسی انتخاب شد.\n\nاز منوی زیر انتخاب کنید:"
            if lang == "fa"
            else "✅ English selected.\n\nChoose from the menu below:"
        )
        await query.edit_message_text(text, reply_markup=main_menu_keyboard(lang))

    # تغییر زبان
    elif data == "change_lang":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            ]
        ])
        await query.edit_message_text(
            "🌐 لطفاً زبان خود را انتخاب کنید:\nPlease select your language:",
            reply_markup=keyboard,
        )

    # منوی اصلی
    elif data.startswith("menu_"):
        lang = data.split("_")[1]
        text = "از منوی زیر انتخاب کنید:" if lang == "fa" else "Choose from the menu below:"
        await query.edit_message_text(text, reply_markup=main_menu_keyboard(lang))

    # لیست خدمات
    elif data.startswith("services_"):
        lang = data.split("_")[1]
        title = "📋 خدمات ما را انتخاب کنید:" if lang == "fa" else "📋 Select a service:"
        await query.edit_message_text(title, reply_markup=services_keyboard(lang))

    # جزئیات هر خدمت
    elif data.startswith("svc_"):
        _, lang, idx = data.split("_")
        svc = SERVICES[int(idx)]
        name = svc[0] if lang == "fa" else svc[1]
        desc = svc[2] if lang == "fa" else svc[3]
        back_label = "🔙 بازگشت به خدمات" if lang == "fa" else "🔙 Back to Services"
        text = f"{name}\n\n{desc}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(back_label, callback_data=f"services_{lang}")]
        ])
        await query.edit_message_text(text, reply_markup=keyboard)

    # ارتباط با ما
    elif data in ("contact_fa", "contact_en"):
        lang = "fa" if data == "contact_fa" else "en"
        text = CONTACT_FA if lang == "fa" else CONTACT_EN
        back_label = "🔙 بازگشت" if lang == "fa" else "🔙 Back"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(back_label, callback_data=f"menu_{lang}")]
        ])
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")


# ─────────────────────────────────────────────
# پیام ناشناس
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "fa")
    text = (
        "لطفاً از دکمه‌های منو استفاده کنید. برای شروع مجدد /start بزنید."
        if lang == "fa"
        else "Please use the menu buttons. Type /start to restart."
    )
    await update.message.reply_text(text)


# ─────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    print("✅ Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
