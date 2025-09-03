import threading
import numpy as np
from dataclasses import dataclass
from typing import Any, List, Optional
import time

@dataclass
class BufferState:
    content: Any
    webcam_reads: int = 0
    t2s_has_read: bool = False
    timestamp: float = 0.0

class AsyncMemory:
    def __init__(self, required_webcam_reads: int = 3):
        self.required_webcam_reads = required_webcam_reads
        self.buffer = None
        self.buffer_lock = threading.Lock()
        self.buffer_updated = threading.Condition(self.buffer_lock)  # Changed to Condition
        
        # History
        self.org_text_history = []
        self.trans_text_history = []
        self.history_lock = threading.Lock()
        
        # Audio buffers
        self.input_audio_buffer = []
        self.output_audio_buffer = []
        self.audio_lock = threading.Lock()

    def write_buffer(self, content: Any) -> None:
        """S2TT writes to buffer - only when previous buffer is fully consumed"""
        with self.buffer_updated:
            # Wait until previous buffer has been fully processed
            while (self.buffer is not None and 
                   (self.buffer.webcam_reads < self.required_webcam_reads or 
                    not self.buffer.t2s_has_read)):
                self.buffer_updated.wait()
            
            # Create new buffer
            self.buffer = BufferState(content=content, timestamp=time.time())
            # print(f"S2TT: New buffer written: '{content}'")
            self.buffer_updated.notify_all()  # Wake up all waiting readers

    def read_buffer_subtitle(self) -> Optional[Any]:
        """Webcam reads from buffer - can read multiple times"""
        with self.buffer_updated:
            # Wait for new content
            while self.buffer is None:
                self.buffer_updated.wait()
            
            if self.buffer.webcam_reads < self.required_webcam_reads:
                self.buffer.webcam_reads += 1
                content = self.buffer.content
                # print(f"Webcam: Read {self.buffer.webcam_reads}/{self.required_webcam_reads}: '{content}'")
                
                # Check if buffer is fully consumed
                self._check_buffer_consumed()
                return content
            else:
                # Already read enough times
                return self.buffer.content

    def read_buffer_t2s(self) -> Optional[Any]:
        """T2S reads from buffer - only once per buffer"""
        with self.buffer_updated:
            # Wait for new content
            while self.buffer is None:
                self.buffer_updated.wait()
            
            if not self.buffer.t2s_has_read:
                self.buffer.t2s_has_read = True
                content = self.buffer.content
                # print(f"T2S: Read buffer: '{content}'")
                
                # Check if buffer is fully consumed
                self._check_buffer_consumed()
                return content
            else:
                # Already read this buffer
                return None

    def _check_buffer_consumed(self):
        """Check if buffer has been fully consumed and notify writers"""
        if (self.buffer and 
            self.buffer.webcam_reads >= self.required_webcam_reads and 
            self.buffer.t2s_has_read):
            # print("Buffer fully consumed, notifying writers")
            self.buffer_updated.notify_all()  # Allow new writes

    def wait_for_new_buffer(self, last_timestamp: float = 0) -> Optional[Any]:
        """Wait for a buffer newer than the given timestamp"""
        with self.buffer_updated:
            while (self.buffer is None or 
                   self.buffer.timestamp <= last_timestamp):
                self.buffer_updated.wait()
            return self.buffer.content, self.buffer.timestamp

    # Audio buffer methods (unchanged)
    def add_input_audio(self, audio):
        with self.audio_lock:
            self.input_audio_buffer.extend(audio)

    def get_input_audio(self):
        with self.audio_lock:
            audio = self.input_audio_buffer.copy()
            self.input_audio_buffer.clear()
            return audio

    def add_output_audio(self, audio):
        with self.audio_lock:
            self.output_audio_buffer.extend(audio)

    def get_output_audio(self):
        with self.audio_lock:
            if self.output_audio_buffer:
                audio = self.output_audio_buffer.copy()
                self.output_audio_buffer.clear()
                return np.array(audio)
            return np.array([])

    # History methods (thread-safe)
    def add_to_history(self, text: str, is_original: bool = True):
        with self.history_lock:
            if is_original:
                self.org_text_history.append(text)
            else:
                self.trans_text_history.append(text)

    def get_history(self, is_original: bool = True) -> List[str]:
        with self.history_lock:
            return (self.org_text_history.copy() if is_original 
                   else self.trans_text_history.copy())