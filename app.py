from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def healthCheck():
    return "App is Running"

@app.route('/api/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        ydl_opts = {
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'noplaylist': True,
        'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')

            return jsonify({
                "download_url": video_url,
                "title": info.get('title'),
                "ext": info.get('ext')
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
