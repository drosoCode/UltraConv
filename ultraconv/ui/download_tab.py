from tkinter import ttk
from ultraconv.sources import KaramoeSource, MusixMatchSource, YoutubeDLSource
from ultraconv.converters import AssConverter, LrcConverter
from ultraconv.processors import ffmpeg_convert
from .data import UserData

SOURCES = ["Kara.moe", "Musixmatch", "Youtube"]

PAD_X = 5
PAD_Y = 5

class DownloadTab:    
    def __init__(self, notebook, w, h):
        self.download_frame = ttk.Frame(notebook, width=w, height=h, padding=20)

        self.provider_label = ttk.Label(self.download_frame, text="Provider")
        self.provider_dropdown = ttk.Combobox(self.download_frame, values=SOURCES)
        self.provider_dropdown.set(SOURCES[0])
        self.search_item_number_label = ttk.Label(self.download_frame, text="Max search results")
        self.search_item_number = ttk.Spinbox(self.download_frame, from_=0, to=100)
        self.search_item_number.set(0)
        self.search_bar = ttk.Entry(self.download_frame)
        self.search_bar_label = ttk.Label(self.download_frame, text="Search")
        self.search_button = ttk.Button(self.download_frame, text="Search")
        self.search_results_scrollbar = ttk.Scrollbar(self.download_frame)
        self.search_results = ttk.Treeview(self.download_frame, yscrollcommand=self.search_results_scrollbar.set, show="tree")
        self.search_results_scrollbar.configure(command=self.search_results.yview)

        self.download_lyrics_button = ttk.Button(self.download_frame, text="Download lyrics")
        self.download_video_button = ttk.Button(self.download_frame, text="Download video")
        self.convert_audio_checkbox = ttk.Checkbutton(self.download_frame, text="Convert audio")
        self.convert_audio_checkbox.invoke()
        self.convert_video_checkbox = ttk.Checkbutton(self.download_frame, text="Convert video")
        self.convert_video_checkbox.invoke()
        self.ignore_wbw_checkbox = ttk.Checkbutton(self.download_frame, text="Ignore Word Sync")
        self.ignore_wbw_checkbox.invoke()
        self.save_file_checkbox = ttk.Checkbutton(self.download_frame, text="Save lyrics file")
        self.save_file_checkbox.invoke()
        self.save_file_checkbox.invoke()
        self.bpm_number_label = ttk.Label(self.download_frame, text="BPM")
        self.bpm_number = ttk.Spinbox(self.download_frame, from_=0, to=1000)
        self.bpm_number.set(400)


        # position widgets
        self.provider_label.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y)
        self.provider_dropdown.grid(row=0, column=1, columnspan=2, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.search_item_number_label.grid(row=0, column=3, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.search_item_number.grid(row=0, column=4, padx=PAD_X, pady=PAD_Y, sticky="nsew")

        self.search_bar_label.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y)
        self.search_bar.grid(row=1, column=1, columnspan=6, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.search_button.grid(row=1, column=7, padx=PAD_X, pady=PAD_Y)

        self.search_results.grid(row=2, column=0, columnspan=8, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.search_results_scrollbar.grid(row=2, column=8, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.download_video_button.grid(row=3, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.convert_video_checkbox.grid(row=3, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.convert_audio_checkbox.grid(row=3, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.download_lyrics_button.grid(row=4, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.ignore_wbw_checkbox.grid(row=4, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.save_file_checkbox.grid(row=4, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.bpm_number_label.grid(row=4, column=3, padx=PAD_X, pady=PAD_Y)
        self.bpm_number.grid(row=4, column=4, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        # setup handlers
        self.provider_dropdown.bind("<<ComboboxSelected>>", lambda e: self._set_provider(self.provider_dropdown.get()))
        self.search_button.bind("<Button-1>", lambda e: self._search_click())
        self.download_lyrics_button.bind("<Button-1>", lambda e: self._dl_lyrics_click())
        self.download_video_button.bind("<Button-1>", lambda e: self._dl_video_click())

        # set initial state
        self.provider = KaramoeSource()
        self.provider_results = {}

    def get_frame(self):
        return self.download_frame

    def _set_lyrics(self, enabled):
        state = "disabled"
        if enabled:
            state = "normal"
        self.bpm_number.config(state=state)
        self.ignore_wbw_checkbox.config(state=state)
        self.save_file_checkbox.config(state=state)
        self.download_lyrics_button.config(state=state)
        
    def _set_video(self, enabled):
        state = "disabled"
        if enabled:
            state = "normal"
        self.convert_audio_checkbox.config(state=state)
        self.convert_video_checkbox.config(state=state)
        self.download_video_button.config(state=state)

    def _set_provider(self, provider):
        if provider == "Kara.moe":
            self._set_lyrics(True)
            self._set_video(True)
            self.search_item_number.set(0)
            self.provider = KaramoeSource()
        elif provider == "Musixmatch":
            self._set_lyrics(True)
            self._set_video(False)
            self.search_item_number.set(10)
            self.provider = MusixMatchSource()
        elif provider == "Youtube":
            self._set_lyrics(False)
            self._set_video(True)
            self.search_item_number.set(5)
            self.provider = YoutubeDLSource()
        self._clear_results()

    def _clear_results(self):
        self.provider_results = {}
        for i in self.search_results.get_children():
            self.search_results.delete(i)

    def _search_click(self):
        if self.provider is None:
            print("Error: No provider selected")
            UserData.set_message("Error: No provider selected")
            return
        
        UserData.set_message("Searching ...")
        UserData.set_progress_bar(-1)

        # clear previous results
        self._clear_results()

        # callback to display new results
        def callback(data):
            for i in data:
                self.provider_results[i.id] = i
                duration = ""
                if i.duration > 0:
                    m, s = divmod(i.duration, 60)
                    duration = f"{m}:{s} min"
                year = ""
                if i.year > 0:
                    year = f"({i.year})"
                self.search_results.insert("", "end", text=f"{i.track} - {i.artist} {year} {duration}", values=(i.id))
            
            UserData.set_message("Done !")
            UserData.set_progress_bar(1)
        
        # retrieve new results
        UserData.start_task(callback, self.provider.search_songs, self.search_bar.get(), int(self.search_item_number.get()))


    def _dl_lyrics_click(self):
        # get selected search result
        item = self.search_results.focus()
        if item is None:
            print("Error: No item selected")
            return
        id = self.search_results.item(item)["values"]

        # download lyrics
        lyrics = self.provider.download_lyrics(self.provider_results[id])
        
        # save lyrics to file
        if self.save_file_checkbox.state()[0] == "selected":
            with open("lyrics.txt", "w+") as f:
                f.write(lyrics)

        # convert lyrics and add them to the ultrastar file
        if isinstance(self.provider, KaramoeSource):
            cvt = AssConverter(bpm=int(self.bpm_number.get()))
        else:
            cvt = LrcConverter(bpm=int(self.bpm_number.get()), ignore_words=self.ignore_wbw_checkbox.get())

        uf = cvt.convert(lyrics)


    def _dl_video_click(self):
        item = self.search_results.focus()
        if item is None:
            print("Error: No item selected")
            return
        id = self.search_results.item(item)["values"]

        path = self.provider.download_video(self.provider_results[id])
        
        if self.convert_audio_checkbox.state()[0] == "selected":
            ffmpeg_convert(path, "audio.mp3")
        if self.convert_video_checkbox.state()[0] == "selected":
            ffmpeg_convert(path, "video.mp4")
