import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.getenv("TOKEN")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': 'video.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        },
        'nocheckcertificate': True,
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video") and file.endswith(".mp4"):
                with open(file, 'rb') as f:
                    await update.message.reply_video(video=f)
                os.remove(file)
                return

        await update.message.reply_text("❌ No se pudo descargar el video")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
