import os
import subprocess

def list_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.mp4')]

def get_time_input(prompt):
    while True:
        time_str = input(prompt)
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            print("Invalid format. Please enter time in HH:MM:SS format.")

def cut_video(input_file, start_time, end_time, output_file, output_format):
    if output_format == 'mp4':
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', str(start_time // 3600) + ':' + str((start_time % 3600) // 60).zfill(2) + ':' + str(start_time % 60).zfill(2),
            '-to', str(end_time // 3600) + ':' + str((end_time % 3600) // 60).zfill(2) + ':' + str(end_time % 60).zfill(2),
            '-c', 'copy',
            output_file
        ]
    elif output_format == 'gif':
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', str(start_time // 3600) + ':' + str((start_time % 3600) // 60).zfill(2) + ':' + str(start_time % 60).zfill(2),
            '-to', str(end_time // 3600) + ':' + str((end_time % 3600) // 60).zfill(2) + ':' + str(end_time % 60).zfill(2),
            '-vf', 'fps=10,scale=320:-1:flags=lanczos',
            output_file
        ]
    
    subprocess.run(command)

if __name__ == '__main__':
    directory = input("Enter the directory containing MP4 files: ")
    
    while True:
        if not os.path.exists(directory):
            print("Directory does not exist.")
            continue
    
        mp4_files = list_files(directory)
    
        if not mp4_files:
            print("No MP4 files found in the directory.")
            continue
        
        break

    print("Select a file to cut:")
    for i, file in enumerate(mp4_files):
        print(f"{i + 1}. {file}")

    while True:
        choice = int(input("Enter the number of the file to cut: ")) - 1
        if choice < 0 or choice >= len(mp4_files):
            print("Invalid selection.")
            continue
        break

    selected_file = mp4_files[choice]

    start_time = get_time_input("Enter the start time in HH:MM:SS format: ")
    end_time = get_time_input("Enter the end time in HH:MM:SS format: ")

    while True:
        if start_time >= end_time:
            print("Start time must be less than end time.")
            continue
        break

    while True:
        output_format = input("Enter the output format (mp4/gif): ").strip().lower()
        if output_format not in ['mp4', 'gif']:
            print("Invalid format. Please enter either 'mp4' or 'gif'.")
            continue
        break

    input_file = os.path.join(directory, selected_file)
    output_file = os.path.join(directory, f"cut/{selected_file.rsplit('.', 1)[0]}.{output_format}")

    cut_video(input_file, start_time, end_time, output_file, output_format)
    
    print(f"Cut video saved as {output_file}")
