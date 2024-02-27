import requests
import json

# URL of the Flask app endpoint
url = 'http://130.126.139.253:3000/get_result'

# Data to be sent to the API
data = {
    'video_url': 'http://130.126.139.253:5000/cat.mp4',
    'app_id': '123'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.text)
