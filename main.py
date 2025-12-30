import os
from ultraconv.ui.main_window import run

config_path = os.path.join(os.getcwd(), "config_sources.json")

run(config_path)