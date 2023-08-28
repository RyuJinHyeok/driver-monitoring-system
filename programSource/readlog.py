# log를 통해서 음성을 출력하는 프로그램

# 파이썬 라이브러리
import os
import time
import pygame

#사용자 정의 라이브러리
import config as config


# 음성안내 소리 파일
class_sounds = {
    "drowsy": "drowsy.wav",
    "mobile use": "mobile_use.wav",
    "HandsNotOnWheel": "hands_not_on_wheel.wav",
    "noSeatbelt": "no_seatbelt.wav",
}
pygame.mixer.init()

def play_sound(class_name): # 음성재생 함수
    sound_file_name = class_sounds.get(class_name)
    if sound_file_name:
        source_path = config.sound
        sound_file_path = os.path.join(source_path, sound_file_name)
        pygame.mixer.Sound(sound_file_path).play()
        time.sleep(0.001)
        # winsound.PlaySound(sound_file_path, winsound.SND_FILENAME)
        # os.system(f"powershell -c (New-Object Media.SoundPlayer '{sound_file_path}').PlaySync()")
        # time.sleep(1)
    else:
        print("음성 파일이 없습니다.")




'''
def process_log_file(log_file_path): 
    if not os.path.exists(log_file_path):
        print("log파일이 없습니다.")
        return

    with open(log_file_path, "r") as log_file:
        lines = log_file.readlines()
        for line in lines:
            class_name = line.strip()
            play_sound(class_name)
    os.remove(log_file_path)

'''
# log_file_path = "c:/Users/ADMIN/Documents/YOLO/Hack/test/log/log.txt"
# process_log_file(log_file_path)

# class_names = {
#     "1": "drowsy",
#     "2": "mobile_use",
#     "3": "HandsNotOnWheel",
#     "4": "noSeatbelt"
# }

# def save_class_to_log(class_number):
#     class_name = class_names.get(class_number)
#     if class_name:
#         with open(config.log_file_path, "a") as log_file:
#             log_file.write(class_name + "\n")
#     else:
#         print("Invalid class number")