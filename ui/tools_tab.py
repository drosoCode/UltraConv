from tkinter import ttk

PAD_X = 10
PAD_Y = 5

def get_tools_frame(notebook, w, h) -> ttk.Frame:
    tools_frame = ttk.Frame(notebook, width=w, height=h, padding=20)

    import_lrc_button = ttk.Button(tools_frame, text="Import LRC")
    import_lrc_ignore_wbw_checkbox = ttk.Checkbutton(tools_frame, text="Ignore Word Sync")
    import_lrc_ignore_wbw_checkbox.invoke()
    import_lrc_bpm_number_label = ttk.Label(tools_frame, text="BPM")
    import_lrc_bpm_number = ttk.Spinbox(tools_frame, from_=0, to=1000)
    import_lrc_bpm_number.set(400)
    import_lrc_line_pct_label = ttk.Label(tools_frame, text="Line percentage")
    import_lrc_line_pct = ttk.Spinbox(tools_frame, from_=0, to=1, increment=0.05)
    import_lrc_line_pct.set(0.95)
    import_lrc_word_pct_label = ttk.Label(tools_frame, text="Word percentage")
    import_lrc_word_pct = ttk.Spinbox(tools_frame, from_=0, to=1, increment=0.05)
    import_lrc_word_pct.set(0.8)
    
    import_ass_button = ttk.Button(tools_frame, text="Import ASS")
    import_ass_bpm_number_label = ttk.Label(tools_frame, text="BPM")
    import_ass_bpm_number = ttk.Spinbox(tools_frame, from_=0, to=1000)
    import_ass_bpm_number.set(400)

    transliterate_button = ttk.Button(tools_frame, text="Transliterate")
    transliterate_dropdown_label = ttk.Label(tools_frame, text="From-To Writing")
    transliterate_dropdown = ttk.Combobox(tools_frame, values=["Any-Latin"])
    transliterate_dropdown.set("Any-Latin")
    
    split_voice_button = ttk.Button(tools_frame, text="Split voice")
    split_voice_dropdown_label = ttk.Label(tools_frame, text="Model")
    split_voice_dropdown = ttk.Combobox(tools_frame, values=["htdemucs"])
    split_voice_dropdown.set("htdemucs")
    split_voice_jobs_number_label = ttk.Label(tools_frame, text="Jobs")
    split_voice_jobs_number = ttk.Spinbox(tools_frame, from_=0, to=8)
    split_voice_jobs_number.set(4)
    split_voice_shifts_number_label = ttk.Label(tools_frame, text="Shifts")
    split_voice_shifts_number = ttk.Spinbox(tools_frame, from_=0, to=8)
    split_voice_shifts_number.set(1)

    pitch_button = ttk.Button(tools_frame, text="Pitch")
    pitch_post_process_checkbox = ttk.Checkbutton(tools_frame, text="Post-Process")
    pitch_post_process_checkbox.invoke()
    

    import_lrc_button.grid(row=0, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    import_lrc_ignore_wbw_checkbox.grid(row=0, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    import_lrc_bpm_number_label.grid(row=0, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
    import_lrc_bpm_number.grid(row=0, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    import_lrc_line_pct_label.grid(row=1, column=0, sticky="", padx=PAD_X, pady=PAD_Y)
    import_lrc_line_pct.grid(row=1, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    import_lrc_word_pct_label.grid(row=1, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
    import_lrc_word_pct.grid(row=1, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    ttk.Separator(tools_frame, orient='horizontal').grid(row=2, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

    import_ass_button.grid(row=3, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    import_ass_bpm_number_label.grid(row=3, column=1, sticky="", padx=PAD_X, pady=PAD_Y)
    import_ass_bpm_number.grid(row=3, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    
    ttk.Separator(tools_frame, orient='horizontal').grid(row=4, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

    transliterate_button.grid(row=5, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    transliterate_dropdown_label.grid(row=5, column=1, sticky="", padx=PAD_X, pady=PAD_Y)
    transliterate_dropdown.grid(row=5, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    ttk.Separator(tools_frame, orient='horizontal').grid(row=6, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

    split_voice_button.grid(row=7, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    split_voice_dropdown_label.grid(row=7, column=1, sticky="", padx=PAD_X, pady=PAD_Y)
    split_voice_dropdown.grid(row=7, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    split_voice_jobs_number_label.grid(row=8, column=0, sticky="", padx=PAD_X, pady=PAD_Y)
    split_voice_jobs_number.grid(row=8, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    split_voice_shifts_number_label.grid(row=8, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
    split_voice_shifts_number.grid(row=8, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    ttk.Separator(tools_frame, orient='horizontal').grid(row=9, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

    pitch_button.grid(row=10, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    pitch_post_process_checkbox.grid(row=10, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    return tools_frame

