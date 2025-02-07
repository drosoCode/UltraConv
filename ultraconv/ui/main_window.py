import tkinter
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor

import sv_ttk

from .download_tab import DownloadTab
from .tools_tab import get_tools_frame
from .file_tab import FileTab
from .data import UserData

WIDTH = 960
HEIGHT = 530

def run():
    root = tkinter.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title('UltraConv')

    notebook = ttk.Notebook(root)

    # create frames
    file_frame = FileTab(notebook, WIDTH, HEIGHT).get_frame()
    file_frame.pack(fill='both', expand=True)

    download_frame = DownloadTab(notebook, WIDTH, HEIGHT).get_frame()
    download_frame.pack(fill='both', expand=True)

    tools_frame = get_tools_frame(notebook, WIDTH, HEIGHT)
    tools_frame.pack(fill='both', expand=True)

    # add frames to notebook
    notebook.add(file_frame, text='File')
    notebook.add(download_frame, text='Download')
    notebook.add(tools_frame, text='Tools')

    # add bottom widgets
    UserData.ui_progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", maximum=1, value=0)
    UserData.ui_status_text = ttk.Label(root, text="Please open a txt file")

    notebook.grid(row=0, column=0, columnspan=9, rowspan=10, sticky="nsew")
    UserData.ui_status_text.grid(row=10, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
    UserData.ui_progress_bar.grid(row=10, column=5, columnspan=5, sticky="nsew", padx=10, pady=10)

    sv_ttk.set_theme("dark")

    # init UserData
    UserData.ui_root = root
    UserData._executor = ThreadPoolExecutor(max_workers=1)
    UserData._future = None

    root.mainloop()

