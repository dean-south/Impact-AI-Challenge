import cv2
import pyvirtualcam
import threading
import numpy as np
from PIL import ImageDraw, Image, ImageFont


class VirtualCamera:
    def __init__(self, memory, source=0, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps

        self.camera = pyvirtualcam.Camera(
            width=self.width, 
            height=self.height, 
            fps=self.fps
        )

        self.stream = cv2.VideoCapture(source)

        self.memory = memory

        self.stop = False

        print(f"Virtual camera started: {self.width}x{self.height} @ {self.fps}fps")
        print(f"Camera device: {self.camera.device}")
        
    
    def stop_stream(self):
        """Stop the virtual camera"""
        if self.camera:
            self.camera.close()
            print("Virtual camera stopped")

        self.stream.release()

    
    def start(self):
        self.stop = False
        print("Starting Virtual Camera...")
        threading.Thread(target=self.stream_from_webcam, args=()).start()

    
    def stream_from_webcam(self):
        """Stream from a real webcam through the virtual camera"""
        if not self.camera:
            print("Camera not started. Call start() first.")
            return
        
        if not self.stream.isOpened():
            print(f"Failed to open webcam")
            return
        
        # Set webcam properties
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.stream.set(cv2.CAP_PROP_FPS, self.fps)
                
        print(f"Streaming from webcam...")
        
        try:
            while not self.stop:
                ret, frame = self.stream.read()
                if not ret:
                    print("Failed to read from webcam")
                    break
                
                # Resize if necessary
                if frame.shape[:2] != (self.height, self.width):
                    frame = cv2.resize(frame, (self.width, self.height))
                
                text = self.memory.read_buffer_subtitle()

                if text:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame)

                    font = ImageFont.truetype("C:\Windows\Fonts\\arial.ttf", 25)
                    draw = ImageDraw.Draw(pil_image)
                    draw.text((self.width//2, self.height-100), text, anchor="ms", font_size=40, font=font)

                    frame = np.asarray(pil_image)
    

                # Send to virtual camera
                self.camera.send(frame)
                self.camera.sleep_until_next_frame()   

        except KeyboardInterrupt:
            print("\nStopping stream...")
        finally:
            self.stream.release()