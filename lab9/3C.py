from imutils.video import VideoStream
import imutils
import numpy as np
import time
import cv2

video_path = None
buffsize = 64
indx = 0

# path buffer
path = np.zeros((buffsize, 2), dtype="int")

# PIROS tartomány HSV-ben (3.A)
red_lower1 = (0, 120, 70)
red_upper1 = (10, 255, 255)
red_lower2 = (170, 120, 70)
red_upper2 = (180, 255, 255)

# video / kamera
if video_path is None:
    vs = VideoStream(src=0).start()
    time.sleep(2)
else:
    vs = cv2.VideoCapture(video_path)

while True:
    frame = vs.read()
    frame = frame if video_path is None else frame[1]

    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    blur = cv2.GaussianBlur(frame, (9, 9), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # 3.A – piros mask
    mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask = cv2.bitwise_or(mask1, mask2)

    # zajszűrés
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # kontúrok
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    center = None

    if len(cnts) > 0:
        # legnagyobb kontúr
        cnt = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)

        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10 and center is not None:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # PATH FRISSÍTÉS (3.B)
            if indx < buffsize:
                path[indx] = center
                indx += 1
            else:
                path[:-1] = path[1:]
                path[-1] = center
    else:
        # NINCS objektum → töröljük a nyomvonalat (3.B)
        indx = 0

    # 3.C – fordított vastagságú track
    for i in range(1, indx):
        min_th = 1
        max_th = 6
        t = i / float(indx)  # 0..1
        thickness = int(min_th + t * (max_th - min_th))

        cv2.line(
            frame,
            (path[i-1][0], path[i-1][1]),
            (path[i][0], path[i][1]),
            (0, 0, 255),
            thickness
        )

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if video_path is None:
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows()
