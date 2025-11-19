from imutils.video import VideoStream
import imutils
import datetime
import argparse
import time
import cv2
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--width", type=int, default=400, help="ablak szélessége")
ap.add_argument("--picamera", type=int, default=0, help="1 = PiCamera (RPi only), 0 = USB")
ap.add_argument("--cam-index", type=int, default=0, help="kamera index (0=alapértelmezett)")
args = vars(ap.parse_args())

# PiCamera csak Raspberry Pi-n működik
if args["picamera"] == 1:
    sys.exit("PiCamera csak Raspberry Pi-n támogatott. Mac-en használd USB/beépített kamerával (--picamera 0).")

# USB / beépített kamera
vs = VideoStream(src=args["cam_index"]).start()
time.sleep(2.0)  # bemelegedési idő

try:
    while True:
        frame = vs.read()
        if frame is None:
            print("Nem jön kép a kamerából. Próbáld másik --cam-index értékkel (pl. 1).")
            break

        frame = imutils.resize(frame, width=args["width"])
        ts = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        cv2.putText(frame, ts, (10, frame.shape[0]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    cv2.destroyAllWindows()
    vs.stop()
