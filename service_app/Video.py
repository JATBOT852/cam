import cv2
import time
import threading
from playsound import playsound

class FaceDetectionApp:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    timers = {"left": None, "right": None, "upward": None, "downward": None}
    alert_duration = 5  # Duration in seconds for detecting suspicious activity
    beep_played = {"left": False, "right": False, "upward": False, "downward": False}
    path_to_warning_mp3 = r"beep-warning-6387 (1).mp3"

    @staticmethod
    def initialize_audio():
        try:
            print("Audio system initialized successfully.")
        except Exception as e:
            print(f"Error initializing audio system: {e}")

    @staticmethod
    def detect_face_orientation(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FaceDetectionApp.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            FaceDetectionApp.reset_timers()
            return "No Face Detected", None

        FaceDetectionApp.beep_played.update({"left": False, "right": False, "upward": False, "downward": False})

        face_rect = faces[0]
        x, y, w, h = face_rect

        screen_center_x = frame.shape[1] // 2
        screen_center_y = frame.shape[0] // 2

        x_threshold = 100  # Adjust thresholds based on actual needs
        y_threshold = 100

        # Determine the face's position relative to the center
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        if face_center_x < screen_center_x - x_threshold:  # Left
            status = FaceDetectionApp.check_movement_timer("left")
            cv2.putText(frame, "Move Left", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif face_center_x > screen_center_x + x_threshold:  # Right
            status = FaceDetectionApp.check_movement_timer("right")
            cv2.putText(frame, "Move Right", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif face_center_y < screen_center_y - y_threshold:  # Upward
            status = FaceDetectionApp.check_movement_timer("upward")
            cv2.putText(frame, "Move Upward", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif face_center_y > screen_center_y + y_threshold:  # Downward
            status = FaceDetectionApp.check_movement_timer("downward")
            cv2.putText(frame, "Move Downward", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            FaceDetectionApp.reset_timers()
            status = "Face Centered"
            cv2.putText(frame, "Face Centered", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return status, face_rect

    @staticmethod
    def check_movement_timer(direction):
        if FaceDetectionApp.timers[direction] is None:
            FaceDetectionApp.timers[direction] = time.time()
            return "Normal"
        else:
            elapsed_time = time.time() - FaceDetectionApp.timers[direction]
            if elapsed_time > FaceDetectionApp.alert_duration:
                if not FaceDetectionApp.beep_played[direction]:
                    FaceDetectionApp.play_long_beep(direction)
                    FaceDetectionApp.beep_played[direction] = True
                FaceDetectionApp.timers[direction] = None  # Reset timer
                return "Suspicious"
            else:
                return "Normal"

    @staticmethod
    def reset_timers():
        for direction in FaceDetectionApp.timers:
            FaceDetectionApp.timers[direction] = None

    @staticmethod
    def play_long_beep(activity):
        def beep():
            try:
                playsound(FaceDetectionApp.path_to_warning_mp3)
                print(f"Long beep sound played for {activity}.")
            except Exception as e:
                print(f"Error playing sound: {e}")

        beep_thread = threading.Thread(target=beep)
        beep_thread.start()

    @staticmethod
    def genarate_video():
        FaceDetectionApp.initialize_audio()
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Camera not found or failed to open.")
            return
        
        while True:
            success, frame = cap.read()
            if not success:
                print("Error: Failed to capture image.")
                break
            
            status, face_rect = FaceDetectionApp.detect_face_orientation(frame)

            if face_rect is not None:
                x, y, w, h = face_rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.putText(frame, f"Status: {status}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    FaceDetectionApp.genarate_video()

