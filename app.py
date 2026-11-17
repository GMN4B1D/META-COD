from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
os.makedirs("downloads", exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        url = request.form['url']
        
        # YT COOKIE PROBLEM FIX
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            # YT ke android client hisebe dekhabo, tahole Accept cookie chabena
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']
                }
            },
            # Jodi cookies.txt file thake oita use korbe
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        }
        # None value remove
        ydl_opts = {k: v for k, v in ydl_opts.items() if v is not None}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                msg = f"✅ Download Complete: {info.get('title', 'Video')}"
        except Exception as e:
            msg = f"❌ Error: {e}"

    return render_template('index.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
