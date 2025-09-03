# Real-Time Speech Translation System For Video Calling

A Python-based real-time speech translation system that captures audio input, transcribes speech, translates it to a target language, synthesizes translated speech, and displays subtitles on video streams. Perfect for multilingual video calls and real-time communication.

## Features

- Real-time speech recognition using OpenAI's Whisper
- Multi-language translation powered by Google's Gemini AI
- Text-to-speech synthesis with Facebook's MMS-TTS models
- Live subtitle overlay on video streams
- Virtual camera support for video conferencing
- Thread-safe buffer management for audio/video synchronization
- GUI interface for easy language selection and configuration

## System Requirements

- Python 3.12
- CUDA-capable GPU with minimum 6GB Memory
- Microphone and camera
- Virtual camera software support
- Windows OS

## Setup

### Dependencies
`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu[Enter Cuda Version, e.g.129]`  
`pip install whisper`  
`pip install transformers`  
`pip install langchain langchain-google-genai`  
`pip install pyaudio`  
`pip install opencv-python`  
`pip install pyvirtualcam`  
`pip install pillow`  
`pip install numpy`  
`pip install tkinter`  

### Software to Install
- [OBS Studio](https://obsproject.com/)
- [VB-CABLE Virtual Audio Device](https://vb-audio.com/Cable/)

### Configure Video Calling App
- Go to settings
- Go to Video/Camera settings and under camera select **OBS Virtual Camera**
- Go to Audio settings and under microphone select **Cable Output (VB-Audio Virtual Cable)** 

## How to Run
- In a terminal run `python main.py` and a GUI will pop up
- Select the language you want to speak and the language you want outputed
- Select if you want to enable audio translation
- Hit confirm
- You can change languages and if translated audio is outputed by simply clicking confirm with your updated settings
