import pyaudio
import threading
import time
import numpy as np


class OutputAudio:
    def __init__(self, input_audio, memory, translated_audio=True, device_idx=20):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.input_audio = input_audio
        self.stop = False
        self.p = pyaudio.PyAudio()
        self.memory = memory
        self.translated_audio = translated_audio

        print(f'{self.CHANNELS=}')

        # Open output stream (speakers)
        self.output_stream = self.p.open(format=self.FORMAT,
                                         channels=self.CHANNELS,
                                         rate=self.RATE,
                                         output=True,
                                        #  input=True,
                                         frames_per_buffer=self.CHUNK,
                                         output_device_index=device_idx)
        

    def play_audio(self):
        while not self.stop:
            audio_data = self.memory.get_output_audio() if self.translated_audio is not None else self.input_audio.data

            # print(f"Output audio chunk size: {len(audio_data)}")
            if audio_data is not None:
                if self.translated_audio:
                    audio_data = (audio_data * 32767).astype(np.int16).tobytes()

                for i in range(0, len(audio_data), self.CHUNK):
                    chunk = audio_data[i:i + self.CHUNK]

                    self.output_stream.write(chunk)
            
            time.sleep(0.01)

    
    # def use_translated_audio(self, use_trans_audio):
    #     self.translated_audio = use_trans_audio


    def start(self):
        self.stop = False
        print("Starting audio output stream...")
        threading.Thread(target=self.play_audio, args=(), daemon=True).start()

    def stop_stream(self):
        # Clean up resources
        self.stop = True
        self.output_stream.stop_stream()
        self.output_stream.close()
        self.p.terminate()