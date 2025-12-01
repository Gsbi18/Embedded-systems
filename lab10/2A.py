import numpy as np
import cv2

prototxt_path = "src/MobileNetSSD_deploy_prototxt.txt"
model_path = "src/MobileNetSSD_deploy.caffemodel"


video_path = None

conf_limit = 0.25

CLASSES = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tv/monitor",
]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("Loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

if video_path is None:
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError("Nem sikerült megnyitni a video forrást.")

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5
    )

    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > conf_limit:
            idx = int(detections[0, 0, i, 1])

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            color = COLORS[idx]

            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(
                frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

    cv2.imshow("MobileNetSSD – realtime detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
