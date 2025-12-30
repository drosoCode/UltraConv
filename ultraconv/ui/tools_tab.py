from tkinter import ttk, filedialog

import voluptuous as vol

from ultraconv.processors import get_available_processors
from ultraconv.converters import LrcConverter, AssConverter
from ultraconv.models import UltrastarFile
from .data import UserData

PAD_X = 10
PAD_Y = 5

class ToolsTab:    
    def __init__(self, notebook, w, h):
        self.frame = ttk.Frame(notebook, width=w, height=h, padding=20)

        self._processor_by_name = {}
        self.processor_name = ""

        for i in get_available_processors():
            if self.processor_name == "":
                self.processor_name = i.get_info().name
            self._processor_by_name[i.get_info().name] = i

        # Import Section

        self.import_lrc_button = ttk.Button(self.frame, text="Import LRC")
        self.import_ass_button = ttk.Button(self.frame, text="Import ASS")
        self.import_bpm_number_label = ttk.Label(self.frame, text="BPM")
        self.import_bpm_number = ttk.Spinbox(self.frame, from_=0, to=1000)
        self.import_bpm_number.set(400)
        
        self.import_lrc_button.grid(row=0, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.import_ass_button.grid(row=0, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.import_bpm_number_label.grid(row=0, column=2, sticky="", padx=PAD_X, pady=PAD_Y)
        self.import_bpm_number.grid(row=0, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        ttk.Separator(self.frame, orient='horizontal').grid(row=1, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

        # Tool Selection Section

        self.processor_dropdown_label = ttk.Label(self.frame, text="Processor")
        self.processor_dropdown = ttk.Combobox(self.frame, values=list(self._processor_by_name.keys()))
        self.processor_run_button = ttk.Button(self.frame, text="Run")
        self.processor_desc_label = ttk.Label(self.frame, text=self._processor_by_name[self.processor_name].get_info().description)

        self.processor_dropdown_label.grid(row=2, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.processor_dropdown.grid(row=2, column=1, columnspan=6, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.processor_dropdown.set(self.processor_name)
        self.processor_run_button.grid(row=2, column=7, sticky="nsew", padx=PAD_X, pady=PAD_Y)
        self.processor_desc_label.grid(row=3, column=0, columnspan=8, sticky="w", padx=PAD_X, pady=PAD_Y)
        
        ttk.Separator(self.frame, orient='horizontal').grid(row=4, columnspan=8, sticky="ew", padx=PAD_X, pady=PAD_Y)

        # Config Section

        self.config_start_row = 5
        self.config_widgets = {}

        # bind event handlers
        self.import_lrc_button.bind("<Button-1>", lambda e: self._import_lrc())
        self.import_ass_button.bind("<Button-1>", lambda e: self._import_ass())
        self.processor_run_button.bind("<Button-1>", lambda e: self._run_tool())
        self.processor_dropdown.bind("<<ComboboxSelected>>", self._on_processor_changed)
        
        # initialize config options
        self.update_config_options()

    def _on_processor_changed(self, event):
        """Handle processor dropdown selection change"""
        self.processor_name = self.processor_dropdown.get()
        self.processor_desc_label.config(text=self._processor_by_name[self.processor_name].get_info().description)
        self.update_config_options()

    def update_config_options(self):
        """Dynamically create TTK widgets based on voluptuous schema"""
        # clear old widgets
        for widget_list in self.config_widgets.values():
            if isinstance(widget_list, list):
                for widget in widget_list:
                    widget.destroy()
            else:
                widget_list.destroy()
        self.config_widgets = {}
        
        # create new widgets based on schema
        opts: vol.Schema = self._processor_by_name[self.processor_name].get_options()
        i = 0
        for k, v in opts.schema.items():
            # Create label
            label = ttk.Label(self.frame, text=str(k).replace('_', ' ').title())
            label.grid(row=self.config_start_row + i, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)
            
            # Create widget based on validator type
            default_value = None
            try:
                default_value = k.default()
            except Exception:
                pass
            widget = self._create_widget_for_validator(v, default_value)
            widget.grid(row=self.config_start_row + i, column=1, sticky="ew", padx=PAD_X, pady=PAD_Y)
            
            self.config_widgets[k] = [label, widget]
            i += 1
    
    def _create_widget_for_validator(self, validator, default_value):
        """Create appropriate TTK widget based on voluptuous validator"""
        # Handle different validator types
        if validator == bool:
            widget = ttk.Checkbutton(self.frame)
            if default_value is not None:
                if default_value:
                    widget.invoke()
            return widget
            
        elif isinstance(validator, vol.In):
            # Handle vol.In([list of choices])
            choices = list(validator.container)
            widget = ttk.Combobox(self.frame, values=choices, state="readonly")
            if default_value is not None and default_value in choices:
                widget.set(default_value)
            elif choices:
                widget.set(choices[0])
            return widget
            
        elif isinstance(validator, vol.Range):
            # Handle vol.Range(min, max)
            widget = ttk.Spinbox(self.frame, from_=validator.min, to=validator.max, width=10)
            if default_value is not None:
                widget.set(str(default_value))
            else:
                widget.set(str(validator.min))
            return widget
            
        else:
            # Default to Entry for strings and unknown types
            widget = ttk.Entry(self.frame)
            if default_value is not None:
                widget.insert(0, str(default_value))
            return widget
    
    def get_config_values(self):
        """Extract values from config widgets"""
        config = {}
        for key, widget_list in self.config_widgets.items():
            widget = widget_list[1]  # widget_list[0] is label, [1] is the input widget
            
            if isinstance(widget, ttk.Checkbutton):
                config[key] = 'selected' in widget.state()
            elif isinstance(widget, (ttk.Spinbox, ttk.Entry)):
                try:
                    value = widget.get()
                    # Try to convert to appropriate type
                    if value.replace('.', '').replace('-', '').isdigit():
                        config[key] = float(value) if '.' in value else int(value)
                    else:
                        config[key] = value
                except:
                    config[key] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                config[key] = widget.get()

        return config
        

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
        
        UserData.ultrastar_file = LrcConverter(bpm=int(self.import_bpm_number.get())).convert(f, UserData.ultrastar_file)
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

        UserData.ultrastar_file = AssConverter(bpm=int(self.import_bpm_number.get())).convert(f, UserData.ultrastar_file)
        UserData.display_file()
        UserData.set_message("Lyrics imported successfully !")
        UserData.set_progress_bar(1)

    def _run_tool(self):
        if not self.processor_name or self.processor_name not in self._processor_by_name:
            UserData.set_message("Error: No processor selected")
            return
            
        # Get processor class and config values
        processor_class = self._processor_by_name[self.processor_name]
        config_values = self.get_config_values()
        
        # Create processor instance with config
        try:
            proc = processor_class(config_values)
        except Exception as e:
            UserData.set_message(f"Error creating processor: {str(e)}")
            return
            
        UserData.set_message(f"Running {self.processor_name}...")
        UserData.set_progress_bar(-1)

        def cb(file):
            UserData.ultrastar_file = file
            UserData.display_file()
            UserData.set_message(f"{self.processor_name} completed!")
            UserData.set_progress_bar(1)

        UserData.start_task(cb, proc.run, UserData.ultrastar_file)
