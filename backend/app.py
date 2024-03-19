from flask import Flask, jsonify, render_template, request
import requests
import os
import video_postprocess
from video_postprocess import post_process, parse_test_file
import csv
import yaml
import subprocess

app = Flask(__name__)

VIDEO_PATH='/data5/haozhen/app/data/raw'
FRAME_PATH='/data5/haozhen/app/data/frames'
CONFIG_PATH = '/data5/haozhen/app/data/config'
YAML_PATH = '/data5/haozhen/BIKE/configs/hmdb51/hmdb_zero_shot.yaml'
checkpoint_path = '/data5/haozhen/BIKE/checkpoints/k400-vit-b-16-f8.pt'
script_path = '/data5/haozhen/BIKE/scripts/run_test_zeroshot.sh'
predict_path = '/data5/haozhen/BIKE/sample_output.txt'

@app.route('/',methods=['GET'])
def test():
    return "connected", 200

@app.route('/get_result',methods=['POST'])
def get_result():
    video_url = request.json.get('video_url')
    app_id = request.json.get('app_id')    # application id, folder name for this user's data
    name_list = request.json.get('name_list') # class names
    filename = request.json.get('filename')
    label = request.json.get('label')  # correct class

    if label == None: # if correct class not provide, random assign a class
        label_num = 0 

    # class id config file
    config_file_path = os.path.join(CONFIG_PATH, app_id)
    config_file_path = os.path.join(config_file_path, 'names.csv')   # config file for app_id 123
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
    config_dict = dict()
    with open(config_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name'])  # Write the header
        
        for i, name in enumerate(name_list):
            writer.writerow([i, name])  # Write each id and name
            config_dict[i] = name
            if name == label and label != None:
                label_num = i
    print(f"File written successfully at {config_file_path}")

    txt_path = os.path.join(CONFIG_PATH, app_id)
    txt_path = os.path.join(txt_path, f'{app_id}.txt')
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400
    if not app_id:
        app_id = "000"
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            video_path = os.path.join(VIDEO_PATH, app_id)       # video directory for app_id 123
            frame_path = os.path.join(FRAME_PATH, app_id)       # frame directory for app_id 123
            video_filename = os.path.join(video_path, filename)
            os.makedirs(os.path.dirname(video_filename), exist_ok=True)
            os.makedirs(os.path.dirname(frame_path), exist_ok=True)
            with open(video_filename, 'wb') as video_file:
                video_file.write(response.content)
            
            frame_count = post_process(video_path, frame_path)            # decompose video to frames
            frame_path_video = os.path.join(frame_path, filename.split('.')[0])        # frame dir of a specific video (of filename)
            with open(txt_path, 'a') as f:                                  # edit label file (frame dir, frame count, labeled class)
                f.write(frame_path_video + ' ' + str(frame_count) + ' ' + f'{str(label_num)}')

            # modify paths on yaml config file
            with open(YAML_PATH, 'r') as file:
                yaml_content = yaml.safe_load(file)

            yaml_content['data']['num_classes'] = len(name_list)
            yaml_content['data']['val_root'] = frame_path
            yaml_content['data']['val_list'] = txt_path
            yaml_content['data']['label_list'] = config_file_path

            with open(YAML_PATH, 'w') as file:
                yaml.safe_dump(yaml_content, file)
            
            command = ['bash', script_path, YAML_PATH, checkpoint_path]
            result = subprocess.run(command, capture_output=True, text=True)   # run model to predict result

            if result.returncode == 0:
                print("Script executed successfully.")
                print("Output:", result.stdout)
            else:
                print("Script execution failed.")
                print("Error:", result.stderr)


            test_results = parse_test_file(predict_path, config_dict)
            return jsonify({"success": True, "message": "Video predicted successfully", "data": test_results}), 200
        else:
            return jsonify({"success": False, "message": "Failed to download video"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='130.126.139.253', port=3000)
    #app.run(host='127.0.0.1', port=3000)
