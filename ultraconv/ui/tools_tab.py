from tkinter import ttk, filedialog

from ultraconv.processors import TransliteratorProcessor, SplitterProcessor, PitcherProcessor
from ultraconv.converters import LrcConverter, AssConverter
from ultraconv.models import UltrastarFile
from .data import UserData

PAD_X = 10
PAD_Y = 5

class ToolsTab:    
    def __init__(self, notebook, w, h):
        self.frame = ttk.Frame(notebook, width=w, height=h, padding=20)

        self.import_lrc_button = ttk.Button(self.frame, text="Import LRC")
        self.import_lrc_ignore_wbw_checkbox = ttk.Checkbutton(self.frame, text="Ignore Word Sync")
        self.import_lrc_ignore_wbw_checkbox.invoke()
        self.import_lrc_bpm_number_label = ttk.Label(self.frame, text="BPM")
        self.import_lrc_bpm_number = ttk.Spinbox(self.frame, from_=0, to=1000)
        self.import_lrc_bpm_number.set(400)
        self.import_lrc_line_pct_label = ttk.Label(self.frame, text="Line percentage")
        self.import_lrc_line_pct = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01)
        self.import_lrc_line_pct.set(0.95)
        self.import_lrc_word_pct_label = ttk.Label(self.frame, text="Word percentage")
        self.import_lrc_word_pct = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01)
        self.import_lrc_word_pct.set(0.8)
        
        self.import_ass_button = ttk.Button(self.frame, text="Import ASS")
        self.import_ass_bpm_number_label = ttk.Label(self.frame, text="BPM")
        self.import_ass_bpm_number = ttk.Spinbox(self.frame, from_=0, to=1000)
        self.import_ass_bpm_number.set(400)

        self.transliterate_button = ttk.Button(self.frame, text="Transliterate")
        self.transliterate_dropdown_label = ttk.Label(self.frame, text="From-To Writing")
        langs = TransliteratorProcessor.get_languages()
        self.transliterate_dropdown = ttk.Combobox(self.frame, values=langs)
        if "Any-Latin" in langs:
            self.transliterate_dropdown.set("Any-Latin")
        
        self.split_voice_button = ttk.Button(self.frame, text="Split voice")
        self.split_voice_dropdown_label = ttk.Label(self.frame, text="Model")
        models = SplitterProcessor.get_models()
        self.split_voice_dropdown = ttk.Combobox(self.frame, values=models)
        if "htdemucs" in models:
            self.split_voice_dropdown.set("htdemucs")
        self.split_voice_jobs_number_label = ttk.Label(self.frame, text="Jobs")
        self.split_voice_jobs_number = ttk.Spinbox(self.frame, from_=0, to=8)
        self.split_voice_jobs_number.set(4)
        self.split_voice_shifts_number_label = ttk.Label(self.frame, text="Shifts")
        self.split_voice_shifts_number = ttk.Spinbox(self.frame, from_=0, to=8)
        self.split_voice_shifts_number.set(1)

        self.pitch_button = ttk.Button(self.frame, text="Pitch")
        self.pitch_post_process_checkbox = ttk.Checkbutton(self.frame, text="Post-Process")
        self.pitch_post_process_checkbox.invoke()
        

        self.import_lrc_button.grid(row=0, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.import_lrc_ignore_wbw_checkbox.grid(row=0, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.import_lrc_bpm_number_label.grid(row=0, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
        self.import_lrc_bpm_number.grid(row=0, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.import_lrc_line_pct_label.grid(row=1, column=0, sticky="", padx=PAD_X, pady=PAD_Y)
        self.import_lrc_line_pct.grid(row=1, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.import_lrc_word_pct_label.grid(row=1, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
        self.import_lrc_word_pct.grid(row=1, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        ttk.Separator(self.frame, orient='horizontal').grid(row=2, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

        self.import_ass_button.grid(row=3, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.import_ass_bpm_number_label.grid(row=3, column=1, sticky="", padx=PAD_X, pady=PAD_Y)
        self.import_ass_bpm_number.grid(row=3, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        
        ttk.Separator(self.frame, orient='horizontal').grid(row=4, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

        self.transliterate_button.grid(row=5, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.transliterate_dropdown_label.grid(row=5, column=1, sticky="", padx=PAD_X, pady=PAD_Y)
        self.transliterate_dropdown.grid(row=5, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        ttk.Separator(self.frame, orient='horizontal').grid(row=6, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

        self.split_voice_button.grid(row=7, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.split_voice_dropdown_label.grid(row=7, column=1, sticky="", padx=PAD_X, pady=PAD_Y)
        self.split_voice_dropdown.grid(row=7, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.split_voice_jobs_number_label.grid(row=8, column=0, sticky="", padx=PAD_X, pady=PAD_Y)
        self.split_voice_jobs_number.grid(row=8, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.split_voice_shifts_number_label.grid(row=8, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
        self.split_voice_shifts_number.grid(row=8, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        ttk.Separator(self.frame, orient='horizontal').grid(row=9, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

        self.pitch_button.grid(row=10, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.pitch_post_process_checkbox.grid(row=10, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        # bind event handlers
        self.import_lrc_button.bind("<Button-1>", lambda e: self._import_lrc())
        self.import_ass_button.bind("<Button-1>", lambda e: self._import_ass())
        self.split_voice_button.bind("<Button-1>", lambda e: self._split_voice())
        self.transliterate_button.bind("<Button-1>", lambda e: self._transliterate())
        self.pitch_button.bind("<Button-1>", lambda e: self._pitch())

    def get_frame(self):
        return self.frame
    
    def _import_lrc(self):
        filetypes = (
            ('lyrics file', '*.lrc;*.txt'),
            ('All files', '*.*')
        )
        f = filedialog.askopenfilename(title="Select the lrc file to import", filetypes=filetypes)
        if f == "":
            UserData.set_message("Error: No file selected")
            return
        
        cvt = LrcConverter(
            bpm=int(self.import_lrc_bpm_number.get()),
            ignore_words=("selected" in self.import_lrc_ignore_wbw_checkbox.state()),
            line_length_pct=float(self.import_lrc_line_pct.get()),
            word_length_pct=float(self.import_lrc_word_pct.get())
        )
        with open(f, "r", encoding="utf8") as fi:
            data = fi.readlines()
        UserData.ultrastar_file = cvt.convert(lyrics=data, ultrastar_file=UserData.ultrastar_file)
        UserData.display_file()

        UserData.set_message("Lyrics imported successfully !")
        UserData.set_progress_bar(1)

    def _import_ass(self):
        filetypes = (
            ('lyrics file', '*.ass;*.txt'),
            ('All files', '*.*')
        )
        f = filedialog.askopenfilename(title="Select the lrc file to import", filetypes=filetypes)
        if f == "":
            UserData.set_message("Error: No file selected")
            return

        cvt = AssConverter(bpm=int(self.import_ass_bpm_number.get()))
        with open(f, "r", encoding="utf8") as fi:
            data = fi.readlines()
        UserData.ultrastar_file = cvt.convert(lyrics=data, ultrastar_file=UserData.ultrastar_file)
        UserData.display_file()

        UserData.set_message("Lyrics imported successfully !")
        UserData.set_progress_bar(1)

    def _split_voice(self):
        proc = SplitterProcessor(model=self.split_voice_dropdown.get(), jobs=int(self.split_voice_jobs_number.get()), shifts=int(self.split_voice_shifts_number.get()))
        UserData.set_message("Splitting voice ...")
        UserData.set_progress_bar(-1)

        def cb(file):
            UserData.ultrastar_file = file
            UserData.display_file()
            UserData.set_message("Voice splitting done !")
            UserData.set_progress_bar(1)

        UserData.start_task(cb, proc.run, UserData.ultrastar_file)

    def _transliterate(self):
        proc = TransliteratorProcessor(language=self.transliterate_dropdown.get())
        UserData.ultrastar_file = proc.run(UserData.ultrastar_file)
        UserData.display_file()
        UserData.set_message("Transliteration done !")
        UserData.set_progress_bar(1)

    def _pitch(self):
        proc = PitcherProcessor(postproc=("selected" in self.pitch_post_process_checkbox.state()))
        UserData.set_message("Pitching ...")
        UserData.set_progress_bar(-1)

        def cb(file):
            UserData.ultrastar_file = file
            UserData.display_file()
            UserData.set_message("Pitching done !")
            UserData.set_progress_bar(1)

        UserData.start_task(cb, proc.run, UserData.ultrastar_file)
