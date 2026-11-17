import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Log on korlam jate error dekhte paro
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

#  /start command - Upore GM DOWNLOADER nam thakbe
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔥 **GM DOWNLOADER** 🔥\n"
        "━━━━━━━━━━━━━━━━\n"
        "GM's World Official Bot\n\n"
        "YouTube / Facebook / Instagram / TikTok\n"
        "Link pathao, ami instant download link dibo.\n\n"
        "👉 Just link send koro!"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# Link pele download korbe
async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "http" not in url:
        await update.message.reply_text("❌ Valid link dao GM")
        return

    status_msg = await update.message.reply_text("⏳ **GM DOWNLOADER** is Processing... Please wait 10s")

    try:
        # Eta new working API - yt-dlp er moto block khay na
        api_url = "https://co.wuk.sh/api/json"
        payload = {
            "url": url,
            "vCodec": "h264",
            "vQuality": "720",
            "aFormat": "mp3",
            "isAudioOnly": False
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        res = requests.post(api_url, json=payload, headers=headers, timeout=30)
        data = res.json()
        
        video_url = data.get("url")

        if video_url:
            final_text = (
                f"✅ **GM DOWNLOADER - Ready** ✅\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"Title: {data.get('text', 'Video')[:50]}\n\n"
                f"👇 **Download Link:** 👇\n"
                f"[🔥 CLICK HERE TO DOWNLOAD 🔥]({video_url})\n\n"
                f"Link kaj na korle, link e chap diye browser e open koro."
            )
            await status_msg.edit_text(final_text, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            await status_msg.edit_text(f"❌ Download fail hoise GM.\n\nAPI bolche: {data}\nOnno link diye try koro.")

    except Exception as e:
        await status_msg.edit_text(f"❌ Error hoise: {str(e)}\n30 sec por abar try koro.")
        logging.error(f"Error: {e}")

# Bot run
def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN Environment Variable e add koro nai!")
        return

    print("🔥 GM DOWNLOADER Bot Starting...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_handler))

    app.run_polling()

if __name__ == '__main__':
    main()
