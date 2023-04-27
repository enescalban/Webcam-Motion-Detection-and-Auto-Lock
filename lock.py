import cv2
import numpy as np
import time
import pyautogui
import os
import winsound

# Kamera aygıtı
cap = cv2.VideoCapture(0)

# Hareket tespiti için arka plan modeli
fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100)

# Hareket olup olmadığını takip etmek için
motion_detected = False

# Hareket algılanmadan geçen süre (saniye cinsinden)
no_motion_elapsed_time = 0

# Hareket algılanmadan kilitlenmesi gereken süre (saniye cinsinden)
no_motion_lock_time = 5

# tonun frekansı ve süresi
frequency = 1000  # Hz
duration = 1000  # ms

while True:
    # Kameradan video akışı alma
    ret, frame = cap.read()

    # Görüntüyü gri tonlamalı hale getirme ve arka plan modeli üzerinden geçirme
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
        
        # Hareket algılanmadığı ilk 3 saniye içinde
        if no_motion_elapsed_time <= 3*25:
            # 1000 Hz frekansında bir saniye boyunca ton çal
            winsound.Beep(frequency, duration)

        # Hareket algılanmadan geçen süre kilitlenmesi gereken süreyi aşıyorsa
        if no_motion_elapsed_time > no_motion_lock_time:
            os.system("lock.bat")
            motion_detected = False
            no_motion_elapsed_time = 0
            
    # Görüntüyü ekranda gösterme
    cv2.imshow('frame', fgmask)

    # Q tuşuna basılırsa çıkış yapma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
