import cv2

cap = cv2.VideoCapture(0)  # 0 for default webcam
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Webcam Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break
cap.release()
cv2.destroyAllWindows()