from pathlib import Path
from ultraconv.models import UltrastarFile
from tkinter import ttk, scrolledtext
from concurrent.futures import ThreadPoolExecutor, Future


class UserData:

    ultrastar_file: UltrastarFile

    ui_progress_bar: ttk.Progressbar
    ui_status_text: ttk.Label
    ui_text_preview: scrolledtext.ScrolledText
    ui_root: ttk.Frame

    _executor: ThreadPoolExecutor
    _future: Future
    _callback: callable

    @staticmethod
    def set_message(message):
        UserData.ui_status_text.config(text=message)

    @staticmethod
    def set_progress_bar(value):
        if value == 0:
            UserData.ui_progress_bar.config(mode="determinate", maximum=1, value=0)
        elif value == 1:
            UserData.ui_progress_bar.config(mode="determinate", maximum=1, value=1)
        else:
            UserData.ui_progress_bar.config(mode="indeterminate")
            UserData.ui_progress_bar.start()

    @staticmethod
    def display_file():
        # clear the text preview
        UserData.ui_text_preview.delete(1.0, "end")
        # display the file
        UserData.ui_text_preview.insert("end", "\n".join(UserData.ultrastar_file.get_file_data()))

    @staticmethod
    def ultrastar_dir():
        return Path(UserData.ultrastar_file.file_path).parent

    @staticmethod
    def start_task(callback, fn, /, *args, **kwargs):
        if UserData._future is not None:
            return False
        UserData._callback = callback
        UserData._future = UserData._executor.submit(fn, *args, **kwargs)
        UserData.ui_root.after(500, UserData._check_task)
        return True

    @staticmethod
    def _check_task():
        if UserData._future.done():
            UserData._callback(UserData._future.result())
            UserData._future = None
        else:
            UserData.ui_root.after(1000, UserData._check_task)
