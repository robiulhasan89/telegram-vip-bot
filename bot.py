import telebot

# Environment থেকে Token নেয়ার জন্য
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS").split(',')]
VIP_CHANNEL_LINKS = os.getenv("VIP_CHANNEL_LINKS").split(',')
REFERRAL_LINK = os.getenv("REFERRAL_LINK")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Welcome to VIP Access Bot.\nPlease send me your Trader ID to verify.")

@bot.message_handler(func=lambda m: True)
def handle_trader_id(message):
    trader_id = message.text.strip()

    if not trader_id.isdigit():
        bot.reply_to(message, "⚠️ Invalid Trader ID. Please send a correct numeric ID.")
        return

    # যদি অ্যাডমিন হয়, সরাসরি VIP লিংক দেয়
    if message.from_user.id in ADMIN_IDS:
        send_vip_links(message.chat.id)
        return

    # নরমাল ইউজারের জন্য চেক করবো
    if check_trader_id(trader_id):
        send_vip_links(message.chat.id)
    else:
        bot.send_message(message.chat.id, f"❌ Sorry! Your Trader ID is not valid under our Referral.\n\n👉 Please create an account using our link first:\n{REFERRAL_LINK}")

def check_trader_id(trader_id):
    """
    এখানে এখন আমরা ধরছি সব সঠিক আইডি ১০০% ম্যানুয়ালি চেক করতে হবে না।
    ভবিষ্যতে API দিয়ে অটো চেক করা যাবে।
    """
    # এখন সব ID চেক ফিক্স করে True করে দিলাম।
    return True

def send_vip_links(chat_id):
    links_text = "🎉 Congratulations! Here are your VIP Channel Links:\n\n"
    for link in VIP_CHANNEL_LINKS:
        links_text += f"🔗 {link}\n"
    bot.send_message(chat_id, links_text)

bot.infinity_polling()
