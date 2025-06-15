# 🧠 PROTON - Desktop Voice Assistant
![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=for-the-badge)

**PROTON** is a smart desktop-based voice assistant developed in Python. It interacts through speech, executes system commands, navigates files, performs Google searches, fetches dates and locations, and more — all hands-free.

---

## 🌟 Features

- 🎙️ Voice recognition & response (text-to-speech)
- 📅 Fetch current date and time
- 🌐 Perform Google searches
- 🗺️ Get locations using Google Maps
- 🗂️ Navigate files and directories
- 📂 Read and list files in a folder
- 🖱️ Simulate keyboard/mouse actions (optional)
- 🎯 Interactive GUI for chat-like experience

---

## 🛠️ Tech Stack

- **Language**: Python
- **Speech Recognition**: `speech_recognition`
- **Text-to-Speech**: `pyttsx3`
- **GUI**: `tkinter`
- **Automation**: `pyautogui`, `keyboard`
- **Web Integration**: `webbrowser`, `wikipedia`
- **File/OS Access**: `os`, `datetime`, `threading`, etc.

---

## 🧪 How It Works

1. Launch the GUI.
2. Speak a command (e.g., "Proton, tell me the date of today").
3. Proton listens, processes, and responds accordingly.

---

## 🖼️ Demo Screenshots

### 1. 🗨️ Greeting and Date Fetching  
![Date Feature](./Screenshot%20(255).png)  
*Proton welcomes the user and responds with the current date using voice and text.*

---

### 2. 🗺️ Location Finder  
![Location Feature](./Screenshot%20(257).png)  
*User asks Proton to find a location. Proton searches and shows Bengaluru on Google Maps.*

---

### 3. 📂 File Directory Access  
![File Navigation](./Screenshot%20(258).png)  
*Proton lists files from the root directory using voice commands like `proton list`.*

---

### 4. 🔍 Google Search with Voice  
![Google Search](./Screenshot%20(256).png)  
*Proton performs a voice-triggered Google search like `proton search github`.*

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Proton-Voice-Assistant.git
   cd Proton-Voice-Assistant

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the assistant:
   ```bash
   python src/Proton.py
---
## 📁 Project Structure
    ```bash
        Proton-Voice-Assistant/
    ├── demo_media/             # Screenshots, recordings, etc.
    ├── src/                    # Main source code files
    │   ├── Proton.py           # Core logic for the voice assistant
    │   └── app.py              # Optional GUI handling or other components
    ├── requirements.txt
    └── README.md
---

##  🙌 Credits
- Voice & speech libraries: speech_recognition, pyttsx3
- GUI: tkinter
- Tools: keyboard, pyautogui, webbrowser, os, threading

---

## 📌 Future Improvements

1. Add weather & news APIs
2. Integrate chatbot (e.g., GPT)
3. Multilingual support
4. Add commands for controlling apps (e.g., VSCode, Spotify).
---

## 🧑‍💻 Developed by

Harvinder Kaur

Final Year Student | Python & AI Enthusiast


