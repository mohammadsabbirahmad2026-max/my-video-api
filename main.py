from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Sabbir's Fast API is LIVE! 🚀"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "URL missing"}), 400

    ydl_opts = {
        # এই লাইনটি অডিওসহ ভিডিওর সেরা ফাইলটি খুঁজে নেবে (Merge করা ফাইল)
        'format': 'best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # download=False মানে সার্ভারে কোনো ফাইল সেভ হবে না
            info = ydl.extract_info(video_url, download=False)
            
            # অডিওসহ ভিডিওর লিঙ্ক ফিল্টার করা
            formats = info.get('formats', [])
            final_link = None
            
            # আমরা এমন লিঙ্ক খুঁজবো যাতে অডিও (acodec) এবং ভিডিও (vcodec) দুটোই আছে
            for f in reversed(formats):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                    final_link = f.get('url')
                    break
            
            # যদি উপরে না পায়, তবে ডিফল্ট সবথেকে ভালো লিঙ্কটি নিবে
            if not final_link:
                final_link = info.get('url')

            return jsonify({
                "status": "success",
                "title": info.get('title', 'Sabbir Video'),
                "video_url": final_link,
                "audio_url": final_link, # ভিডিওর ভেতর গান থাকবেই
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
            actual_filename = ydl.prepare_filename(info)
            
            # ভিডিওর আসল নাম এবং ডাটা সংগ্রহ
            title = info.get('title', 'Sabbir Video')
            thumbnail = info.get('thumbnail')

            # এপিআই এখন ভিডিওর ডাইরেক্ট ডাউনলোড লিঙ্ক দেবে (আপনার সার্ভার থেকে)
            # মনে রাখবেন, রেন্ডারে ফাইল বেশিক্ষণ থাকে না, তাই সাথে সাথে পাঠাতে হবে
            return jsonify({
                "status": "success",
                "title": title,
                "video_url": f"{request.host_url}files/{os.path.basename(actual_filename)}",
                "thumbnail": thumbnail
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ফাইল সার্ভ করার রুট
@app.route('/files/<filename>')
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    
    # ফাইল পাঠানোর পর ডিলিট করার লজিক (Custom Response)
    def generate():
        with open(file_path, 'rb') as f:
            yield from f
        try:
            os.remove(file_path) # ফাইল পাঠানো শেষ হলে ডিলিট করে দিবে
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Error deleting: {e}")

    return app.response_class(generate(), mimetype='video/mp4')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
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
