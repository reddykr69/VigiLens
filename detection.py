from ultralytics import YOLO
import sys
import os

def get_model_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "yolov8s.pt")
    return "yolov8s.pt"

class ObjectDetector:
    def __init__(self):
        self.model = YOLO(get_model_path())
        self.target_classes = ["person", "backpack", "handbag", "suitcase"]

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        persons = []
        bags = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                conf = float(box.conf[0])

                if label in self.target_classes and conf > 0.5:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    obj = {
                        "label": label,
                        "box": (x1, y1, x2, y2),
                        "center": (cx, cy),
                        "conf": conf
                    }

                    if label == "person":
                        persons.append(obj)
                    else:
                        bags.append(obj)

        return persons, bags