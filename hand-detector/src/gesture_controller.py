class GestureController:
    # Class variables
    gc_mode = 0
    cap = None
    CAM_HEIGHT = None
    CAM_WIDTH = None
    hr_major = None  # Right Hand by default
    hr_minor = None  # Left hand by default 
    dom_hand = True

    def __init__(self):
        """Initialize camera and window settings"""
        GestureController.gc_mode = 1
        GestureController.cap = cv2.VideoCapture(0)
        
        if not GestureController.cap.isOpened():
            print("❌ Webcam could not be opened.")
            return
            
        GestureController.CAM_HEIGHT = GestureController.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        GestureController.CAM_WIDTH = GestureController.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    @staticmethod
    def classify_hands(results):
        """Classify detected hands as left or right"""
        left, right = None, None
        try:
            # Process first hand
            handedness_dict = MessageToDict(results.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[0]
            else:
                left = results.multi_hand_landmarks[0]
        except:
            pass
            
        try:
            # Process second hand if present
            handedness_dict = MessageToDict(results.multi_handedness[1])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[1]
            else:
                left = results.multi_hand_landmarks[1]
        except:
            pass

        # Assign hands based on dominance setting
        if GestureController.dom_hand:
            GestureController.hr_major = right
            GestureController.hr_minor = left
        else:
            GestureController.hr_major = left
            GestureController.hr_minor = right

    def start(self):
        """Main loop for hand gesture detection and control"""
        handmajor = HandRecog(HLabel.MAJOR)
        handminor = HandRecog(HLabel.MINOR)

        with mp_hands.Hands(max_num_hands=2, 
                          min_detection_confidence=0.5, 
                          min_tracking_confidence=0.5) as hands:
            while GestureController.cap.isOpened() and GestureController.gc_mode:
                success, image = GestureController.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                    
                # Process image
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Handle detected hands
                if results.multi_hand_landmarks:
                    GestureController.classify_hands(results)
                    handmajor.update_hand_result(GestureController.hr_major)
                    handminor.update_hand_result(GestureController.hr_minor)
                    
                    # Process gestures
                    handmajor.set_finger_state()
                    handminor.set_finger_state()
                    gest_name = handminor.get_gesture()
                    
                    # Handle controls based on detected gestures
                    if gest_name == Gest.PINCH_MINOR:
                        Controller.handle_controls(gest_name, handminor.hand_result)
                    else:
                        gest_name = handmajor.get_gesture()
                        Controller.handle_controls(gest_name, handmajor.hand_result)

                    # Draw hand landmarks
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, 
                                               mp_hands.HAND_CONNECTIONS)
                else:
                    Controller.prev_hand = None

                # Display output
                cv2.imshow('Virtual Mouse Gesture Controller', image)
                if cv2.waitKey(5) & 0xFF == 13:  # Exit on Enter key
                    break

        # Cleanup
        GestureController.cap.release()
        cv2.destroyAllWindows()