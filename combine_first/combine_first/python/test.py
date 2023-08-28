import os
import leadlog

log_file_path = "/Users/k4n9jun3/Documents/23하계해커톤/combine_first/log/log.txt"
class_names = {
    "1": "drowsy",
    "2": "mobile_use",
    "3": "HandsNotOnWheel",
    "4": "noSeatbelt"
}

def save_class_to_log(class_number):
    class_name = class_names.get(class_number)
    if class_name:
        with open(log_file_path, "a") as log_file:
            log_file.write(class_name + "\n")
    else:
        print("Invalid class number")

while True:
    class_numbers = input("시뮬레이션 상황(1~4)을 쉼표로 구분하여 입력하세요 (종료하려면 '5' 입력): ")
    if class_numbers.lower() == '5':
        break
    
    class_numbers_list = class_numbers.split(',')
    for class_number in class_numbers_list:
        save_class_to_log(class_number.strip())

    log_file = "/Users/k4n9jun3/Documents/23하계해커톤/combine_first/log/log.txt"
    leadlog.process_log_file(log_file)
