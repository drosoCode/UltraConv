from tkinter import scrolledtext, filedialog, WORD
from tkinter import ttk
import subprocess
        
from ultraconv.processors.utils import get_yass_path
from ultraconv.ui.data import UserData
from ultraconv.models import UltrastarFile

PAD_X = 10
PAD_Y = 5

class FileTab:

    def __init__(self, notebook, w, h):
        self._notebook = notebook
        self.frame = ttk.Frame(notebook, width=w, height=h, padding=20)

        self.open_button = ttk.Button(self.frame, text="Open txt")
        self.open_txt_label = ttk.Label(self.frame, text="path/to/file.txt")
        UserData.ui_text_preview = scrolledtext.ScrolledText(self.frame, wrap=WORD, width=110, height=20)
        self.save_button = ttk.Button(self.frame, text="Save")
        self.reload_button = ttk.Button(self.frame, text="Reload from disk")
        self.open_yass_button = ttk.Button(self.frame, text="Open in YASS")

        self.open_button.grid(row=0, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.open_txt_label.grid(row=0, column=1, columnspan=7, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        UserData.ui_text_preview.grid(row=1, column=0, sticky="nsew", rowspan=5, columnspan=8, padx=PAD_X, pady=PAD_Y)

        self.save_button.grid(row=6, column=0, sticky="nsew", columnspan=2, padx=PAD_X, pady=PAD_Y)
        self.reload_button.grid(row=6, column=2, sticky="nsew", columnspan=2, padx=PAD_X, pady=PAD_Y)
        self.open_yass_button.grid(row=6, column=4, sticky="nsew", columnspan=2, padx=PAD_X, pady=PAD_Y)

        self.open_button.bind("<Button-1>", lambda e: self._open_file())
        self.save_button.bind("<Button-1>", lambda e: self._save_file())
        self.reload_button.bind("<Button-1>", lambda e: self._reload_file())
        self.open_yass_button.bind("<Button-1>", lambda e: self._open_yass())

    def get_frame(self):
        return self.frame

    def _open_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        f = filedialog.askopenfilename(title="Select the .txt file to use for Ultrastar", filetypes=filetypes)
        self.open_txt_label.config(text=f)
        if f != "":
            UserData.ultrastar_file = UltrastarFile()
            UserData.ultrastar_file.read(f)
            UserData.set_message("File loaded successfully !")
            UserData.set_progress_bar(1)
            UserData.display_file()
            self._notebook.tab(1, state="normal")
            self._notebook.tab(2, state="normal")
        else:
            UserData.set_message("File open aborted")

    def _save_file(self):
        UserData.ultrastar_file.write()
        UserData.set_message("File saved successfully !")
        UserData.set_progress_bar(1)

    def _reload_file(self):
        f = UserData.ultrastar_file.file_path
        if f != "":
            UserData.ultrastar_file = UltrastarFile()
            UserData.ultrastar_file.read(f)
            UserData.set_message("File reloaded successfully !")
            UserData.set_progress_bar(1)
            UserData.display_file()
        else:
            UserData.set_message("No file to reload")

    def _open_yass(self):
        yass_path = get_yass_path()
        f = UserData.ultrastar_file.file_path
        if f != "":
            subprocess.Popen([yass_path, f])
            UserData.set_message("YASS opened !")
        else:
            UserData.set_message("No file to open in YASS")
