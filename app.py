from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    youtube_url = request.json.get('url')
    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'outtmpl': 'subtitles/%(id)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            video_id = info['id']
            subtitle_file = f'subtitles/{video_id}.en.vtt'

            if os.path.exists(subtitle_file):
                with open(subtitle_file, 'r') as f:
                    subtitles = f.read()
                os.remove(subtitle_file)
                return jsonify({"subtitles": subtitles})
            else:
                # If subtitles are not available, download audio
                audio_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }],
                    'outtmpl': 'audio/%(id)s.%(ext)s'
                }
                with yt_dlp.YoutubeDL(audio_opts) as ydl_audio:
                    ydl_audio.download([youtube_url])
                
                audio_file = f'audio/{video_id}.mp3'
                return jsonify({"audio_path": audio_file})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
