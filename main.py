from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    ydl_opts = {
        # 'best' নিশ্চিত করবে যে অডিও এবং ভিডিও একসাথেই আছে
        'format': 'best[ext=mp4]/best', 
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # ভিডিও লিঙ্ক (অডিওসহ)
            video_url = info.get('url')
            
            # শুধু অডিও লিঙ্ক বের করার চেষ্টা
            audio_url = None
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                        audio_url = f.get('url')
                        break
            
            # যদি আলাদা অডিও না পাওয়া যায়, তবে ভিডিওর লিঙ্কটিকেই অডিও হিসেবে ব্যবহার করা যাবে
            if not audio_url:
                audio_url = video_url

            return jsonify({
                "status": "success",
                "title": info.get('title', 'Sabbir Video'),
                "video_url": video_url,
                "audio_url": audio_url,
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
