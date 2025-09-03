<H1>Real-Time Speech Translation System<H1>

A Python-based real-time speech translation system that captures audio input, transcribes speech, translates it to a target language, synthesizes translated speech, and displays subtitles on video streams. Perfect for multilingual video calls and real-time communication.

<H2>Features<H2>

Real-time speech recognition using OpenAI's Whisper
Multi-language translation powered by Google's Gemini AI
Text-to-speech synthesis with Facebook's MMS-TTS models
Live subtitle overlay on video streams
Virtual camera support for video conferencing
Thread-safe buffer management for audio/video synchronization
GUI interface for easy language selection and configuration

<H2>System Requirements<H2>

Python 3.8+
CUDA-capable GPU with minimum 6GB Memory
Microphone and camera
Virtual camera software support

<H2>Setup<H2>

<H3>Dependencies<H3>
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu[Enter Cuda Version, e.g.129]
pip install whisper
pip install transformers
pip install langchain langchain-google-genai
pip install pyaudio
pip install opencv-python
pip install pyvirtualcam
pip install pillow
pip install numpy
pip install tkinter
