from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    if not url:
        return jsonify({"status": "error", "message": "无效链接"})
    
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        filename = stream.download(output_path="downloads")
        return jsonify({"status": "success", "filename": os.path.basename(filename)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
