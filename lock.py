import cv2
import numpy as np
import time
import pyautogui
import os


cap = cv2.VideoCapture(0)


fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg = cv2.createBackgroundSubtractorMOG2(history=4000, varThreshold=300)



motion_detected = False


no_motion_elapsed_time = 0


no_motion_lock_time = 5

while True:
 
    ret, frame = cap.read()

 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)


    edges = cv2.Canny(fgmask, 50, 190)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    num_contours = len(contours)

    # Hareket algılandıysa
    if num_contours > 0:
        motion_detected = True
        no_motion_elapsed_time = 0
    else:
        no_motion_elapsed_time += 1

 
    if no_motion_elapsed_time > no_motion_lock_time:
        os.system("lock.bat")
        motion_detected = False
        no_motion_elapsed_time = 0
        


    cv2.imshow('frame', fgmask)

    # Q tuşuna basılırsa çıkış yapma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()


