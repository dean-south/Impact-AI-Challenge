import pyaudio
import threading
import numpy as np

class InputAudio:
    def __init__(self, memory):
        self.memory = memory
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 16000

        self.data = None
        self.stop = False

        self.p = pyaudio.PyAudio()

        # Open input stream (microphone)
        self.input_stream = self.p.open(format=self.FORMAT,
                                        channels=self.CHANNELS,
                                        rate=self.RATE,
                                        input=True,
                                        frames_per_buffer=self.CHUNK,
                                        input_device_index=1)


    def start(self):
        # Start the update thread
        print("Starting audio input stream...")
        self.stream_thread = threading.Thread(target=self.update, args=(), daemon=True)
        self.stream_thread.start()


    def stop_stream(self):
        # Clean up resources
        self.stop = True
        self.input_stream.stop_stream()
        self.input_stream.close()
        self.p.terminate()


    def update(self):
        while not self.stop:        
            self.data = self.input_stream.read(self.CHUNK)
            self.memory.add_input_audio(np.frombuffer(self.data, dtype=np.float32))