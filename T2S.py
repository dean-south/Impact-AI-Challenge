import torch
import time
import gc
import threading
from transformers import VitsModel, AutoTokenizer

class T2S:
    def __init__(self, memory, lang='eng'):

        model_name = 'facebook/mms-tts-' + lang
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        print(f"Loading TTS model {model_name}...")
        
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = VitsModel.from_pretrained(model_name).to(self.device)
        self.memory = memory
        
        self.model.eval()

        self.stop = False


    @torch.no_grad()
    def synthesize_speech(self):
        while not self.stop:
            """Synthesize speech from text using the TTS model with Langchain integration."""
            try:
                text = self.memory.read_buffer_t2s()

                if text and not (text == '' or text == ' '):
                    # Generate speech
                    inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
                    output = self.model(**inputs)

                    self.memory.add_output_audio(output.waveform.cpu().numpy()[0])
                else:
                    time.sleep(0.01)
                
            except Exception as e:
                print(f"Error in speech synthesis: {str(e)}")
                pass

        
    def start(self):
        self.stop = False
        print("Starting speech synthesis thread...")
        threading.Thread(target=self.synthesize_speech, args=(), daemon=True).start()
    

    def stop_t2s(self):
        self.stop = True


    def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'model'):
            del self.model
        if hasattr(self, 'tokenizer'):
            del self.tokenizer
        torch.cuda.empty_cache()
        gc.collect()