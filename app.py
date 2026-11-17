from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url') if data else None
    if not url:
        return jsonify({"error": "URL missing"}), 400

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'nocheckcertificate': True,
        # YT cookie fix
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # best direct url
            if 'entries' in info:
                info = info['entries'][0]
            
            formats = info.get('formats', [])
            # mp4 filter
            video_url = info.get('url')
            title = info.get('title')

            return jsonify({"title": title, "url": video_url, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
