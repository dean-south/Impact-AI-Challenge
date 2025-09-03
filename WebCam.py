import cv2
import threading
import time
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class WebCame:
    def __init__(self, memory, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        self.memory = memory

        self.stop = False

    def start(self):
        self.stop = False
        print("Starting video stream...")
        threading.Thread(target=self.update, args=()).start()


    def update(self):
        while not self.stop:
            ret, frame = self.stream.read()
            if not ret:
                break

            text = self.memory.read_buffer_subtitle()

            if text:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame)

                font = ImageFont.truetype("C:\Windows\Fonts\\arial.ttf", 25)
                draw = ImageDraw.Draw(pil_image)
                draw.text((225, 100), text, font=font, anchor='ms')

                frame = np.asarray(pil_image)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
            cv2.imshow('Zoom', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stream.release()
                cv2.destroyAllWindows()
                break

    def stop_stream(self):
        self.stop = True
        self.stream.release()
        cv2.destroyAllWindows()
