from languageGUI import LanguageGUI



def main():
    lang_gui = LanguageGUI()

    # print(f'{test_mode=}')

    # memory = AsyncMemory(30)
    # audio_in = InputAudio(memory=memory)
    # device_idx = 3 if test_mode else 20
    # audio_out = OutputAudio(audio_in, memory=memory, output_lang=output_lang, device_idx=device_idx)
    # video_stream = WebCame(src=0, memory=memory) if test_mode else VirtualCamera(memory=memory)
    # # summariser = TextSummarizer()
    # s2tt = S2TT(memory=memory, in_lang=input_lang, out_lang=trans_lang)

    # if output_lang is not None:
    #     t2s = T2S(memory=memory, lang=output_lang) 
    #     t2s.start()

    # video_stream.start()
    # audio_in.start()
    # audio_out.start()
    # s2tt.start()

    # # Wait for video stream to close
    # try:
    #     while video_stream.stream.isOpened():
    #         time.sleep(0.1)
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     # Cleanup
    #     video_stream.stop()
    #     audio_in.stop_stream()
    #     audio_out.stop_stream()
        
        # summariser.summarize(memory.get_org_text_history())

if __name__ == "__main__":
    main()

