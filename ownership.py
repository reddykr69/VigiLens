import math
import time

class OwnershipTracker:
    def __init__(self, distance_threshold=200, time_threshold=10):
        self.distance_threshold = distance_threshold
        self.time_threshold = time_threshold
        self.abandoned_timers = {}

    def calculate_distance(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def find_nearest_person(self, bag, persons):
        if not persons:
            return None, float("inf")
        min_dist = float("inf")
        nearest = None
        for person in persons:
            d = self.calculate_distance(bag["center"], person["center"])
            if d < min_dist:
                min_dist = d
                nearest = person
        return nearest, min_dist

    def check_abandonment(self, bags, persons):
        current_time = time.time()
        alerts = []
        active_ids = []

        for bag in bags:
            bag_id = str(bag["box"])
            active_ids.append(bag_id)
            nearest, distance = self.find_nearest_person(bag, persons)

            if distance > self.distance_threshold:
                if bag_id not in self.abandoned_timers:
                    self.abandoned_timers[bag_id] = current_time
                else:
                    elapsed = current_time - self.abandoned_timers[bag_id]
                    if elapsed >= self.time_threshold:
                        alerts.append({
                            "bag": bag,
                            "elapsed": elapsed,
                            "distance": distance
                        })
            else:
                if bag_id in self.abandoned_timers:
                    del self.abandoned_timers[bag_id]

        for k in [k for k in self.abandoned_timers if k not in active_ids]:
            del self.abandoned_timers[k]

        return alerts