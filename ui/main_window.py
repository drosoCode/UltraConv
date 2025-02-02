import tkinter
from tkinter import ttk

import sv_ttk

from download_tab import get_download_frame
from tools_tab import get_tools_frame
from file_tab import get_file_tab

WIDTH = 1000
HEIGHT = 500

root = tkinter.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title('UltraConv')
style = ttk.Style(root)

#button = ttk.Button(root, text="Click me!")
#button.pack()
#scrollbar = ttk.Scrollbar(root)
#listbox = ttk.Treeview(root, yscrollcommand=scrollbar.set, show="tree")
#scrollbar.configure(command=listbox.yview)
#
#scrollbar.pack(side="right", fill="y")
#listbox.pack(side="left", fill="both", expand=True)
#
#for i in range(100):
#    text = f"Item #{i+1}"
#    listbox.insert("", "end", text=text)
#

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# create frames
file_frame = get_file_tab(notebook, WIDTH, HEIGHT)
file_frame.pack(fill='both', expand=True)

download_frame = get_download_frame(notebook, WIDTH, HEIGHT)
download_frame.pack(fill='both', expand=True)

tools_frame = get_tools_frame(notebook, WIDTH, HEIGHT)
tools_frame.pack(fill='both', expand=True)

# add frames to notebook
notebook.add(file_frame, text='File')
notebook.add(download_frame, text='Download')
notebook.add(tools_frame, text='Tools')

sv_ttk.set_theme("dark")

root.mainloop()

"""
Menu deroulant (ex: choix modele/langage translit): https://www.pythontutorial.net/tkinter/tkinter-combobox/
Liste des resultats de recherche: https://www.pythontutorial.net/tkinter/tkinter-listbox/
Visu fichier ultrastar: https://www.pythontutorial.net/tkinter/tkinter-scrolledtext/
Selection nombre: https://www.pythontutorial.net/tkinter/tkinter-spinbox/
Bouton: https://www.pythontutorial.net/tkinter/tkinter-button/
Tabs: https://www.pythontutorial.net/tkinter/tkinter-notebook/
Progressbar: https://www.pythontutorial.net/tkinter/tkinter-progressbar/
File picker: https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
Input box: https://www.pythontutorial.net/tkinter/tkinter-entry/
Checkbox: https://www.pythontutorial.net/tkinter/tkinter-checkbox/
"""
