import tkinter as tk
from S2TT import S2TT
from T2S import T2S
from inputAudio import InputAudio
from WebCam import WebCame
from outputAudio import OutputAudio
from async_memory import AsyncMemory
# from summary import TextSummarizer
from virtualCamera import VirtualCamera
from tkinter import ttk


class LanguageGUI:
    def __init__(self):
        self.result = None
        self.setup_gui()
        self.root.mainloop()
    

    def setup_gui(self):
        # Create main window
        self.system_start = False
        self.root = tk.Tk()
        self.root.title("Simple Dropdown GUI")
        self.root.geometry("450x300")

        # Options for dropdowns
        options1 = ['English',
            'Deutsch',
            'Norsk',
            'Français',
            'Italiano',
            'Svenska',
            'עברית',
            '吴语',
            'Malayu',
            'Indo ',
            'Spanish']
        
        self.lang_dict = {
            'English': ['english', 'eng'],
            'Deutsch': ['german', 'deu'],
            'Norsk': ['norwegian', None],
            'Français': ['french', 'fra'],
            'Italiano': ['italian', None],
            'Svenska': ['swedish', 'swe'],
            'עברית': ['hebrew', 'heb'],
            '普通话': ['chinese', None],
            'Malayu': ['malay', 'pse'],
            'Indo': ['indonisian', 'ind'],
            'Spanish': ['spanish', 'spa']
        }

        # Create dropdown 1
        tk.Label(self.root, text="What is your Language:").pack(pady=5)
        self.dropdown1 = ttk.Combobox(self.root, values=options1, state="readonly")
        self.dropdown1.set(options1[0])  # Set default selection
        self.dropdown1.pack(pady=5)

        # Create dropdown 2
        tk.Label(self.root, text="What is the Other Person's Language:").pack(pady=5)
        self.dropdown2 = ttk.Combobox(self.root, values=options1, state="readonly")
        self.dropdown2.set(options1[0])  # Set default selection
        self.dropdown2.pack(pady=5)

        self.translated_audio_var = tk.BooleanVar()
        self.translated_audio_checkbox = tk.Checkbutton(self.root, text="Enable Translated Audio", 
                                 variable=self.translated_audio_var)
        self.translated_audio_checkbox.pack(pady=5)


        self.test_mode_var = tk.BooleanVar()
        self.test_mode_checkbox = tk.Checkbutton(self.root, text="Enable test mode", 
                                 variable=self.test_mode_var)
        self.test_mode_checkbox.pack(pady=5)

        # Create confirm button
        self.confirm_btn = tk.Button(self.root, text="Confirm", command=self.on_confirm)
        self.confirm_btn.pack(pady=10)

        self.shutdown_btn = tk.Button(self.root, text='Shutdown', command=self.on_shutdown_system)
        self.shutdown_btn.pack(pady=10)

    
    def get_selections(self):
        """Show GUI and return the selected values when confirmed"""
        self.root.mainloop()
        return self.result
    

    def setup_system(self, input_lang, trans_lang, output_lang, test_mode=False, use_trans_audio=True):
        self.memory = AsyncMemory(30)
        self.audio_in = InputAudio(memory=self.memory)
        device_idx = 3 if test_mode else 6
        self.audio_out = OutputAudio(self.audio_in, memory=self.memory, translated_audio=use_trans_audio, device_idx=device_idx)
        self.video_stream = WebCame(src=0, memory=self.memory) if test_mode else VirtualCamera(memory=self.memory)
        # summariser = TextSummarizer()
        self.s2tt = S2TT(memory=self.memory, in_lang=input_lang, out_lang=trans_lang)
        self.t2s = T2S(memory=self.memory, lang=output_lang) 

        if output_lang is not None:
            self.t2s.start()

        self.video_stream.start()
        self.audio_in.start()
        self.audio_out.start()
        self.s2tt.start()

        self.system_start = True


    def on_shutdown_system(self):
        if self.system_start:
            self.audio_in.stop_stream()
            self.audio_out.stop_stream()
            self.s2tt.stop_s2tt()
            self.t2s.stop_t2s()
            self.video_stream.stop_stream()

        self.root.destroy()

    
    def reset_system(self, input_lang, trans_lang, output_lang, test_mode=False, use_trans_audio=True):
        self.audio_in.stop_stream()
        self.audio_out.stop_stream()
        self.s2tt.stop_s2tt()
        self.t2s.stop_t2s()
        self.video_stream.stop_stream()

        self.memory = AsyncMemory(30)
        self.audio_in = InputAudio(memory=self.memory)
        device_idx = 3 if test_mode else 6
        self.audio_out = OutputAudio(self.audio_in, memory=self.memory, translated_audio=use_trans_audio, device_idx=device_idx)
        self.video_stream = WebCame(src=0, memory=self.memory) if test_mode else VirtualCamera(memory=self.memory)
        # summariser = TextSummarizer()
        self.s2tt.reset(memory=self.memory, in_lang=input_lang, out_lang=trans_lang)
        self.t2s = T2S(memory=self.memory, lang=output_lang) 

        if output_lang is not None:
            self.t2s.start()

        self.video_stream.start()
        self.audio_in.start()
        self.audio_out.start()
        self.s2tt.start()


    def on_confirm(self):
        selection1 = self.dropdown1.get()
        selection2 = self.dropdown2.get()

        lang_in = self.lang_dict[selection1][0]
        lang_trans, lang_out = self.lang_dict[selection2]

        test_mode = self.test_mode_var.get()

        use_trans_audio = self.translated_audio_var.get() and lang_out is not None

        if self.system_start:
            self.reset_system(input_lang=lang_in,
                              trans_lang=lang_trans, 
                              output_lang=lang_out,
                              test_mode=test_mode,
                              use_trans_audio=use_trans_audio)
        else:
            self.setup_system(input_lang=lang_in,
                              trans_lang=lang_trans, 
                              output_lang=lang_out,
                              test_mode=test_mode,
                              use_trans_audio=use_trans_audio)