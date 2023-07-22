import cv2
import numpy as np
import time
import os
import winsound

# Kamera aygıtı
cap = cv2.VideoCapture(0)

# Hareket tespiti için arka plan modeli
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100)

# Hareket algılanmadan kilitlenmesi gereken süre (saniye cinsinden)
no_motion_lock_time = 5

# Hareket algılanmadan geçen süre (saniye cinsinden)
no_motion_elapsed_time = 0

# tonun frekansı ve süresi
frequency = 1000  # Hz
duration = 1000  # ms

# Bayrak, hareket algılandığını gösterir
motion_detected = False

# Bayrak, sesli uyarının yapıldığını gösterir
alerted = False

while True:
    # Kameradan video akışı alma, ancak görüntüyü işlemeyeceğiz
    _, frame = cap.read()

    # Görüntüyü gri tonlamalı hale getirme ve arka plan modeli üzerinden geçirme
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)

    edges = cv2.Canny(fgmask, 50, 190)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    num_contours = len(contours)

    # Hareket algılandıysa
    if num_contours > 0:
        motion_detected = True
        # Hareket algılandığında burada ses çalmamıza gerek yok
        # Çünkü hareket algılandığında zaten önceki uyarıyı yapmış oluyoruz
        no_motion_elapsed_time = 0
        # Eğer daha önce uyarı yapılmadıysa ve kilitlenme durumunda değilse
        if not alerted and no_motion_elapsed_time <= no_motion_lock_time*25:
            # 1000 Hz frekansında bir saniye boyunca ton çal
            winsound.Beep(frequency, duration)
            alerted = True
    else:
        no_motion_elapsed_time += 1

        # Hareket algılanmadan geçen süre kilitlenmesi gereken süreyi aşıyorsa
        if no_motion_elapsed_time > no_motion_lock_time*25:
            if not alerted:
                # Kilitlenme durumunda bir kez daha bip sesi çal
                winsound.Beep(frequency, duration)
                alerted = True
            os.system("lock.bat")
            motion_detected = False
            no_motion_elapsed_time = 0
            # Uyarı yapıldıktan sonra bayrağı sıfırla
            alerted = False

    # Herhangi bir görüntü işleme olmadan arka planda çalışıyoruz, ekrana göstermiyoruz

    # 'q' tuşuna basılırsa çıkış yapma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
