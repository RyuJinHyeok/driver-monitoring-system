# 메인 프로그램

# 파이썬 라이브러리
import datetime
import cv2
from ultralytics import YOLO
import sys
import numpy as np
import datetime
import os 
import threading
import time

import dlib
from functools import wraps
from scipy.spatial import distance

# 사용자 정의 라이브러리
import config as config
import programSource.alert as alert
import programSource.readlog as rd
import programSource.aihack as ha

#사용자 정의 함수
def userID(): # 사용자 ID
    x=input("사용자 ID를 입력하세요.(4자리)")
    return x

def save_video(user_id,event,fps,w,h,img_array):  #동영상 저장
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    nowtime=now.strftime('%H%M%S') 
    filename= str(user_id)+'_'+event+'_'+nowtime+'.avi'
    filePath=os.path.join(config.source_path,filename)
    out = cv2.VideoWriter(filePath, fourcc, fps, (w, h))
    for img in img_array:
        out.write(img)
    alert.alertMail(event, filename)
    out.release()
    ha.process_files(config.source_path,config.destination_path)

# dlib 인식 모델 정의
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor(os.path.join(config.path, "shape_predictor_68_face_landmarks.dat"))

def calculate_EAR(eye): # 눈 거리 계산
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio

############################################

class_list = ['awake', 'drowsy'] if config.mode == 1 else ['mobile use', 'HandsNotOnWheel', 'HandsOnWheel', 'noSeatbelt', 'seatbelt'] 

# 모델 불러오기
model = YOLO(os.path.join(config.path, ("drowsy_detect_model.pt" if config.mode == 1 else 'integrated_model.pt'))) 

event = 'drowsy'

cap = cv2.VideoCapture(0 if config.mode == 3 else config.videoFile)  #   동영상 캡쳐 객체 생성

if not cap.isOpened():
    print("Camera open failed!")
    sys.exit()

w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) # 카메라에 따라 값이 정상적, 비정상적


DROWSY_THRESHOLD = 60
INTEGRATED_THRESHOLD = 15
img_array=[]
state=0
idx=0
inputs=None
drowsyCnt=0  
normalCntCnt=0

# 통합 모델용
event_cnt = [0, 0, 0, 0]
normal_event_cnt = [0, 0, 0, 0]

user_id=userID()
while True: # 프레임마다 연산
    now = datetime.datetime.now() #시간 객체
    start = datetime.datetime.now()

    class_cnt = [0, 0, 0, 0, 0]

    detected_event_list = []

    ret, raw_frame = cap.read()  # 다음 프레임 읽기
    if not ret: # 정상이 아니라면
        print('Cam Error') # 카메라 오류
        break

    if config.mode == 1:
        frame = cv2.resize(raw_frame, dsize=(raw_frame.shape[1] // 2, raw_frame.shape[0] // 2), interpolation=cv2.INTER_LINEAR)
    else: frame = raw_frame
        
    #############################
    results = model.predict(source=[frame], save=False)[0] # 추론 결과
    # 한 프레임 안에서 객체 종류마다 박스 그리기
    for data in results.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
        confidence = float(data[4])

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        label = int(data[5])

        # 중복 제거 및 상반되는 클래스 처리
        if class_cnt[label] == 1: continue

        if config.mode == 1:
            if label == 0 and class_cnt[1] == 1: continue
            elif label == 1 and class_cnt[0] == 1: continue
        else:
            if label == 1 and class_cnt[2] == 1: continue
            elif label == 2 and class_cnt[1] == 1: continue
            elif label == 3 and class_cnt[4] == 1: continue
            elif label == 4 and class_cnt[3] == 1: continue

        class_cnt[label] += 1

        if config.mode == 2 and (label in [0, 1, 3]):
            event_cnt[label] += 1
            if event_cnt[label] >= INTEGRATED_THRESHOLD:
                normal_event_cnt[label] = 0
                if event_cnt[label] == INTEGRATED_THRESHOLD:
                    detected_event_list.append(class_list[label])
                    if label == 0: event_cnt[label] = 0
            
        elif config.mode == 2 and (label in [2, 4]):
            normal_event_cnt[label - 1] += 1
            if normal_event_cnt[label - 1] >= INTEGRATED_THRESHOLD:
                event_cnt[label - 1] = 0


        # 박스 그리기
        if label in ([0] if config.mode == 1 else [2, 4]):
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)    # 초록
        else:
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 3)    # 빨강
        
        if ymin <= 0: ymin = 20
        cv2.putText(frame, class_list[label]+' '+str(round(confidence, 3)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
        inputs=label

    # 사진 저장
    if config.mode == 2:
        # 우선순위 정하기
        for e in detected_event_list:
            # 초깃값 제거
            if event == 'drowsy': event = e
            
            priority = {'noSeatbelt': 2, 'mobile use': 1, 'HandsNotOnWheel': 0}
            if priority[event] < priority[e]:
                event = e

        if len(detected_event_list) != 0:
            rd.play_sound(event)
            threading.Thread(target=save_video, args=(user_id, event, fps, w, h, [frame])).start()
            detected_event_list.clear()
            event = 'drowsy'
    

    if config.mode == 1 and len(results.boxes.data.tolist()) == 0:
        # 눈 탐지
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = hog_face_detector(gray)
        for face in faces:
            
            face_landmarks = dlib_facelandmark(gray, face)
            leftEye = []
            rightEye = []

            for n in range(36,42): # 오른쪽 눈 감지  
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                leftEye.append((x,y))
                next_point = n+1
                if n == 41:
                    next_point = 36
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

            for n in range(42,48): # 왼쪽 눈 감지
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                rightEye.append((x,y))
                next_point = n+1
                if n == 47:
                    next_point = 42
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

            left_ear = calculate_EAR(leftEye)
            right_ear = calculate_EAR(rightEye)

            EAR = (left_ear+right_ear)/2
            EAR = round(EAR,2)

            # 결과
            inputs = 1 if EAR < 0.19 else 0

    ##############################
    end = datetime.datetime.now()
    img_array.append(raw_frame)

    ''' 정보 표출 '''
    total = (end - start).total_seconds() # 한 프레임 작업하는데 걸린 시간
    # print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')
    fps_live = f'FPS: {1 / total:.2f}'   #Frames Per Second" #FPS 계산
    cv2.putText(frame, fps_live, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('frame', frame) 
    
    if state==0 and inputs == 1:
        temp=idx # 플래그 세우기
        print("temp ",temp)
        drowsyCnt+=1
        print("drcnt",drowsyCnt)
        
        if drowsyCnt>DROWSY_THRESHOLD:
            state=1 #현재 상태 졸음으로 설정
            normalCnt=0
            rd.play_sound('drowsy')
            

    elif state==1 and inputs ==0:
        temp=idx # 플래그 세우기
        print("temp ",temp)
        normalCnt+=1
        print("normalCnt",normalCnt)

        if normalCnt>DROWSY_THRESHOLD :
            state=0 #현재 상태 정상으로 설정
            threading.Thread(target=save_video, args=(user_id,event,fps,w,h,img_array)).start()
            # save_video(user_id,event,fps,w,h,img_array)
            drowsyCnt=0
            img_array=[]
            ''' 
            if normalCnt>CLASS_THRESHOLD :
            state=0 #현재 상태 정상으로 설정
            #log.append(idx-threshold)
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            print(frame.shape)
            nowtime=str(now.minute) + str(now.second)
            filename= str(user_id)+'_'+event+'_'+nowtime+'.avi'
            filePath=os.path.join(config.source_path,filename)

            out = cv2.VideoWriter(filePath, fourcc, fps, (w, h))
            for img in img_array:
                out.write(img)
            
            alert.alertMail(1, filename)
            out.release()
            drowsyCnt=0
            img_array=[]
            file_list = os.listdir(config.source_path)
            ha.process_files(file_list)
            '''

    
    
    if cv2.waitKey(1) == ord('q'): # 종료키
        save_video(user_id,event,fps,w,h,img_array)
        break
#############################################################################


cap.release()
cv2.destroyAllWindows()


########################################################
    # if cv2.waitKey(1) == ord('q'): # 종료키
    #     #rd.play_sound("drowsy")
    #     fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #     print(frame.shape)
    #     #nowtime=str(now.minute) + str(now.second)
    #     nowtime=now.strftime('%H%M%S') 
    #     filename= str(user_id)+'_'+event+'_'+nowtime+'.avi'
    #     filePath=os.path.join(config.source_path,filename)

    #     out = cv2.VideoWriter(filePath, fourcc, fps, (w, h))
    #     for img in img_array:
    #         out.write(img)
    #     alert.alertMail(1, filename)
    #     out.release()
    #     # file_list = os.listdir(config.source_path)
    #     # ha.process_files(file_list)
    #     ha.process_files(config.source_path,config.destination_path)
    #     break

