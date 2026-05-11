import cv2
import datetime

class AlertSystem:
    def __init__(self):
        self.alert_log = []

    def draw_alert(self, frame, bag, elapsed):
        x1, y1, x2, y2 = bag["box"]
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 3)
        cv2.putText(frame, f"UNATTENDED {bag['label'].upper()}",
                    (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0,0,255), 2)
        cv2.putText(frame, f"Time: {int(elapsed)}s",
                    (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0,0,255), 2)
        return frame

    def draw_normal(self, frame, bag):
        x1, y1, x2, y2 = bag["box"]
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(frame, bag["label"],
                    (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0,255,0), 2)
        return frame

    def draw_person(self, frame, person):
        x1, y1, x2, y2 = person["box"]
        cv2.rectangle(frame, (x1,y1), (x2,y2), (255,255,0), 2)
        return frame

    def log_alert(self, bag):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = {
            "time": timestamp,
            "object": bag["label"],
            "status": "Alert"
        }
        self.alert_log.append(entry)
        return entry

    def reset(self):
        self.alert_log.clear()