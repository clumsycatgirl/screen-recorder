import numpy as np
import cv2
from PIL import ImageGrab
from screeninfo import get_monitors
import os
import time
import threading
import subprocess

def monitor_exit(stop_event):
    """Listens for the Q key to stop the recording."""
    while True:
        if input().strip().lower() == 'q':
            stop_event.set()  # Stop the recording
            break

def get_next_filename(output_dir):
    """Generates a unique filename for saving videos."""
    counter = 1
    while True:
        filename = os.path.join(output_dir, f"rec_{counter}.mp4")
        if not os.path.exists(filename):
            return filename
        counter += 1

def compress_video(input_file, output_file):
    """Compress the video file using ffmpeg."""
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vcodec', 'libx264',
        '-crf', '28',
        output_file
    ]
    subprocess.run(command)

def get_file_size(file_path):
    """Returns the file size in bytes."""
    return os.path.getsize(file_path) if os.path.exists(file_path) else 0

if __name__ == '__main__':
    output_dir = "output"
    compressed_dir = os.path.join(output_dir, "compressed")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(compressed_dir):
        os.makedirs(compressed_dir)

    monitors = get_monitors()
    if len(monitors) == 0:
        print("No monitors found.")
        exit(1)
    
    monitor = monitors[0]
    x, y, width, height = monitor.x, monitor.y, monitor.width, monitor.height

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    output_filename = get_next_filename(output_dir)
    
    video_writer = cv2.VideoWriter(output_filename, fourcc, 24.0, (width, height))

    print(f'Starting recording. Press Q to stop...')

    stop_event = threading.Event()
    exit_thread = threading.Thread(target=monitor_exit, args=(stop_event,))
    exit_thread.start()

    start_time = time.time()
    frame_count = 0
    fps = 0
    max_size = 9 * 1024 * 1024  # 9MB

    try:
        while not stop_event.is_set():
            frame_start_time = time.time()

            img = ImageGrab.grab(bbox=(x, y, width, height))
            np_img = np.array(img)
            cvt_image = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

            video_writer.write(cvt_image)

            # frame_time = time.time() - frame_start_time
            # frame_count += 1

            # elapsed_time = time.time() - start_time
            # if elapsed_time >= 1:
            #     fps = frame_count / elapsed_time
            #     print(f"Current FPS: {fps:.2f}")
                # start_time = time.time()
                # frame_count = 0

            # if get_file_size(output_filename) >= max_size:
            #     video_writer.release()
            #     print(f"Recording saved to {output_filename}")

            #     compressed_filename = os.path.join(compressed_dir, os.path.basename(output_filename).replace(".mp4", "_compressed.mp4"))
            #     compress_video(output_filename, compressed_filename)
            #     print(f"Compressed video saved to {compressed_filename}")

            #     output_filename = get_next_filename(output_dir)
            #     video_writer = cv2.VideoWriter(output_filename, fourcc, 24.0, (width, height))

    finally:
        video_writer.release()
        cv2.destroyAllWindows()
        print(f"Final recording saved to {output_filename}")

        compressed_filename = os.path.join(compressed_dir, os.path.basename(output_filename).replace(".mp4", "_compressed.mp4"))
        compress_video(output_filename, compressed_filename)
        print(f"Final compressed video saved to {compressed_filename}")
