import os
from tkinter import ttk
from ultraconv.models.source import SourceType
from ultraconv.models.ultrastar import UltrastarFile
from ultraconv.sources import get_available_sources
from .data import UserData
import json
import traceback

PAD_X = 5
PAD_Y = 5

class DownloadTab:
    def __init__(self, notebook, w, h, source_config_path):
        self._source_by_name = {}
        self.provider_name = ""
        self.provider_instance = None

        self._load_config_file(source_config_path)

        for i in get_available_sources():
            name = i.get_info().name
            opts = i.get_options()
            cfg = self.config_data.get(name, {})
            try:
                cfg = opts(cfg) # validate config
            except Exception as e:
                print(f"Error in config for source {name}: {e}")
                print(opts)
                continue

            if self.provider_name == "":
                self.provider_name = name
            self._source_by_name[name] = i
        
        self.download_frame = ttk.Frame(notebook, width=w, height=h, padding=20)

        self.provider_label = ttk.Label(self.download_frame, text="Provider")
        self.provider_dropdown = ttk.Combobox(self.download_frame, values=list(self._source_by_name.keys()))
        self.provider_dropdown.set(self.provider_name)
        self.search_item_number_label = ttk.Label(self.download_frame, text="Max search results")
        self.search_item_number = ttk.Spinbox(self.download_frame, from_=0, to=100)
        self.search_item_number.set(0)
        self.search_bar = ttk.Entry(self.download_frame)
        self.search_bar_label = ttk.Label(self.download_frame, text="Search")
        self.search_button = ttk.Button(self.download_frame, text="Search")
        self.search_results_scrollbar = ttk.Scrollbar(self.download_frame)
        self.search_results = ttk.Treeview(self.download_frame, yscrollcommand=self.search_results_scrollbar.set, show="tree")
        self.search_results_scrollbar.configure(command=self.search_results.yview)

        self.download_button = ttk.Button(self.download_frame, text="Download")
        
        self.sources_types = {
            SourceType.LYRICS: ttk.Checkbutton(self.download_frame, text="Lyrics"),
            SourceType.METADATA: ttk.Checkbutton(self.download_frame, text="Metadata"),
            SourceType.VIDEO: ttk.Checkbutton(self.download_frame, text="Video"),
            SourceType.AUDIO: ttk.Checkbutton(self.download_frame, text="Audio"),
            SourceType.VOICE_AUDIO: ttk.Checkbutton(self.download_frame, text="Voice"),
            SourceType.INSTRUMENTAL_AUDIO: ttk.Checkbutton(self.download_frame, text="Instrumental"),
        }
        for i in self.sources_types.values():
            i.invoke()

        # position widgets
        self.provider_label.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y)
        self.provider_dropdown.grid(row=0, column=1, columnspan=2, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.search_item_number_label.grid(row=0, column=3, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.search_item_number.grid(row=0, column=4, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.search_item_number.set(5)

        self.search_bar_label.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y)
        self.search_bar.grid(row=1, column=1, columnspan=6, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.search_button.grid(row=1, column=7, padx=PAD_X, pady=PAD_Y)

        self.search_results.grid(row=2, column=0, columnspan=8, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.search_results_scrollbar.grid(row=2, column=8, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.sources_types[SourceType.LYRICS].grid(row=3, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.sources_types[SourceType.METADATA].grid(row=3, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.sources_types[SourceType.VIDEO].grid(row=3, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.sources_types[SourceType.AUDIO].grid(row=4, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.sources_types[SourceType.VOICE_AUDIO].grid(row=4, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.sources_types[SourceType.INSTRUMENTAL_AUDIO].grid(row=4, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        self.download_button.grid(row=3, column=5, padx=PAD_X, pady=PAD_Y)

        # setup handlers
        self.provider_dropdown.bind("<<ComboboxSelected>>", lambda e: self._set_provider(self.provider_dropdown.get()))
        self.search_button.bind("<Button-1>", lambda e: self._search_click())
        self.download_button.bind("<Button-1>", lambda e: self._dl_click())

        # set initial state
        self._set_checkboxes()
        self._set_provider(self.provider_name)
        self.provider_results = {}

    def _load_config_file(self, path):
        if not os.path.exists(path):
            print("No config file found")
            self.config_data = {}
            return
        with open(path, "r", encoding="utf-8") as f:
            self.config_data = json.load(f)

    def get_frame(self):
        return self.download_frame

    def _set_checkboxes(self):
        for i in self.sources_types.values():
            i.config(state="disabled")
        for i in self._source_by_name[self.provider_name].get_info().supported_types:
            self.sources_types[i].config(state="normal")

    def _set_provider(self, provider):
        self.provider_name = provider
        try:
            self.provider_instance = self._source_by_name[provider](self.config_data.get(provider, {}))
        except Exception as e:
            UserData.set_message(f"Error setting provider: {e}")
            traceback.print_exc()
            self.provider_instance = None
        self._clear_results()
        self._set_checkboxes()

    def _clear_results(self):
        self.provider_results = {}
        for i in self.search_results.get_children():
            self.search_results.delete(i)

    def _search_click(self):
        if not self.provider_instance:
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
                if i.duration is not None and i.duration > 0:
                    m, s = divmod(i.duration, 60)
                    duration = f"{m}:{s} min"
                year = ""
                if i.year > 0:
                    year = f"({i.year})"
                self.search_results.insert("", "end", text=f"{i.track} - {i.artist} {year} {duration}", values=(i.id))
            
            UserData.set_message("Done !")
            UserData.set_progress_bar(1)
        
        # retrieve new results
        UserData.start_task(callback, self.provider_instance.search, self.search_bar.get(), int(self.search_item_number.get()))


    def _dl_click(self):
        # get selected search result
        item = self.search_results.focus()
        if item == "":
            UserData.set_message("Error: No item selected")
            return
        id = self.search_results.item(item)["values"]

        UserData.set_message("Downloading ...")
        UserData.set_progress_bar(-1)

        def _cb(uf: UltrastarFile):
            UserData.display_file()
            UserData.set_message("Download complete !")
            UserData.set_progress_bar(1)

        # download
        dl_types = []
        for k, v in self.sources_types.items():
            if v.instate(["selected"]):
                dl_types.append(k)
        UserData.start_task(_cb, self.provider_instance.download, self.provider_results[str(id[0])], dl_types, UserData.ultrastar_file)
