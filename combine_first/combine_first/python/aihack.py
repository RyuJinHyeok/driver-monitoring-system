import os
import re
import shutil

source_path = "/Users/k4n9jun3/Documents/23하계해커톤/combine_first/videos"
destination_path = "/Users/k4n9jun3/Documents/23하계해커톤/combine_first/save"

def process_files(files):
    pattern = re.compile(r"(\d+)_(\w+)_(\d\d\d\d-\d\d\d\d)\.avi")
    for file_name in files:
        if file_name.endswith('.avi'):
            match = pattern.match(file_name)
            if match:
                id_part, class_part, timeline_part = match.groups()
                id_folder = os.path.join(destination_path, id_part)
                if not os.path.exists(id_folder):
                    os.makedirs(id_folder)
                new_file_name = f"{class_part}-{timeline_part}.avi"
                destination_file_path = os.path.join(id_folder, new_file_name)
                source_file_path = os.path.join(source_path, file_name)
                shutil.copy(source_file_path, destination_file_path)
            else:
                print(f"포맷이 맞지 않습니다.")
                
    for file_name in files:
        if file_name.endswith('.avi'):
            source_file_path = os.path.join(source_path, file_name)
            new_file_name = os.path.splitext(file_name)[0] + ".mp4"
            new_file_path = os.path.join(source_path, new_file_name)
            os.rename(source_file_path, new_file_path)

file_list = os.listdir(source_path)
process_files(file_list)
