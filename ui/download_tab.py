from tkinter import ttk, IntVar

SOURCES = ["Kara.moe", "Musixmatch", "Youtube"]

PAD_X = 5
PAD_Y = 5

def get_download_frame(notebook, w, h) -> ttk.Frame:
    download_frame = ttk.Frame(notebook, width=w, height=h, padding=20)

    provider_label = ttk.Label(download_frame, text="Provider")
    provider_dropdown = ttk.Combobox(download_frame, values=SOURCES)
    provider_dropdown.set(SOURCES[0])
    search_item_number_label = ttk.Label(download_frame, text="Max search results")
    search_item_number = ttk.Spinbox(download_frame, from_=0, to=100)
    search_item_number.set(10)
    search_bar = ttk.Entry(download_frame)
    search_bar_label = ttk.Label(download_frame, text="Search")
    search_button = ttk.Button(download_frame, text="Search")
    search_results_scrollbar = ttk.Scrollbar(download_frame)
    search_results = ttk.Treeview(download_frame, yscrollcommand=search_results_scrollbar.set, show="tree")
    search_results_scrollbar.configure(command=search_results.yview)

    download_lyrics_button = ttk.Button(download_frame, text="Download lyrics")
    download_video_button = ttk.Button(download_frame, text="Download video")
    convert_audio_checkbox = ttk.Checkbutton(download_frame, text="Convert audio")
    convert_audio_checkbox.invoke()
    convert_video_checkbox = ttk.Checkbutton(download_frame, text="Convert video")
    convert_video_checkbox.invoke()
    ignore_wbw_checkbox = ttk.Checkbutton(download_frame, text="Ignore Word Sync")
    ignore_wbw_checkbox.invoke()
    save_file_checkbox = ttk.Checkbutton(download_frame, text="Save lyrics file")
    save_file_checkbox.invoke()
    save_file_checkbox.invoke()
    bpm_number_label = ttk.Label(download_frame, text="BPM")
    bpm_number = ttk.Spinbox(download_frame, from_=0, to=1000)
    bpm_number.set(400)

    provider_label.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y)
    provider_dropdown.grid(row=0, column=1, columnspan=2, padx=PAD_X, pady=PAD_Y, sticky="nsew")
    search_item_number_label.grid(row=0, column=3, padx=PAD_X, pady=PAD_Y, sticky="nsew")
    search_item_number.grid(row=0, column=4, padx=PAD_X, pady=PAD_Y, sticky="nsew")

    search_bar_label.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y)
    search_bar.grid(row=1, column=1, columnspan=6, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    search_button.grid(row=1, column=7, padx=PAD_X, pady=PAD_Y)

    search_results.grid(row=2, column=0, columnspan=8, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    search_results_scrollbar.grid(row=2, column=8, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    download_video_button.grid(row=3, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    convert_video_checkbox.grid(row=3, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    convert_audio_checkbox.grid(row=3, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    download_lyrics_button.grid(row=4, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    ignore_wbw_checkbox.grid(row=4, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    save_file_checkbox.grid(row=4, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    bpm_number_label.grid(row=4, column=3, padx=PAD_X, pady=PAD_Y)
    bpm_number.grid(row=4, column=4, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    return download_frame

