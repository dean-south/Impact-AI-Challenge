import numpy as np
import torch
import whisper
import time
import gc
import threading
from typing import Optional
from langchain.chains import TransformChain
from translator import T2TT


class S2TT:
    def __init__(self, memory, in_lang: str = 'spanish', out_lang: str = 'english'):
        
        self.stop = False

        self.in_lang = in_lang
        self.out_lang = out_lang
        
        """Initialize transcriber with buffer duration in seconds"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        # Initialize Whisper model
        print("Loading Whisper model...")
        self.model = whisper.load_model(
            "large-v3-turbo", 
            device=self.device,
            download_root="./models"
        )

        self.memory = memory
        
        # Buffer setup
        self.last_transcription_time = time.time()
        self.prev_transcription = ""
        
        # Memory management
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.set_per_process_memory_fraction(0.8)
        
        # Whisper options
        self.options = whisper.DecodingOptions(
            fp16=torch.cuda.is_available(),
            language=self.in_lang,
            task='transcribe',
            without_timestamps=True,
            beam_size=5
        )
        
        # Initialize LangChain components
        self.setup_langchain()
        
        self.model.eval()

        self.T2TT = T2TT()

        print("Model and LangChain ready!")


    def setup_langchain(self):
        """Setup LangChain components for post-processing"""
        
        # Create text cleaning chain
        def clean_text(inputs: dict) -> dict:
            text = inputs['text']
            if not text:
                return {'cleaned_text': ''}
            
            # Basic text cleaning
            cleaned = text.strip()
            cleaned = ' '.join(cleaned.split())  # Remove extra whitespace
            cleaned = cleaned.capitalize()
            
            return {'cleaned_text': cleaned}
        
        self.clean_chain = TransformChain(
            input_variables=['text'],
            output_variables=['cleaned_text'],
            transform=clean_text
        )


    def _preprocess_audio(self, input_audio: np.ndarray) -> Optional[np.ndarray]:
        """Preprocess audio and check for silence"""
        if len(input_audio) == 0:
            return None
            
        # Convert to float32 if needed
        audio_array = np.array(input_audio, dtype=np.float32)
        
        # Enhanced silence detection
        window_size = 160  # 100ms windows
        windows = np.array_split(audio_array, max(1, len(audio_array) // window_size))
        window_energies = [np.sqrt(np.mean(np.square(w))) for w in windows]
        
        if np.mean(window_energies) < 0.015:
            return None
            
        # Normalize audio
        if np.max(np.abs(audio_array)) > 0:
            audio_array = audio_array / np.max(np.abs(audio_array))
            
        return audio_array


    @torch.no_grad()
    def transcribe_translate(self):
        while not self.stop:
            # Rate limiting
            current_time = time.time()
            time.sleep(1)
                
            audio_array = np.array(self.memory.get_input_audio(), dtype=np.float32)
            
            # Preprocess audio
            processed_audio = self._preprocess_audio(audio_array)
            if processed_audio is None:
                self.memory.write_buffer(" ")
                time.sleep(0.01)
                continue

            # Transcribe with Whisper
            with torch.amp.autocast('cuda',enabled=True):
                result = self.model.transcribe(
                    processed_audio,
                    **self.options.__dict__
                )
            
            transcription = result['text'].strip()
            
            # Process through LangChain
            if transcription:
                cleaned_result = self.clean_chain.run(text=transcription)
                transcription = cleaned_result
            
            # Periodic CUDA cleanup
            if torch.cuda.is_available() and current_time % 30 < 1:
                torch.cuda.empty_cache()
                gc.collect()
            
            self.memory.add_to_history(transcription, True)

            if self.in_lang == self.out_lang:
                translation = transcription
            elif transcription == '':
                translation = ''
            else:
                translation = self.T2TT.translate(transcription, self.in_lang, self.out_lang)
            
            self.memory.add_to_history(translation, False)
            self.memory.write_buffer(translation)


    def start(self):
        self.stop = False
        print("Starting transcription thread...")
        threading.Thread(target=self.transcribe_translate, args=(), daemon=True).start()

    
    def reset(self, memory, in_lang, out_lang):
        self.memory = memory
        self.in_lang = in_lang
        self.out_lang = out_lang


    def stop_s2tt(self):
        self.stop = True


    def __del__(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()