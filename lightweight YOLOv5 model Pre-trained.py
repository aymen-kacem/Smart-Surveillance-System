from ultralytics import YOLO

model = YOLO("yolov5s.pt")  # Small model for faster inference
results = model(r"C:\Users\User\Downloads\2.jpg", show=True) #put the image path like input here
print(results)
