import requests
import json

# URL of the Flask app endpoint
url = 'http://130.126.139.253:3000/get_result'

# user give class categories, at least 5
name_list = [
    'fighting',
    'playing',
    'running',
    'jogging',
    'reading',
    'writing'
]

# Data to be sent to the API
data = {
    'video_url': 'http://130.126.139.253:8080/cat.mp4',
    'app_id': '123',
    'name_list': name_list,
    'filename': 'cat.mp4',
    'label': 'fighting'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.text)
