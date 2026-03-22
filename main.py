from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Sabbir's Multi-Source Video API is LIVE! 🚀"

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', # সব ফরম্যাট চেক করবে
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # ব্যাকআপ লিঙ্ক তৈরির লজিক
            formats = info.get('formats', [])
            
            # ১. সেরা ভিডিও লিঙ্ক (অডিওসহ)
            video_url = info.get('url')
            
            # ২. ব্যাকআপ ভিডিও লিঙ্ক (যদি প্রথমটা কাজ না করে)
            backup_video = None
            for f in reversed(formats):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                    backup_video = f.get('url')
                    break
            
            # ৩. আলাদা অডিও লিঙ্ক (শুধু গান/মিউজিক)
            audio_url = None
            for f in formats:
                if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                    audio_url = f.get('url')
                    break

            return jsonify({
                "status": "success",
                "title": info.get('title', 'Sabbir Video'),
                "video_url": video_url or backup_video, # মেইন না থাকলে ব্যাকআপ
                "backup_url": backup_video,
                "audio_url": audio_url,
                "thumbnail": info.get('thumbnail'),
                "source": info.get('extractor_key')
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
