from ultralytics import YOLO
import cv2

model = YOLO("yolov8s.pt")

TARGET_CLASSES = ["person", "backpack", "handbag", "suitcase"]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
  
    results = model(frame)  

    for r in results:
     for box in r.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        conf = float(box.conf[0])   

        if label in TARGET_CLASSES and conf > 0.5: 
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0,255,0), 2)

    cv2.imshow("Filtered Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()azs