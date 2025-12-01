#!/usr/bin/env python3

import cv2
import numpy as np
import pytesseract
import time
import os

EAST_MODEL_PATH = "frozen_east_text_detection.pb"
IMAGE_PATH = "himnusz.jpg"
CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
EAST_WIDTH = 320
EAST_HEIGHT = 320
ROI_EXPAND = 15
MIN_BOX_SIZE = 15


def decode_predictions(scores, geometry, conf_threshold):
    """
    EAST kimenetek dekódolása bounding boxokra.
    scores: 1x1xHxW
    geometry: 1x5xHxW
    Visszaad: rects, confidences
    rects: list of (startX, startY, endX, endY)
    confidences: list of float
    """
    (num_rows, num_cols) = scores.shape[2:4]
    rects = []
    confidences = []

    for y in range(num_rows):
        scores_data = scores[0, 0, y]
        x0_data = geometry[0, 0, y]
        x1_data = geometry[0, 1, y]
        x2_data = geometry[0, 2, y]
        x3_data = geometry[0, 3, y]
        angles_data = geometry[0, 4, y]

        for x in range(num_cols):
            score = scores_data[x]
            if score < conf_threshold:
                continue

            offset_x = x * 4.0
            offset_y = y * 4.0

            angle = angles_data[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            end_x = int(offset_x + (cos * x1_data[x]) + (sin * x2_data[x]))
            end_y = int(offset_y - (sin * x1_data[x]) + (cos * x2_data[x]))
            start_x = int(end_x - w)
            start_y = int(end_y - h)

            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(float(score))

    return rects, confidences


def main():
    if not os.path.exists(EAST_MODEL_PATH):
        raise FileNotFoundError(f"EAST modell nem található: {EAST_MODEL_PATH}")

    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Bemeneti kép nem található: {IMAGE_PATH}")

    print("[INFO] EAST modell betöltése...")
    net = cv2.dnn.readNet(EAST_MODEL_PATH)

    print("[INFO] Kép betöltése...")
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise RuntimeError("Nem sikerült beolvasni a képet.")

    orig = image.copy()
    (orig_h, orig_w) = image.shape[:2]

    new_w, new_h = EAST_WIDTH, EAST_HEIGHT
    r_w = orig_w / float(new_w)
    r_h = orig_h / float(new_h)

    image = cv2.resize(image, (new_w, new_h))
    (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(
        image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False
    )

    net.setInput(blob)

    layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

    print("[INFO] Detektálás EAST-tel...")
    start = time.time()
    (scores, geometry) = net.forward(layer_names)
    end = time.time()
    print(f"[INFO] EAST futási idő: {end - start:.2f} s")

    rects, confidences = decode_predictions(scores, geometry, CONF_THRESHOLD)

    indices = cv2.dnn.NMSBoxes(rects, confidences, CONF_THRESHOLD, NMS_THRESHOLD)

    if len(indices) == 0:
        print("[INFO] Nem talált szövegdobozt.")
        cv2.imshow("Eredmény", orig)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    if isinstance(indices, np.ndarray):
        indices = indices.flatten().tolist()
    else:
        indices = [i[0] for i in indices]

    result = orig.copy()

    print("[INFO] Tesseract OCR a detektált ROI-okon...")
    for idx in indices:
        (start_x, start_y, end_x, end_y) = rects[idx]

        start_x = int(start_x * r_w)
        start_y = int(start_y * r_h)
        end_x = int(end_x * r_w)
        end_y = int(end_y * r_h)

        if (end_x - start_x) < MIN_BOX_SIZE or (end_y - start_y) < MIN_BOX_SIZE:
            continue

        start_x = max(0, start_x - ROI_EXPAND)
        start_y = max(0, start_y - ROI_EXPAND)
        end_x = min(orig_w, end_x + ROI_EXPAND)
        end_y = min(orig_h, end_y + ROI_EXPAND)

        roi = orig[start_y:end_y, start_x:end_x]
        if roi.size == 0:
            continue

        config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(roi, config=config, lang="eng")
        text_clean = text.strip().replace("\n", " ")

        print(f'[OCR] "{text_clean}"  @ ({start_x},{start_y})–({end_x},{end_y})')

        cv2.rectangle(result, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        if text_clean:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.2
            thickness = 2

            (text_w, text_h), baseline = cv2.getTextSize(
                text_clean, font, font_scale, thickness
            )

            text_x = start_x
            text_y = start_y - 20

            if text_y - text_h < 0:
                text_y = end_y + text_h + 10

            bg_x1 = text_x
            bg_y1 = text_y - text_h - baseline
            bg_x2 = text_x + text_w
            bg_y2 = text_y + baseline

            bg_x1 = max(0, bg_x1)
            bg_y1 = max(0, bg_y1)
            bg_x2 = min(result.shape[1], bg_x2)
            bg_y2 = min(result.shape[0], bg_y2)

            cv2.rectangle(result, (bg_x1, bg_y1), (bg_x2, bg_y2), (255, 255, 255), -1)

            cv2.putText(
                result,
                text_clean,
                (text_x, text_y),
                font,
                font_scale,
                (0, 0, 0),
                thickness,
            )

    cv2.imshow("EAST + Tesseract eredmény", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
