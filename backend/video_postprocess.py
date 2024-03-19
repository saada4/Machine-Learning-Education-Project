import cv2
import os
from tqdm import tqdm
import argparse
import re


def post_process(source_dir, target_dir):
    out_paths = []
    frame_nums = []
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    avi_files = [f for f in os.listdir(source_dir) if f.endswith('.mp4') or f.endswith('.avi')] # input is .mp4 format

    for avi_file in tqdm(avi_files):
        avi_file_path = os.path.join(source_dir, avi_file)
        frames_dir = os.path.join(target_dir, os.path.splitext(avi_file)[0])
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
        
        # Capture the video from the avi file
        vidcap = cv2.VideoCapture(avi_file_path)
        
        success, image = vidcap.read()
        count = 0
        
        while success:
            # Save frame as a .jpg file of size (320, 224)
            resized_image = cv2.resize(image, (320, 224), interpolation=cv2.INTER_AREA)
            frame_filename = os.path.join(frames_dir, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_filename, resized_image)
            
            success, image = vidcap.read()
            count += 1

        if count != 0:
            out_paths.append(frames_dir)
            frame_nums.append(count - 1)
        # Release the video capture object
        vidcap.release()

    print("Decomposition completed.")
    print(f'In total processed {count} videos')
    # for i in range(len(out_paths)):
    #     print(f'{out_paths[i]} {frame_nums[i]} 0')
    return count

def parse_test_file(file_path, config_dict):
    results = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if 'average' in line or 'predicted class id:' in line:
                # Remove extra spaces and newlines
                cleaned_line = line.strip()
                # Extract data using regular expressions
                if 'average' in cleaned_line:
                    match = re.search(r"\[(\d+)/(\d+)\], average ([\d.]+) sec/video\s+Prec@1 ([\d.]+) \(([\d.]+)\)\s+Prec@5 ([\d.]+) \(([\d.]+)\)", cleaned_line)
                    if match:
                        results.append({
                            'test_index': int(match.group(1)),
                            'total_tests': int(match.group(2)),
                            'average_time': float(match.group(3)),
                            'prec@1_current': float(match.group(4)),
                            'prec@1_average': float(match.group(5)),
                            'prec@5_current': float(match.group(6)),
                            'prec@5_average': float(match.group(7)),
                            'predicted_class': None  # Placeholder for predicted class id
                        })
                        print(results)
                elif 'predicted class id:' in cleaned_line:
                    # The last entry will be the one needing the predicted class id
                    class_num = int(cleaned_line.split(': ')[1])
                    results[-1]['predicted_class'] = config_dict[class_num]
    return results
