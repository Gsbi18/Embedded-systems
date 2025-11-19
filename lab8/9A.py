# realtime_barcode_qr.py
from pyzbar.pyzbar import decode, ZBarSymbol
import cv2
import time
from collections import deque

# --- beállítások ---
CAM_INDEX = 0          # ha több kamera van: 0,1,2...
WIDTH, HEIGHT = 1280, 720  # kérhetsz nagyobb felbontást is
WINDOW_W, WINDOW_H = 960, 720  # megjelenítő ablak mérete

# mely szimbólumokat keressük (QR + gyakori vonalkódok)
SYMBOLS = [
    ZBarSymbol.QRCODE,
    ZBarSymbol.EAN13, ZBarSymbol.EAN8, ZBarSymbol.UPCA, ZBarSymbol.UPCE,
    ZBarSymbol.CODE128, ZBarSymbol.CODE39, ZBarSymbol.I25,
    ZBarSymbol.DATABAR, ZBarSymbol.DATABAR_EXP
]

# --- kamera megnyitása ---
cap = cv2.VideoCapture(CAM_INDEX)
# próbáljuk kérni az adott felbontást (nem minden driver teljesíti)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    raise RuntimeError("Nem tudtam megnyitni a kamerát. Ellenőrizd a CAM_INDEX-et és a jogosultságokat.")

# megjelenítő ablak
cv2.namedWindow("Barcode/QR Scanner", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Barcode/QR Scanner", WINDOW_W, WINDOW_H)

# FPS kijelzéshez kis átlagoló buffer
ts_hist = deque(maxlen=30)

print("Indul a valós idejű olvasás. Nyomj 'q'-t a kilépéshez, 's'-t a mentéshez.")
frame_id = 0

try:
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Képkocka olvasási hiba.")
            break

        t0 = time.time()

        # Célszerű szürkeárnyalatot adni a dekódernek (gyakran gyorsabb/stabilabb)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detektálás + dekódolás
        results = decode(gray, symbols=SYMBOLS)

        # Vizualizáció ugyanarra a képre, amit meg is jelenítünk
        vis = frame.copy()

        for b in results:
            (x, y, w, h) = b.rect
            data = b.data.decode("utf-8", errors="replace")
            typ = b.type

            # keret + felirat
            cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 0, 255), 2)
            label = f"{data} ({typ})"
            cv2.putText(vis, label, (x, max(0, y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # FPS becslés
        ts_hist.append(time.time() - t0)
        if ts_hist:
            fps = 1.0 / (sum(ts_hist) / len(ts_hist))
            cv2.putText(vis, f"FPS: {fps:.1f}   found: {len(results)}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # megjelenítés (ablak méretezhető marad)
        cv2.imshow("Barcode/QR Scanner", vis)

        # billentyűk: q=quit, s=save
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            out_name = f"frame_{frame_id:06d}.png"
            cv2.imwrite(out_name, vis)
            print(f"Elmentve: {out_name}")

        frame_id += 1

finally:
    cap.release()
    cv2.destroyAllWindows()
