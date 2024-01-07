import os
import cv2

def decompose_video_to_frames(input_video_path, output_processed_data_dir):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at path {input_video_path}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)    
    interval = int(0.2 * fps) 
    frame_count = 0
    image_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if frame_count % interval == 0:
                frame_file_path = os.path.join(output_processed_data_dir, f'{frame_count:05d}.png')
                cv2.imwrite(frame_file_path, frame)
                image_count += 1
            frame_count += 1
        else:
            break

    cap.release()
    
    print(f"Processed {image_count} frames from the video.")
    
    return True

def get_video_properties(input_video_path):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at path {input_video_path}")
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    properties = {
        "fps": fps,
        "frames": cap.get(cv2.CAP_PROP_FRAME_COUNT),
        "duration": frame_count / fps
    }
    return properties