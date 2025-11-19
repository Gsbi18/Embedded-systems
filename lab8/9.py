from pyzbar import pyzbar
import cv2

image = cv2.imread("qrkod.png")
if image is None:
    raise Exception("nem tudom beolvasni a barcode.png-t")

barcodes = pyzbar.decode(image)

for barcode in barcodes:
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 2)

cv2.imshow("out", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
