import cv2
import numpy as np
import pyautogui as pag
import asyncio
import threading
import time
import argparse
from tkinter import messagebox

main_window_name = "watch out for mom critical"
main_motion_window_name = "watch out for mom critical motion"
ah_shit = False # 엄크 발생됨
motion = False # 모션 있음

# 파라미터
parser = argparse.ArgumentParser()
parser.add_argument("--sensitivity", type=int, help="민감도 0 ~ 100", default=10)
parser.add_argument("--max-diff", type=int, help="모션 감지 0 ~ ...", default=100)
parser.add_argument("--mom-critical-ready-delay", type=int, help="엄크 감지후 준비 딜레이 (s)", default=5)
parser.add_argument("--abs-delay-frame-count", type=int, help="비교 프레임 frame_count보다 높거나 같을수 없습니다, 0 이하이면 감지되지 않습니다", default=4)
parser.add_argument("--frame-count", type=int, help="임시 프레임 수", default=5)
parser.add_argument("--video", type=int, help="카메라 번호", default=0)
parser.add_argument("--no-gui", help="창을 표시하지 않음", action='store_true')

args = parser.parse_args()

sensitivity = args.sensitivity # 민감도 0 ~ 100
max_diff = args.max_diff # 모션 감지 차이
abs_delay_frame_count = args.abs_delay_frame_count # 비교 프레임 frame_count보다 높거나 같을수 없습니다, 0 이하이면 감지되지 않습니다
mom_critical_ready_delay = args.mom_critical_ready_delay # 엄크가 발생하고 난 후 다시 준비하는 시간입니다.
frame_count = args.frame_count # 임시 프레임 수
no_gui = args.no_gui # no gui

def main():
    print("sensitivity: " + str(sensitivity))
    print("max_diff: " + str(max_diff))
    print("abs_delay_frame_count: " + str(abs_delay_frame_count))
    print("mom_critical_ready_delay: " + str(mom_critical_ready_delay))
    print("frame_count: " + str(frame_count))
    print("video: " + str(args.video))
    print("no_gui: " + str(args.no_gui))

    global motion
    gray_frames = []
    sensitivity_s = 255 - (sensitivity * 2.54)

    video = cv2.VideoCapture(args.video) # 비디오 불러옴

    if not video.isOpened(): # 비디오가 열려있지 않으면
        print("카메라를 열수 없습니다")
        if not no_gui:
            messagebox.showerror(main_window_name, "카메라를 열수 없습니다.")
        return
    
    # 비디오 설정
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 480) # 비디오 해상도 설정
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

    # 기본값 설정
    ret, f = video.read()
    f_g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    for i in range(0, frame_count): # 기본값
        gray_frames.append(f_g)
    # 기본값 설정
       
    if not no_gui:
        cv2.namedWindow(main_window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(main_motion_window_name, cv2.WINDOW_NORMAL)
        h, w, c = f.shape
        cv2.resizeWindow(main_window_name, w, h)
        cv2.resizeWindow(main_motion_window_name, w, h)

    while ret:
        try:
            ret, current_frame = video.read() # 프레임 불러옴
            if not no_gui:
                draw = current_frame.copy() # 프레임 복제

            if not ret: break
            
            current_gray = gray_frames[frame_count - 1] = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            current_diff = cv2.absdiff(current_gray, gray_frames[frame_count - abs_delay_frame_count - 1])
            ret, current_threshold = cv2.threshold(current_diff, sensitivity_s, 255, cv2.THRESH_BINARY)
            
            diff = cv2.morphologyEx(current_threshold, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
            diff_cnt = cv2.countNonZero(diff)
        

            if diff_cnt > max_diff:
                motion = True
                nzero = np.nonzero(diff)
            
                if not no_gui:
                    cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])),
                        (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
    
                    cv2.putText(draw, "oh shit mom critical", (10, 60), # 모션 감지 그리기
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))

                oh_shit_mom_critical()
            else:
                motion = False
        
            if not no_gui:
                cv2.putText(draw, "diff: " + str(diff_cnt), (10, 20), # 차이 그리기
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
                if not ah_shit:
                    cv2.putText(draw, "mom critical ready.", (10, 40), # 엄크 준비됨
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))

            window_size = get_window_size(main_window_name)
        
            if not no_gui:
                cv2.imshow(main_window_name, draw)
                cv2.imshow(main_motion_window_name, current_threshold)

            push_frames(frame_count, gray_frames)
    
            if cv2.waitKey(1) & 0xFF == 27:
                break
        except: break
    cv2.destroyAllWindows()

def oh_shit_mom_critical(): # 오 쓋 엄크
    global ah_shit
    if ah_shit is True: return
    ah_shit = True
    mom_critical()
    threading.Thread(target=mom_critical_ready).start()

def mom_critical_ready(): # 엄크 준비
    global motion
    for i in range(0, int(mom_critical_ready_delay / 0.1)):
        time.sleep(0.1)
        if motion:
            mom_critical_ready() # 아직 모션이 있으면 다시 카운트
            return

    global ah_shit
    ah_shit = False

# 프레임 밀기
def push_frames(frame_count, frames): # 대충 프레임 미는거
    for i in range(0, frame_count): # 프레임 뒤로 밀기
        if(i > 0): frames[i - 1] = frames[i]

# 창 크기 가져오기
def get_window_size(name):
    v = cv2.getWindowImageRect(name)
    return v[2], v[3]

def mom_critical():
    pag.hotkey('ctrl', 'winleft', 'right')

main()