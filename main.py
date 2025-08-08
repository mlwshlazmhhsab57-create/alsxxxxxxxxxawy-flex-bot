from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

OWNER_NUMBER, OWNER_PASS, USER1_NUMBER, USER1_PASS, USER2_NUMBER, USER2_PASS = range(6)

OWNER_PHONE = '0123456789'
OWNER_PASSWORD = '123456'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 اهلا! من فضلك ابعت رقم المالك:")
    return OWNER_NUMBER

async def get_owner_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != OWNER_PHONE:
        await update.message.reply_text("❌ الرقم غلط. حاول تاني.")
        return OWNER_NUMBER
    context.user_data['owner_number'] = update.message.text
    await update.message.reply_text("✅ تمام، دلوقتي ابعت الباسورد:")
    return OWNER_PASS

async def get_owner_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != OWNER_PASSWORD:
        await update.message.reply_text("❌ الباسورد غلط. حاول تاني.")
        return OWNER_PASS
    await update.message.reply_text("✅ تم تسجيل الدخول كمالك.\nابعت رقم الفرد الأول:")
    return USER1_NUMBER

async def get_user1_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['user1_number'] = update.message.text
    await update.message.reply_text("تمام، ابعت باسورد الفرد الأول:")
    return USER1_PASS

async def get_user1_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['user1_pass'] = update.message.text
    await update.message.reply_text("تمام، ابعت رقم الفرد التاني:")
    return USER2_NUMBER

async def get_user2_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['user2_number'] = update.message.text
    await update.message.reply_text("تمام، ابعت باسورد الفرد التاني:")
    return USER2_PASS

async def get_user2_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['user2_pass'] = update.message.text
    await update.message.reply_text("✅ تم حفظ كل البيانات. شكراً!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم إلغاء العملية.")
    return ConversationHandler.END

if __name__ == '__main__':
    import os
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            OWNER_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_owner_number)],
            OWNER_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_owner_pass)],
            USER1_NUMBER: [MessageHandler(]()_
