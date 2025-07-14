class HandRecog:  
    def __init__(self, hand_label):
        self.finger = 0
        self.ori_gesture = Gest.PALM
        self.prev_gesture = Gest.PALM
        self.frame_count = 0
        self.hand_result = None
        self.hand_label = hand_label
        
    def update_hand_result(self, hand_result):
        self.hand_result = hand_result
        
    def get_signed_dist(self, point):
        sign = -1
        if self.hand_result.landmark[point[0]].y < self.hand_result.landmark[point[1]].y:
            sign = 1
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist * sign 
        
    def get_dist(self, point):
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist  
    
    def get_dz(self, point):
        return abs(self.hand_result.landmark[point[0]].z - self.hand_result.landmark[point[1]].z)   
    
    def set_finger_state(self):
        if self.hand_result is None:
            return
        points = [[8, 5, 0], [12, 9, 0], [16, 13, 0], [20, 17, 0]]
        self.finger = 0
        self.finger = self.finger | 0  # thumb
        for idx, point in enumerate(points):            
            dist = self.get_signed_dist(point[:2])
            dist2 = self.get_signed_dist(point[1:])          
            try:
                ratio = round(dist / dist2, 1)
            except:
                ratio = round(dist / 0.01, 1)
            self.finger = self.finger << 1
            if ratio > 0.5:
                self.finger = self.finger | 1
                
    def get_gesture(self):
        if self.hand_result is None:
            return Gest.PALM
        
        current_gesture = Gest.PALM
        
        if self.finger in [Gest.LAST3, Gest.LAST4] and self.get_dist([8, 4]) < 0.05:
            if self.hand_label == HLabel.MINOR:
                current_gesture = Gest.PINCH_MINOR
            else:
                current_gesture = Gest.PINCH_MAJOR
        elif Gest.FIRST2 == self.finger:
            point = [[8, 12], [5, 9]]
            dist1 = self.get_dist(point[0])
            dist2 = self.get_dist(point[1])
            ratio = dist1 / dist2

            if ratio > 1.7:
                current_gesture = Gest.V_GEST
            else:
                if self.get_dz([8, 12]) < 0.1:
                    current_gesture = Gest.TWO_FINGER_CLOSED
                else:
                    current_gesture = Gest.MID
        else:
            current_gesture = self.finger
        
        if not hasattr(self, 'gesture_history'):
            self.gesture_history = []
            self.gesture_confidence = {}
            self.min_confidence_threshold = 3
            self.history_size = 7
        
        self.gesture_history.append(current_gesture)
        
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        gesture_counts = {}
        for gesture in self.gesture_history:
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        most_frequent_gesture = max(gesture_counts, key=gesture_counts.get)
        max_count = gesture_counts[most_frequent_gesture]
        
        if most_frequent_gesture in self.gesture_confidence:
            self.gesture_confidence[most_frequent_gesture] += 1
        else:
            self.gesture_confidence[most_frequent_gesture] = 1
            
        for gesture in list(self.gesture_confidence.keys()):
            if gesture != most_frequent_gesture:
                self.gesture_confidence[gesture] = max(0, self.gesture_confidence[gesture] - 0.5)
                if self.gesture_confidence[gesture] == 0:
                    del self.gesture_confidence[gesture]
        
        if (max_count >= 3 and  
            self.gesture_confidence.get(most_frequent_gesture, 0) >= self.min_confidence_threshold):
            
            if hasattr(self, 'ori_gesture') and self.ori_gesture != most_frequent_gesture:
                if self._gestures_are_similar(self.ori_gesture, most_frequent_gesture):
                    if self.gesture_confidence.get(most_frequent_gesture, 0) >= self.min_confidence_threshold + 2:
                        self.ori_gesture = most_frequent_gesture
                else:
                    self.ori_gesture = most_frequent_gesture
            else:
                self.ori_gesture = most_frequent_gesture
        
        if not hasattr(self, 'ori_gesture'):
            self.ori_gesture = Gest.PALM
        
        return self.ori_gesture
    
    def _gestures_are_similar(self, gesture1, gesture2):
        similar_groups = [
            [Gest.V_GEST, Gest.FIRST2, Gest.TWO_FINGER_CLOSED],
            [Gest.PINCH_MAJOR, Gest.PINCH_MINOR],
            [Gest.LAST3, Gest.LAST4]
        ]
        
        for group in similar_groups:
            if gesture1 in group and gesture2 in group:
                return True
        return False
    
    def get_gesture_simple_smooth(self):
        if self.hand_result is None:
            return Gest.PALM
        
        current_gesture = Gest.PALM
        
        if self.finger in [Gest.LAST3, Gest.LAST4] and self.get_dist([8, 4]) < 0.05:
            if self.hand_label == HLabel.MINOR:
                current_gesture = Gest.PINCH_MINOR
            else:
                current_gesture = Gest.PINCH_MAJOR
        elif Gest.FIRST2 == self.finger:
            point = [[8, 12], [5, 9]]
            dist1 = self.get_dist(point[0])
            dist2 = self.get_dist(point[1])
            ratio = dist1 / dist2
            if ratio > 1.7:
                current_gesture = Gest.V_GEST
            else:
                if self.get_dz([8, 12]) < 0.1:
                    current_gesture = Gest.TWO_FINGER_CLOSED
                else:
                    current_gesture = Gest.MID
        else:
            current_gesture = self.finger
        
        if current_gesture == self.prev_gesture:
            self.frame_count += 1
        else:
            self.frame_count = 0
        
        self.prev_gesture = current_gesture
        
        threshold = self._get_smoothing_threshold(current_gesture)
        
        if self.frame_count > threshold:
            self.ori_gesture = current_gesture
        
        return self.ori_gesture
    
    def _get_smoothing_threshold(self, gesture):
        sensitive_gestures = [Gest.PINCH_MAJOR, Gest.PINCH_MINOR, Gest.TWO_FINGER_CLOSED]
        
        if gesture in sensitive_gestures:
            return 6  
        elif gesture == Gest.PALM:
            return 2  
        else:
            return 4  