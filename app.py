import os
import azure.cognitiveservices.speech as speechsdk
import pyautogui
import mediapipe as mp
import cv2
import time
import math
import threading

# Azure Speech-to-Text Configuration
speech_key = "YOUR-SPEECH-API-KEY"
region = "YOUR-LOCATION"

# Initialize MediaPipe for gesture recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam capture for gesture recognition
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Failed to open webcam. Exiting...")
    exit()
else:
    print("Webcam initialized successfully.")

# Global flag for thread termination
terminate_flag = threading.Event()

# Function to process voice commands
def process_command(command):
    print(f"Processing command: {command}")
    command = command.lower()

    try:
        if "open" in command:
            if "chrome" in command:
                os.system("start chrome")  # Open Google Chrome
            elif "notepad" in command:
                os.system("start notepad")  # Open Notepad
            elif "file explorer" in command:
                os.system("explorer")  # Open File Explorer

        elif "close" in command:
            os.system("taskkill /f /im chrome.exe")  # Example for closing Chrome (modify as needed)
            # Note: Taskkill can force-close specific apps by their process name.
            # Replace 'chrome.exe' with the respective app's process name.

        else:
            pyautogui.write(command + " ")  # Keep the typing functionality intact

        print(f"Command processed successfully: {command}")
    except Exception as e:
        print(f"Error processing command: {e}")
# Function for continuous speech recognition using Azure SDK
def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    while not terminate_flag.is_set():
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
            process_command(speech_recognition_result.text)
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

# MediaPipe gesture recognition function
def media_pipe_gestures():
    print("Starting gesture recognition...")
    screen_width, screen_height = pyautogui.size()
    prev_smoothed_x, prev_smoothed_y = None, None
    margin = 30
    click_timeout = 0.05
    click_start_time = None

    while not terminate_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from webcam.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                screen_x = int(index_finger_tip.x * screen_width)
                screen_y = int(index_finger_tip.y * screen_height)

                screen_x = max(min(screen_x, screen_width - margin), margin)
                screen_y = max(min(screen_y, screen_height - margin), margin)

                smoothing_factor = 0.3
                if prev_smoothed_x is None or prev_smoothed_y is None:
                    prev_smoothed_x, prev_smoothed_y = screen_x, screen_y
                smoothed_x = int(prev_smoothed_x * (1 - smoothing_factor) + screen_x * smoothing_factor)
                smoothed_y = int(prev_smoothed_y * (1 - smoothing_factor) + screen_y * smoothing_factor)

                pyautogui.moveTo(smoothed_x, smoothed_y)
                prev_smoothed_x, prev_smoothed_y = smoothed_x, smoothed_y

                distance = calculate_distance(index_finger_tip, thumb_tip)
                if distance < 0.1:
                    if click_start_time is None:
                        click_start_time = time.time()
                else:
                    click_start_time = None

                if click_start_time and time.time() - click_start_time > click_timeout:
                    pyautogui.click()
                    click_start_time = None

        cv2.imshow("MediaPipe Hands", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            terminate_flag.set()
            break

    print("Exiting gesture recognition...")

# Function to calculate the Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Cleanup function
def cleanup():
    print("Cleaning up resources...")
    terminate_flag.set()
    cap.release()
    hands.close()
    cv2.destroyAllWindows()

# Main function
def main():
    print("Starting system...")

    speech_thread = threading.Thread(target=recognize_from_microphone, daemon=True)
    mediapipe_thread = threading.Thread(target=media_pipe_gestures, daemon=True)

    speech_thread.start()
    mediapipe_thread.start()

    try:
        while not terminate_flag.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping system...")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
