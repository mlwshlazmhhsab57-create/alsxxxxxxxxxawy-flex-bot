import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

OWNER_PASS = "1234"

ASK_OWNER, ASK_PASSWORD, ASK_MEMBERS = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("أهلاً! من فضلك ادخل رقم المالك:")
    return ASK_OWNER

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["owner_number"] = update.message.text
    await update.message.reply_text("تمام، دلوقتي ادخل الباسورد:")
    return ASK_PASSWORD

async def ask_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text != OWNER_PASS:
        await update.message.reply_text("كلمة المرور غلط. جرب تاني من أول /start")
        return ConversationHandler.END

    await update.message.reply_text("تمام ✅
دلوقتي ابعت أرقام الأفراد والباسوردات (كل واحد في سطر):")
    return ASK_MEMBERS

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["members"] = update.message.text
    await update.message.reply_text("تم الحفظ. شكراً 🙏")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_OWNER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_password)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_members)],
            ASK_MEMBERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, done)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()