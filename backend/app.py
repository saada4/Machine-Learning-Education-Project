from flask import Flask, jsonify, render_template, request
import requests
import os

app = Flask(__name__)

VIDEO_PATH='/data5/haozhen/app/data'

@app.route('/',methods=['GET'])
def test():
    return "connected", 200

@app.route('/get_result',methods=['POST'])
def get_result():
    video_url = request.json.get('video_url')
    app_id = request.json.get('app_id')    # application id, folder name for this user's data
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400
    if not app_id:
        app_id = "000"
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            video_path = os.path.join(VIDEO_PATH, app_id)
            video_filename = os.path.join(video_path, "preprocess.mp4")
            os.makedirs(os.path.dirname(video_filename), exist_ok=True)
            with open(video_filename, 'wb') as video_file:
                video_file.write(response.content)
            return jsonify({"success": True, "message": "Video downloaded successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to download video"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='130.126.139.253', port=3000)
    #app.run(host='127.0.0.1', port=3000)