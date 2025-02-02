from tkinter import scrolledtext, WORD
from tkinter import ttk

PAD_X = 10
PAD_Y = 5

def get_file_tab(notebook, w, h) -> ttk.Frame:
    file_frame = ttk.Frame(notebook, width=w, height=h, padding=20)

    open_button = ttk.Button(file_frame, text="Open txt")
    open_txt_label = ttk.Label(file_frame, text="path/to/file.txt")
    
    file_preview = scrolledtext.ScrolledText(file_frame, wrap=WORD, width=110, height=20)
    
    save_button = ttk.Button(file_frame, text="Save")
    

    open_button.grid(row=0, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
    open_txt_label.grid(row=0, column=1, columnspan=7, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    file_preview.grid(row=1, column=0, sticky="nsew", rowspan=5, columnspan=8, padx=PAD_X, pady=PAD_Y)

    save_button.grid(row=6, column=0, sticky="nsew", columnspan=8, padx=PAD_X, pady=PAD_Y)

    return file_frame

