import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov5s.pt")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model.predict(frame, stream=True)

    # Annotate detected humans
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get the bounding box coordinates
            conf = box.conf[0].item()  # Get the confidence score
            cls = int(box.cls[0].item())  # Get the class ID
            label = model.names[cls]  # Get the class label (e.g., 'person', 'knife', etc.)

            # Only display the object if the confidence is above a threshold (e.g., 0.25)
            if conf > 0.25:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                cv2.putText(frame, f"{label}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                            2)  # Label the object

    cv2.imshow("Activity Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
