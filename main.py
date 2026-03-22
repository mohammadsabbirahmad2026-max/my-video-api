from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Sabbir's All-in-One Video API is LIVE! 🚀"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "লিঙ্ক দেওয়া হয়নি!"}), 400

    # এখানে আমি শক্তিশালী হেডার যোগ করেছি যা ফেসবুক/টিকটকের ব্লক ভাঙবে
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://www.facebook.com/'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            title = info.get('title', 'Video')

            return jsonify({
                "status": "success",
                "title": title,
                "video_url": direct_link
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Render সাধারণত পোর্ট ৮০০০ বা ১০০০০ ব্যবহার করে, তাই অটোমেটিক ডিটেকশনের ব্যবস্থা রাখা ভালো
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
