import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Webcam not detected")
        break

    cv2.imshow("Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
        break


cap.release()
cv2.destroyAllWindows()
