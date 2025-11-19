from imutils.video import VideoStream
import datetime
import imutils
import time
import cv2
import numpy as np

video_path = None
buffsize = 64
indx = 2

# lower and upper boundaries of a "red" object in HSV color space
red_range = [
    ((0, 100, 100), (10, 255, 255)),
    ((160,100,100), (179,255,255))] 


# initialize the list of tracked points
path = np.zeros((buffsize, 2), dtype='int')

if video_path is None:
    vs = VideoStream().start()
    time.sleep(2)   # warm up the camera
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

    mask1 = cv2.inRange(hsv, red_range[0][0], red_range[00][1])
    mask2 = cv2.inRange(hsv, red_range[1][0], red_range[1][1])
    mask = cv2.bitwise_or(mask1,mask2)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        # find the largest contour in the mask
        cnt = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the path list
        if indx < buffsize:
            path[indx] = (center[0], center[1])
            indx += 1
        else:
            path[0:indx-1] = path[1:indx]
            path[indx-1] = (center[0], center[1])

    # draw the trajectory lines
    for i in range(1, len(path)):
        # compute thickness and draw lines
        thickness = int(np.sqrt(len(path) / float(i + 1)) * 2.5)
        cv2.line(
            frame,
            (path[i-1][0], path[i-1][1]),
            (path[i][0],   path[i][1]),
            (0, 0, 255),
            thickness
        )

    cv2.imshow("Tracking", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

vs.stop() if video_path is None else vs.release()
cv2.destroyAllWindows()
