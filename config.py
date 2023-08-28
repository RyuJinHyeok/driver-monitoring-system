import os

path = os.path.dirname(os.path.abspath(__file__)) 

# mode == 1 -> 졸음 감지 모델
# mode == 2 -> 통합 모델
# mode == 3 -> 실시간 졸음 감지 모델
mode = 1

# AVI 영상이 저장되어 있는 위치
source_path= os.path.join(path, "programSource/videos")

# 사용자 ID별로 분리된 영상을 저장할 루트 폴더
destination_path = os.path.join(path, "userData/save")

# log 저장 경로
log_file_path = os.path.join(path, "userData/log")

# 음성안내 소리파일 저장 경로
sound = os.path.join(path, "programSource/sounds")

# 비디오 파일
videoFile=os.path.join(path, "test2_team1_1.avi")

# GPU 사용여부
GPU=True