import os
import telebot
import requests

# البوت هيقرأ التوكن تلقائياً من إعدادات Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "أهلاً بيك في مساعد صناع المحتوى 🚀\n\n"
        "ابعتلي رابط أي فيديو تيك توك وهجيبلك:\n"
        "📊 إحصائيات التفاعل كاملة\n"
        "📥 رابط تحميل بدون علامة مائية\n\n"
        "أو اكتبلي فكرة فيديو عشان أظبطلك العنوان والهاشتاجات!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def analyze_tiktok(message):
    url = message.text.strip()
    wait_msg = bot.reply_to(message, "⏳ جاري تحليل الفيديو وجلب البيانات...")
    
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            data = response["data"]
            views = data.get("play_count", 0)
            likes = data.get("digg_count", 0)
            comments = data.get("comment_count", 0)
            shares = data.get("share_count", 0)
            video_no_watermark = data.get("play", "")
            
            engagement = round(((likes + comments + shares) / views) * 100, 2) if views > 0 else 0
            
            report = (
                f"📊 **تقرير تحليل الفيديو:**\n\n"
                f"👁️ المشاهدات: `{views:,}`\n"
                f"❤️ اللايكات: `{likes:,}`\n"
                f"💬 التعليقات: `{comments:,}`\n"
                f"🔄 المشاركات: `{shares:,}`\n"
                f"🔥 نسبة التفاعل: `{engagement}%`\n\n"
                f"📥 [اضغط هنا لتحميل الفيديو بدون علامة مائية]({video_no_watermark})"
            )
            bot.edit_message_text(report, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ مقدرتش أوصل للفيديو، تأكد إن الحساب عام والرابط صحيح.", chat_id=message.chat.id, message_id=wait_msg.message_id)
            
    except Exception as e:
        bot.edit_message_text("⚠️ حصل خطأ أثناء الاتصال، جرب تاني بعد ثواني.", chat_id=message.chat.id, message_id=wait_msg.message_id)

print("البوت شغال...")
bot.infinity_polling()
