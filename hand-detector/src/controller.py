class Controller:
    last_right_click = 0
    tx_old = 0
    ty_old = 0
    brightness_val = 50
    trial = True
    flag = False
    grabflag = False
    pinchmajorflag = False
    pinchminorflag = False
    pinchstartxcoord = None
    pinchstartycoord = None
    pinchdirectionflag = None
    prevpinchlv = 0
    pinchlv = 0
    framecount = 0
    prev_hand = None
    pinch_threshold = 0.3

    @staticmethod
    def get_pinch_y_level(hand_result):
        dist = round((Controller.pinchstartycoord - hand_result.landmark[8].y) * 10, 1)
        return dist

    @staticmethod
    def get_pinch_x_level(hand_result):
        dist = round((hand_result.landmark[8].x - Controller.pinchstartxcoord) * 10, 1)
        return dist

    @staticmethod
    def change_system_brightness():
        import time
        current_time = time.time()

        if current_time - smooth_control.last_brightness_change < smooth_control.brightness_cooldown:
            return

        smooth_control.brightness_history.append(Controller.pinchlv)

        if len(smooth_control.brightness_history) > smooth_control.history_size:
            smooth_control.brightness_history.pop(0)

        if len(smooth_control.brightness_history) >= 2:
            weights = [0.3, 0.7] if len(smooth_control.brightness_history) == 2 else [0.2, 0.3, 0.5]
            smoothed_pinchlv = sum(val * weight for val, weight in zip(smooth_control.brightness_history, weights))
        else:
            smoothed_pinchlv = Controller.pinchlv

        if abs(smoothed_pinchlv) < 0.02:
            return

        try:
            currentBrightnessLv = sbcontrol.get_brightness()[0] / 100.0
            newBrightnessLv = currentBrightnessLv + (smoothed_pinchlv / 50.0)

            if newBrightnessLv > 1.0:
                newBrightnessLv = 1.0
            elif newBrightnessLv < 0.0:
                newBrightnessLv = 0.0

            if smooth_control.last_applied_brightness is None or abs(newBrightnessLv - smooth_control.last_applied_brightness) > 0.03:
                sbcontrol.fade_brightness(int(100 * newBrightnessLv), start=sbcontrol.get_brightness()[0])
                smooth_control.last_applied_brightness = newBrightnessLv
                smooth_control.last_brightness_change = current_time

        except Exception as e:
            print(f"Brightness control error: {e}")

    @staticmethod
    def change_system_volume():
        import time
        current_time = time.time()

        if current_time - smooth_control.last_volume_change < smooth_control.volume_cooldown:
            return

        smooth_control.volume_history.append(Controller.pinchlv)

        if len(smooth_control.volume_history) > smooth_control.history_size:
            smooth_control.volume_history.pop(0)

        if len(smooth_control.volume_history) >= 2:
            weights = [0.3, 0.7] if len(smooth_control.volume_history) == 2 else [0.2, 0.3, 0.5]
            smoothed_pinchlv = sum(val * weight for val, weight in zip(smooth_control.volume_history, weights))
        else:
            smoothed_pinchlv = Controller.pinchlv

        if abs(smoothed_pinchlv) < 0.02:
            return

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            currentVolumeLv = volume.GetMasterVolumeLevelScalar()
            newVolumeLv = currentVolumeLv + (smoothed_pinchlv / 50.0)

            if newVolumeLv > 1.0:
                newVolumeLv = 1.0
            elif newVolumeLv < 0.0:
                newVolumeLv = 0.0

            if smooth_control.last_applied_volume is None or abs(newVolumeLv - smooth_control.last_applied_volume) > 0.03:
                volume.SetMasterVolumeLevelScalar(newVolumeLv, None)
                smooth_control.last_applied_volume = newVolumeLv
                smooth_control.last_volume_change = current_time

        except Exception as e:
            print(f"Volume control error: {e}")

    @staticmethod
    def scroll_vertical():
        import time
        current_time = time.time()

        if current_time - smooth_control.last_scroll_change < smooth_control.scroll_cooldown:
            return

        smooth_control.scroll_history.append(Controller.pinchlv)

        if len(smooth_control.scroll_history) > smooth_control.history_size:
            smooth_control.scroll_history.pop(0)

        if len(smooth_control.scroll_history) >= 2:
            weights = [0.3, 0.7] if len(smooth_control.scroll_history) == 2 else [0.2, 0.3, 0.5]
            smoothed_pinchlv = sum(val * weight for val, weight in zip(smooth_control.scroll_history, weights))
        else:
            smoothed_pinchlv = Controller.pinchlv

        if abs(smoothed_pinchlv) < 0.1:
            return

        try:
            scroll_amount = int(120 * abs(smoothed_pinchlv) / 0.5)
            scroll_amount = max(60, min(240, scroll_amount))

            pyautogui.scroll(scroll_amount if smoothed_pinchlv > 0.0 else -scroll_amount)
            smooth_control.last_scroll_change = current_time

        except Exception as e:
            print(f"Scroll control error: {e}")

    @staticmethod
    def scroll_horizontal():
        import time
        current_time = time.time()

        if current_time - smooth_control.last_scroll_change < smooth_control.scroll_cooldown:
            return

        smooth_control.scroll_history.append(Controller.pinchlv)

        if len(smooth_control.scroll_history) > smooth_control.history_size:
            smooth_control.scroll_history.pop(0)

        if len(smooth_control.scroll_history) >= 2:
            weights = [0.3, 0.7] if len(smooth_control.scroll_history) == 2 else [0.2, 0.3, 0.5]
            smoothed_pinchlv = sum(val * weight for val, weight in zip(smooth_control.scroll_history, weights))
        else:
            smoothed_pinchlv = Controller.pinchlv

        if abs(smoothed_pinchlv) < 0.1:
            return

        try:
            scroll_amount = int(120 * abs(smoothed_pinchlv) / 0.5)
            scroll_amount = max(60, min(240, scroll_amount))

            pyautogui.keyDown('shift')
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-scroll_amount if smoothed_pinchlv > 0.0 else scroll_amount)
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('shift')
            smooth_control.last_scroll_change = current_time

        except Exception as e:
            print(f"Horizontal scroll control error: {e}")

    @staticmethod
    def reset_smooth_controls():
        smooth_control.brightness_history.clear()
        smooth_control.volume_history.clear()
        smooth_control.scroll_history.clear()
        smooth_control.last_applied_brightness = None
        smooth_control.last_applied_volume = None

    @staticmethod
    def get_position(hand_result):
        point = 9
        position = [hand_result.landmark[point].x, hand_result.landmark[point].y]
        sx, sy = pyautogui.size()
        x_old, y_old = pyautogui.position()
        x = int(position[0] * sx)
        y = int(position[1] * sy)
        if Controller.prev_hand is None:
            Controller.prev_hand = x, y
        delta_x = x - Controller.prev_hand[0]
        delta_y = y - Controller.prev_hand[1]
        distsq = delta_x ** 2 + delta_y ** 2
        ratio = 1
        Controller.prev_hand = [x, y]
        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** (1 / 2))
        else:
            ratio = 2.1
        x, y = x_old + delta_x * ratio, y_old + delta_y * ratio
        return (x, y)

    @staticmethod
    def pinch_control_init(hand_result):
        Controller.pinchstartxcoord = hand_result.landmark[8].x
        Controller.pinchstartycoord = hand_result.landmark[8].y
        Controller.pinchlv = 0
        Controller.prevpinchlv = 0
        Controller.framecount = 0

    @staticmethod
    def pinch_control(hand_result, controlHorizontal, controlVertical):
        if Controller.framecount == 5:
            Controller.framecount = 0
            Controller.pinchlv = Controller.prevpinchlv

            if Controller.pinchdirectionflag is True:
                controlHorizontal()

            elif Controller.pinchdirectionflag is False:
                controlVertical()

        lvx = Controller.get_pinch_x_level(hand_result)
        lvy = Controller.get_pinch_y_level(hand_result)
        if abs(lvy) > abs(lvx) and abs(lvy) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = False
            if abs(Controller.prevpinchlv - lvy) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvy
                Controller.framecount = 0

        elif abs(lvx) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = True
            if abs(Controller.prevpinchlv - lvx) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvx
                Controller.framecount = 0

    @staticmethod
    def handle_controls(gesture, hand_result):
        x, y = None, None
        if gesture != Gest.PALM:
            x, y = Controller.get_position(hand_result)

        if gesture != Gest.FIST and Controller.grabflag:
            Controller.grabflag = False
            pyautogui.mouseUp(button="left")
        if gesture != Gest.PINCH_MAJOR and Controller.pinchmajorflag:
            Controller.pinchmajorflag = False
        if gesture != Gest.PINCH_MINOR and Controller.pinchminorflag:
            Controller.pinchminorflag = False

        if gesture == Gest.V_GEST:
            Controller.flag = True
            pyautogui.moveTo(x, y, duration=0.1)
        elif gesture == Gest.FIST:
            if not Controller.grabflag:
                Controller.grabflag = True
                pyautogui.mouseDown(button="left")
            pyautogui.moveTo(x, y, duration=0.1)
        elif gesture == Gest.MID and Controller.flag:
            pyautogui.click()
            Controller.flag = False
        elif gesture == Gest.INDEX and Controller.flag:
            if time.time() - Controller.last_right_click > 1:
                pyautogui.click(button='right')
                Controller.last_right_click = time.time()
            Controller.flag = False
        elif gesture == Gest.TWO_FINGER_CLOSED and Controller.flag:
            pyautogui.doubleClick()
            Controller.flag = False
        elif gesture == Gest.PINCH_MINOR:
            if Controller.pinchminorflag is False:
                Controller.pinch_control_init(hand_result)
                Controller.pinchminorflag = True
            Controller.pinch_control(hand_result, Controller.scroll_horizontal, Controller.scroll_vertical)
        elif gesture == Gest.PINCH_MAJOR:
            if Controller.pinchmajorflag is False:
                Controller.pinch_control_init(hand_result)
                Controller.pinchmajorflag = True
            Controller.pinch_control(hand_result, Controller.change_system_brightness, Controller.change_system_volume)