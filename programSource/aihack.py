# 프로그램 이름 : 영상 파일을 사용자 이름에 따라 분류해주는 프로그램
# AVI를 mp4로 바꿔줌.

# 파이썬 라이브러리
import os
import re
import shutil
from moviepy.editor import VideoFileClip

# 사용자 정의 모듈 호출
import config


# source_path = config.source_path
# destination_path = config.destination_path

def process_files(source_path,destination_path):
    file_list = os.listdir(source_path)
    pattern = re.compile(r"(\d+)_(\w+)_(\d\d\d\d\d\d)\.avi")
    for file_name in file_list:
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
                
    for file_name in file_list:
        if file_name.endswith('.avi'):
            source_file_path = os.path.join(source_path, file_name)
            new_file_name = os.path.splitext(file_name)[0] + ".mp4"
            new_file_path = os.path.join(source_path, new_file_name)

            video_clip = VideoFileClip(source_file_path)
            video_clip.write_videofile(new_file_path, codec=('h264_nvenc' if config.GPU else 'h264_qsv'), audio_codec='aac', threads=4)
            os.remove(source_file_path)

#file_list = os.listdir(source_path)
#process_files(file_list)