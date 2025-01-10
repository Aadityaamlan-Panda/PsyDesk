import os
import azure.cognitiveservices.speech as speechsdk
import pyautogui
import mediapipe as mp
import cv2
import time
import math
import threading
import tkinter as tk

# Azure Speech-to-Text Configuration
speech_key = "YOUR-SPEECH-API-KEY"
region = "YOUR-SPEECH-REGION"

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
speech_terminate_flag = threading.Event()
gesture_terminate_flag = threading.Event()

speech_thread = None
gesture_thread = None

# Function to process voice commands
import os
import pyautogui
import subprocess

# Predefined list of common programs with their corresponding executable commands
COMMON_PROGRAMS = {
    # Browsers
    "chrome": "chrome",  # Google Chrome
    "firefox": "firefox",  # Mozilla Firefox
    "edge": "msedge",  # Microsoft Edge
    "opera": "opera",  # Opera Browser
    "safari": "safari",  # Safari (if installed)

    # Text Editors
    "notepad": "notepad",  # Notepad
    "notepad++": "notepad++",  # Notepad++
    "visual studio code": "Code",  # VS Code
    "sublime text": "sublime_text",  # Sublime Text
    "atom": "atom",  # Atom Editor

    # Office Suite
    "word": "winword",  # Microsoft Word
    "excel": "excel",  # Microsoft Excel
    "powerpoint": "powerpnt",  # Microsoft PowerPoint
    "onenote": "onenote",  # Microsoft OneNote
    "outlook": "outlook",  # Microsoft Outlook
    "access": "msaccess",  # Microsoft Access
    "visio": "visio",  # Microsoft Visio
    "publisher": "mspub",  # Microsoft Publisher

    # Communication and Collaboration
    "skype": "skype",  # Skype
    "zoom": "zoom",  # Zoom
    "slack": "slack",  # Slack
    "teams": "teams",  # Microsoft Teams
    "discord": "discord",  # Discord
    "microsoft teams meeting add-in": "TeamsAddin",  # Microsoft Teams Meeting Add-in for Office

    # Cloud Storage and Sync
    "onedrive": "OneDrive",  # Microsoft OneDrive
    "google drive": "googledrivesync",  # Google Drive (Backup & Sync)
    "dropbox": "Dropbox",  # Dropbox
    "box": "Box",  # Box
    "pcloud": "pcloud",  # pCloud

    # File Management and Utilities
    "file explorer": "explorer",  # File Explorer
    "winrar": "winrar",  # WinRAR
    "7zip": "7zFM",  # 7-Zip File Manager
    "adobe acrobat reader": "acrord32",  # Adobe Acrobat Reader
    "vlc": "vlc",  # VLC Media Player
    "paint": "mspaint",  # Microsoft Paint
    "photoshop": "photoshop",  # Adobe Photoshop
    "gimp": "gimp",  # GIMP
    "lightroom": "lightroom",  # Adobe Lightroom

    # Media Players
    "windows media player": "wmplayer",  # Windows Media Player
    "itunes": "itunes",  # iTunes
    "spotify": "spotify",  # Spotify
    "pandora": "pandora",  # Pandora
    "grooveshark": "grooveshark",  # Grooveshark (if installed)

    # Developer Tools
    "visual studio": "devenv",  # Visual Studio
    "android studio": "studio64",  # Android Studio
    "xcode": "xcode",  # Xcode (if available on Windows through emulation or WSL)
    "eclipse": "eclipse",  # Eclipse IDE
    "pycharm": "pycharm",  # PyCharm
    "intellij idea": "idea",  # IntelliJ IDEA
    "netbeans": "netbeans",  # NetBeans

    # Gaming Platforms
    "steam": "steam",  # Steam
    "epic games": "EpicGamesLauncher",  # Epic Games Launcher
    "origin": "origin",  # Origin (by EA)
    "ubisoft connect": "Uplay",  # Ubisoft Connect
    "battle.net": "battle.net",  # Battle.net (Blizzard)
    "gog galaxy": "GOG Galaxy",  # GOG Galaxy

    # Graphics and Animation
    "blender": "blender",  # Blender
    "autocad": "acad",  # AutoCAD
    "solidworks": "sldworks",  # SolidWorks
    "unity": "unity",  # Unity 3D
    "maya": "maya",  # Autodesk Maya
    "cinema 4d": "c4d",  # Cinema 4D

    # Virtualization and Docker
    "virtualbox": "VirtualBox",  # Oracle VirtualBox
    "vmware": "vmware",  # VMware Workstation
    "docker": "docker",  # Docker Desktop
    "hyper-v": "vmms",  # Hyper-V Manager

    # Web Servers and Databases
    "xamp": "xampp-control.exe",  # XAMPP Control Panel
    "wamp": "wampmanager.exe",  # WAMP Server
    "mysql workbench": "mysql-workbench",  # MySQL Workbench
    "postgresql": "pgAdmin4",  # PostgreSQL (pgAdmin)
    "mongodb compass": "mongodb-compass",  # MongoDB Compass

    # System Utilities
    "task manager": "taskmgr",  # Task Manager
    "command prompt": "cmd",  # Command Prompt
    "powershell": "powershell",  # PowerShell
    "msconfig": "msconfig",  # System Configuration
    "registry editor": "regedit",  # Registry Editor
    "device manager": "devmgmt.msc",  # Device Manager
    "disk cleanup": "cleanmgr",  # Disk Cleanup

    # Antivirus and Security
    "norton": "norton",  # Norton Antivirus
    "avast": "avast",  # Avast Antivirus
    "bitdefender": "bitdefender",  # Bitdefender
    "windows defender": "msascui",  # Windows Defender

    # Miscellaneous
    "notion": "notion",  # Notion
    "evernote": "evernote",  # Evernote
    "trello": "trello",  # Trello
    "discord": "discord",  # Discord
    "skype": "skype",  # Skype

    # Your Apps
    "python 3.9": "python3.9",  # Python 3.9
    "python 3.10": "python3.10",  # Python 3.10
    "python 3.13": "python3.13",  # Python 3.13
    "autodesk save to web and mobile": "SaveToWebMobile",  # Autodesk Save to Web and Mobile
    "autodesk app manager": "AutodeskAppManager",  # Autodesk App Manager
    "davinci resolve": "DaVinciResolve",  # DaVinci Resolve
    "autocad": "acad",  # AutoCAD
    "autodesk genuine service": "AutodeskGenuineService",  # Autodesk Genuine Service
    "autodesk material library": "AutodeskMaterialLibrary",  # Autodesk Material Library
    "autodesk single sign on component": "AutodeskSingleSignOn",  # Autodesk Single Sign On Component
    "vmware player": "vmware",  # VMware Player
    "oracle vm virtualbox": "VirtualBox",  # Oracle VM VirtualBox
    "python launcher": "python_launcher",  # Python Launcher
    "python 3.9 pip bootstrap": "pip",  # Python 3.9 pip Bootstrap
    "python 3.10 pip bootstrap": "pip",  # Python 3.10 pip Bootstrap
    "python 3.9.0 executables": "python",  # Python 3.9 Executables
    "python 3.10.0 executables": "python",  # Python 3.10 Executables
    "python 3.13.1 executables": "python",  # Python 3.13 Executables
    "skype click to call": "skype",  # Skype Click-to-Call
    "blackmagic raw common components": "blackmagic",  # Blackmagic RAW Common Components
    "node.js": "node",  # Node.js
    "autodesk inventor interoperability": "InventorInteroperability",  # Autodesk Inventor Interoperability
}


def process_command(command):
    """Process the user command to open or close a program."""
    print(f"Processing command: {command}")
    command = command.lower()

    try:
        if "open" in command:
            matched_program = None
            for program, executable in COMMON_PROGRAMS.items():
                if program in command:
                    matched_program = executable
                    break

            if matched_program:
                print(f"Opening {matched_program}...")
                subprocess.run(["start", matched_program], shell=True, check=True)  # Open the program
            else:
                print("Program not found in predefined list.")
        
        elif "close" in command:
            matched_program = None
            for program, executable in COMMON_PROGRAMS.items():
                if program in command:
                    matched_program = executable
                    break

            if matched_program:
                print(f"Closing {matched_program}...")
                subprocess.run(["taskkill", "/f", "/im", f"{matched_program}.exe"], check=True)  # Close the program
            else:
                print("Program not found in predefined list.")
        
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
    while not speech_terminate_flag.is_set():
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
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam. Exiting...")
        return
    
    print("Starting gesture recognition...")
    screen_width, screen_height = pyautogui.size()
    prev_smoothed_x, prev_smoothed_y = None, None
    margin = 30
    click_timeout = 0.05
    click_start_time = None

    prev_index_y = None  # To track the previous Y-position of the index finger
    prev_middle_y = None  # To track the previous Y-position of the middle finger
    scrolling_active = False  # Flag to track if scrolling should be active

    cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("MediaPipe Hands", 800, 600)

    while not gesture_terminate_flag.is_set():
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

                # Get the index and middle finger tips
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                # Calculate the Euclidean distance between index and middle finger tips
                distance = calculate_distance(index_finger_tip, middle_finger_tip)

                # Check if fingers are joined (distance is small enough)
                if distance < 0.07:  # Threshold for detecting "joined" fingers
                    scrolling_active = True
                else:
                    scrolling_active = False

                # If scrolling is active (fingers are joined)
                if scrolling_active:
                    if prev_index_y is not None and prev_middle_y is not None:
                        # Track the vertical (Y-axis) movement of both fingers
                        index_finger_movement = index_finger_tip.y - prev_index_y
                        middle_finger_movement = middle_finger_tip.y - prev_middle_y

                        # If both fingers are moving up
                        if index_finger_movement < -0.01:  # Moving up
                            pyautogui.scroll(-100)  # Scroll up
                        # If both fingers are moving down
                        elif index_finger_movement > 0.01:  # Moving down
                            pyautogui.scroll(+100)  # Scroll down

                # Update previous positions
                prev_index_y = index_finger_tip.y
                prev_middle_y = middle_finger_tip.y

                # Additional movement (cursor tracking)
                index_finger_x = int(index_finger_tip.x * screen_width)
                index_finger_y = int(index_finger_tip.y * screen_height)

                # Smoothing the cursor movement
                screen_x = max(min(index_finger_x, screen_width - margin), margin)
                screen_y = max(min(index_finger_y, screen_height - margin), margin)

                smoothing_factor = 0.4
                if prev_smoothed_x is None or prev_smoothed_y is None:
                    prev_smoothed_x, prev_smoothed_y = screen_x, screen_y
                smoothed_x = int(prev_smoothed_x * (1 - smoothing_factor) + screen_x * smoothing_factor)
                smoothed_y = int(prev_smoothed_y * (1 - smoothing_factor) + screen_y * smoothing_factor)

                pyautogui.moveTo(smoothed_x, smoothed_y)
                prev_smoothed_x, prev_smoothed_y = smoothed_x, smoothed_y

                distance_finger_tip = calculate_distance(index_finger_tip, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP])
                if distance_finger_tip < 0.1:
                    if click_start_time is None:
                        click_start_time = time.time()
                else:
                    click_start_time = None

                if click_start_time and time.time() - click_start_time > click_timeout:
                    pyautogui.click()
                    click_start_time = None

        cv2.imshow("MediaPipe Hands", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gesture_terminate_flag.set()
            break

    print("Exiting gesture recognition...")
    cap.release()
    cv2.destroyWindow("MediaPipe Hands")

# Function to calculate the Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Cleanup function
def cleanup():
    print("Cleaning up resources...")
    # Set the flags to stop both threads
    speech_terminate_flag.set()
    gesture_terminate_flag.set()
    
    # Wait for both threads to finish if they're still running
    if speech_thread:
        speech_thread.join()
    
    if gesture_thread:
        gesture_thread.join()

    # Release resources
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
    print("Cleanup completed.")


# Functions to control threads
def start_speech_recognition():
    global speech_thread
    if not speech_thread or not speech_thread.is_alive():
        speech_terminate_flag.clear()
        speech_thread = threading.Thread(target=recognize_from_microphone, daemon=True)
        speech_thread.start()

def stop_speech_recognition():
    speech_terminate_flag.set()
    if speech_thread:
        speech_thread.join()

def start_gesture_recognition():
    global gesture_thread
    if not gesture_thread or not gesture_thread.is_alive():
        gesture_terminate_flag.clear()
        gesture_thread = threading.Thread(target=media_pipe_gestures, daemon=True)
        gesture_thread.start()

def stop_gesture_recognition():
    gesture_terminate_flag.set()
    if gesture_thread:
        gesture_thread.join()

# Tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Control Panel")

    speech_label = tk.Label(root, text="Speech Recognition", font=("Arial", 14))
    speech_label.pack(pady=5)

    start_speech_btn = tk.Button(root, text="Start Speech Recognition", command=start_speech_recognition, width=25)
    start_speech_btn.pack(pady=5)

    stop_speech_btn = tk.Button(root, text="Stop Speech Recognition", command=stop_speech_recognition, width=25)
    stop_speech_btn.pack(pady=5)

    gesture_label = tk.Label(root, text="Gesture Recognition", font=("Arial", 14))
    gesture_label.pack(pady=5)

    start_gesture_btn = tk.Button(root, text="Start Gesture Recognition", command=start_gesture_recognition, width=25)
    start_gesture_btn.pack(pady=5)

    stop_gesture_btn = tk.Button(root, text="Stop Gesture Recognition", command=stop_gesture_recognition, width=25)
    stop_gesture_btn.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", cleanup)
    root.mainloop()

# Main function
def main():
    create_gui()

if __name__ == "__main__":
    main()
