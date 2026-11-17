import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("9091735677:AAGd-LJIKqwAN9dBxZTGd6jOOeAePe4pOeA") # Render e Environment Variable e diba

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GM N4B1D Bot Ready ✅\nLink pathao, ami download kore dibo.")

async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "http" not in url:
        return
    
    msg = await update.message.reply_text("⏳ Processing... 10 sec wait koro GM")
    
    try:
        # New Working API
        api_url = "https://co.wuk.sh/api/json"
        payload = {"url": url, "vCodec": "h264", "vQuality": "720"}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        
        r = requests.post(api_url, json=payload, headers=headers, timeout=25)
        data = r.json()
        
        video_link = data.get("url")
        
        if video_link:
            await msg.edit_text(f"✅ Ready GM!\n\n{data.get('text', 'Video')}\n\n👉 [CLICK TO DOWNLOAD]({video_link})", parse_mode='Markdown')
            # chaile direct video pathate paro:
            # await update.message.reply_video(video=video_link, caption="GM N4B1D META COD")
        else:
            await msg.edit_text(f"❌ Fail hoise: {data}\nOnno link try koro.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_handler))
    app.run_polling()
