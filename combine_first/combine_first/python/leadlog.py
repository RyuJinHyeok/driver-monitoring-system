import os
import time

class_sounds = {
    "drowsy": "drowsy.mp3",
    "mobile_use": "mobile_use.mp3",
    "HandsNotOnWheel": "hands_not_on_wheel.mp3",
    "noSeatbelt": "no_seatbelt.mp3",
}
def play_sound(class_name):
    sound_file_name = class_sounds.get(class_name)
    if sound_file_name:
        source_path = "/Users/k4n9jun3/Documents/23하계해커톤/combine_first/sounds"
        sound_file_path = os.path.join(source_path, sound_file_name)
        os.system(f"afplay {sound_file_path}")
        time.sleep(1)
    else:
        print("사운드 파일 없음")

def process_log_file(log_file_path):
    if not os.path.exists(log_file_path):
        print("log파일을 못 찾음")
        return

    with open(log_file_path, "r") as log_file:
        lines = log_file.readlines()
        for line in lines:
            class_name = line.strip()
            play_sound(class_name)
    os.remove(log_file_path)
log_file_path = "/Users/k4n9jun3/Documents/23하계해커톤/combine_first/log/log.txt"
process_log_file(log_file_path)
