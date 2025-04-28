from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")
VIP_CHANNEL_LINKS = os.getenv("VIP_CHANNEL_LINKS", "").split(",")
REFERRAL_LINK = os.getenv("REFERRAL_LINK", "https://broker-qx.pro/sign-up/?lid=YOUR_ID")

# Dummy validation function – আসল ট্রেডার আইডি চেকের জন্য এখানে API লাগবে
def is_valid_trader_id(trader_id):
    # এখানে আপনি আপনার broker এর API connect করে চেক করবেন
    return trader_id.startswith("10") and len(trader_id) >= 6

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        "💡 Please send me your *Trader ID*.\n"
        "I will check if it's registered under my referral link.\n\n"
        "👉 Example: `1043281`",
        parse_mode="Markdown"
    )

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text.strip()

    # Admin Check (optional logging or approval)
    if user_id in ADMIN_IDS:
        await update.message.reply_text("✅ You are an admin.")
        return

    if is_valid_trader_id(message_text):
        await update.message.reply_text(
            "🎉 Congratulations!\n"
            "✅ Your Trader ID has been verified.\n"
            "🔐 Here are your VIP Channel Links:\n\n" +
            "\n".join([f"👉 {link}" for link in VIP_CHANNEL_LINKS])
        )
    else:
        await update.message.reply_text(
            "❌ Your Trader ID is *not valid* or not found under our referral.\n\n"
            f"🔗 Please create your account using our referral link:\n{REFERRAL_LINK}\n\n"
            "Then send your correct Trader ID again.",
            parse_mode="Markdown"
        )

# Main Function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
