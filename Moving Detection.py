import cv2
from ultralytics import YOLO
import time
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load YOLO model
model = YOLO("yolov5s.pt")

# Configure video capture
cap = cv2.VideoCapture(0)

# Track previous position and time
prev_center = None
prev_time = None
person_positions = []

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'aymenkacem2019@gmail.com'  # Replace with your email address
EMAIL_PASSWORD = 'aymen@123'  # Replace with your email password
TO_EMAIL = 'aymenkacem2019@gmail.com'  # Replace with recipient email

def send_email_alert(subject, body):
    """Send an email alert."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"Email sent: {subject}")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model.predict(frame, stream=True)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = model.names[cls]

            if conf > 0.25:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if label == "person":
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    if prev_center is not None and prev_time is not None:
                        dx = center_x - prev_center[0]
                        dy = center_y - prev_center[1]
                        dt = time.time() - prev_time

                        if dt > 0:
                            velocity = math.sqrt(dx ** 2 + dy ** 2) / dt
                            if velocity > 30:
                                cv2.putText(frame, "Running", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                                send_email_alert("Running Detected", "A person is detected running.")

                    if center_y > frame.shape[0] - 100:
                        cv2.putText(frame, "Falling", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        send_email_alert("Falling Detected", "A person is detected falling.")

                    person_positions.append((center_x, center_y, time.time()))
                    person_positions = [pos for pos in person_positions if time.time() - pos[2] < 5]
                    if len(person_positions) > 5:
                        cv2.putText(frame, "Loitering", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        send_email_alert("Loitering Detected", "A person is detected loitering.")

                    prev_center = (center_x, center_y)
                    prev_time = time.time()

                elif label == "knife":  # Adjust this to match the label for dangerous objects
                    send_email_alert("Dangerous Object Detected", "A knife has been detected!")

    cv2.imshow("Activity Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
