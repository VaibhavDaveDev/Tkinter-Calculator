import tkinter as tk
from tkinter import ttk
import math
import collections # Added for history
import json # For settings
import os   # For settings

class Calculator:
    SETTINGS_FILE = "calc_settings.json" 
    NUM_MEMORY_SLOTS = 5 

    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x610") 
        self.root.resizable(True, True) # Changed to True for main window responsiveness
        
        # Configure minimum size for the root window
        self.root.minsize(300, 500) # Example minimum size

        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.memory_slots = [0.0] * Calculator.NUM_MEMORY_SLOTS
        self.active_memory_slot_index = 0
        self.memory_slot_display_var = tk.StringVar()
        
        self.degree_mode = False 
        self.deg_rad_button = None 
        self.initial_deg_rad_text = "Rad" 

        self.history = collections.deque(maxlen=10)
        self.history_window = None
        self.history_listbox = None
        self.memory_slot_display_label = None 

        self.unit_conversion_window = None
        self.conversion_factors = {
            "Length": {
                "Meter (m)": 1.0, "Kilometer (km)": 1000.0, "Mile (mi)": 1609.34,
                "Foot (ft)": 0.3048, "Inch (in)": 0.0254, "Centimeter (cm)": 0.01,
                "Millimeter (mm)": 0.001,
            },
            "Weight": {
                "Kilogram (kg)": 1.0, "Gram (g)": 0.001,
                "Pound (lb)": 0.453592, "Ounce (oz)": 0.0283495,
            },
            "Temperature": { 
                "Celsius (°C)": "Celsius", "Fahrenheit (°F)": "Fahrenheit", "Kelvin (K)": "Kelvin",
            }
        }
        self.unit_categories = list(self.conversion_factors.keys())
        
        self.uc_category_var = tk.StringVar()
        self.uc_from_unit_var = tk.StringVar()
        self.uc_to_unit_var = tk.StringVar()
        self.uc_input_var = tk.StringVar()
        self.uc_result_var = tk.StringVar()
        
        self.uc_category_menu = None
        self.uc_from_unit_menu = None
        self.uc_to_unit_menu = None
        self.uc_input_entry = None
        self.uc_result_label = None

        self.themes = {
            "Light": {
                "bg": "#F0F0F0", "fg": "Black",
                "display_bg": "#FFFFFF", "display_fg": "Black", "mem_slot_fg": "Black", "uc_label_fg": "Black",
                "button_bg": "#E1E1E1", "button_fg": "Black", "button_active_bg": "#CFCFCF",
                "operator_button_bg": "#D3D3D3", "operator_button_fg": "Black", "operator_button_active_bg": "#BEBEBE",
                "memory_button_bg": "#CFCFCF", "memory_button_fg": "Black", "memory_button_active_bg": "#BDBDBD",
                "equals_button_bg": "#ADD8E6", "equals_button_fg": "Black", "equals_button_active_bg": "#9CCCE0",
                "special_button_bg": "#E1E1E1", "special_button_fg": "Black", "special_button_active_bg": "#CFCFCF",
                "listbox_bg": "#FFFFFF", "listbox_fg": "Black", "listbox_select_bg": "#0078D7", "listbox_select_fg": "White",
                "entry_bg": "#FFFFFF", "entry_fg": "Black",
            },
            "Dark": {
                "bg": "#2E2E2E", "fg": "White",
                "display_bg": "#1C1C1C", "display_fg": "White", "mem_slot_fg": "#A9A9A9", "uc_label_fg": "White",
                "button_bg": "#505050", "button_fg": "White", "button_active_bg": "#6A6A6A",
                "operator_button_bg": "#606060", "operator_button_fg": "White", "operator_button_active_bg": "#7A7A7A",
                "memory_button_bg": "#5A5A5A", "memory_button_fg": "White", "memory_button_active_bg": "#707070",
                "equals_button_bg": "#005A9C", "equals_button_fg": "White", "equals_button_active_bg": "#007ACC",
                "special_button_bg": "#505050", "special_button_fg": "White", "special_button_active_bg": "#6A6A6A",
                "listbox_bg": "#1C1C1C", "listbox_fg": "White", "listbox_select_bg": "#005A9C", "listbox_select_fg": "White",
                "entry_bg": "#3C3C3C", "entry_fg": "White",
            }
        }
        self.current_theme_name = "Light" 
        self.style = ttk.Style()
        
        self.all_button_widgets = [] 
        self.display_frame = None
        self.buttons_frame = None
        self.display_label = None

        self.load_settings() 
        self.memory_slot_display_var.set(f"M{self.active_memory_slot_index + 1}")

        self.create_widgets() 
        self.apply_theme()    

        self.root.bind('<Key>', self.handle_keypress)
        self.root.focus_set()

    def load_settings(self):
        try:
            if os.path.exists(Calculator.SETTINGS_FILE):
                with open(Calculator.SETTINGS_FILE, "r") as f:
                    loaded_settings = json.load(f)
                    self.current_theme_name = loaded_settings.get("theme", "Light")
                    loaded_history = loaded_settings.get("history", [])
                    if isinstance(loaded_history, list):
                        self.history.clear(); [self.history.append(item) for item in loaded_history]
                    
                    loaded_memory_slots = loaded_settings.get("memory_slots", [0.0] * Calculator.NUM_MEMORY_SLOTS)
                    if isinstance(loaded_memory_slots, list) and len(loaded_memory_slots) == Calculator.NUM_MEMORY_SLOTS:
                        self.memory_slots = loaded_memory_slots
                    else: self.memory_slots = [0.0] * Calculator.NUM_MEMORY_SLOTS
                    self.active_memory_slot_index = loaded_settings.get("active_memory_slot_index", 0)
                    if not (0 <= self.active_memory_slot_index < Calculator.NUM_MEMORY_SLOTS): self.active_memory_slot_index = 0
            else: pass
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}. Using default settings.")
            self.current_theme_name = "Light"; self.history.clear()
            self.memory_slots = [0.0] * Calculator.NUM_MEMORY_SLOTS; self.active_memory_slot_index = 0
    
    def save_settings(self):
        settings_to_save = {
            "theme": self.current_theme_name, "history": list(self.history),
            "memory_slots": self.memory_slots, "active_memory_slot_index": self.active_memory_slot_index
        }
        try:
            with open(Calculator.SETTINGS_FILE, "w") as f: json.dump(settings_to_save, f, indent=4)
        except IOError as e: print(f"Error saving settings: {e}")

    def create_widgets(self):
        # Configure root window's grid to make the display and button frames responsive
        self.root.grid_rowconfigure(0, weight=1) # Display frame row
        self.root.grid_rowconfigure(1, weight=4) # Button frame row (give more weight to buttons area)
        self.root.grid_columnconfigure(0, weight=1)

        self.display_frame = ttk.Frame(self.root, padding="10 5 10 0")
        self.display_frame.grid(row=0, column=0, sticky="nsew") # Use grid for display_frame
        
        # Configure display_frame's grid
        self.display_frame.grid_columnconfigure(0, weight=1) # Display label
        self.display_frame.grid_columnconfigure(1, weight=0) # Memory slot label (fixed width)
        self.display_frame.grid_rowconfigure(0, weight=1)

        self.display_label = ttk.Label(self.display_frame, textvariable=self.result_var, font=("Arial", 30), anchor="e")
        self.display_label.grid(row=0, column=0, sticky="nsew", pady=(0,5))
        
        self.memory_slot_display_label = ttk.Label(self.display_frame, textvariable=self.memory_slot_display_var, font=("Arial", 12), anchor="w")
        self.memory_slot_display_label.grid(row=0, column=1, sticky="ns", padx=(5,0), pady=(0,5))

        self.buttons_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.buttons_frame.grid(row=1, column=0, sticky="nsew") # Use grid for buttons_frame

        buttons = [
            ("History", 0, 0), ("Theme", 0, 1), ("MNext", 0, 2), 
            ("MS", 1, 0), ("MR", 1, 1), ("MC", 1, 2), ("M+", 1, 3),
            ("M-", 2, 0), ("MAC", 2, 1), ("Units", 2, 2), 
            (self.initial_deg_rad_text, 3, 0), ("π", 3, 1), ("e", 3, 2), ("Del", 3, 3),
            ("sin", 4, 0), ("cos", 4, 1), ("tan", 4, 2), ("^", 4, 3), 
            ("log", 5, 0), ("ln", 5, 1), ("exp", 5, 2), ("√", 5, 3),
            ("x²", 6, 0), ("x³", 6, 1), ("C", 6, 2), ("/", 6, 3),
            ("7", 7, 0), ("8", 7, 1), ("9", 7, 2), ("*", 7, 3),
            ("4", 8, 0), ("5", 8, 1), ("6", 8, 2), ("-", 8, 3),
            ("1", 9, 0), ("2", 9, 1), ("3", 9, 2), ("+", 9, 3),
            ("0", 10, 0, 2), (".", 10, 2), ("=", 10, 3)
        ]
        buttons.insert(3, (None, 0, 3)) # Placeholder for empty cell in row 0, col 3

        self.all_button_widgets.clear() 
        for button_spec in buttons:
            if button_spec[0] is None: continue 
            text, row, col = button_spec[0], button_spec[1], button_spec[2]
            colspan = button_spec[3] if len(button_spec) > 3 else 1
            command = lambda t=text: self.button_click(t)
            if text == "History": command = self.toggle_history_window
            elif text == "Theme": command = self.toggle_theme
            elif text == "Units": command = self.toggle_unit_conversion_window

            button = ttk.Button(self.buttons_frame, text=text, command=command)
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
            self.all_button_widgets.append(button)
            if text == self.initial_deg_rad_text: self.deg_rad_button = button
        
        for i in range(4): self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(11): self.buttons_frame.grid_rowconfigure(i, weight=1)
            
    def apply_theme(self):
        if not hasattr(self, 'style'): self.style = ttk.Style()
        theme_colors = self.themes.get(self.current_theme_name, self.themes["Light"]) 
        self.style.theme_use('default') 
        self.root.config(bg=theme_colors["bg"])

        self.style.configure("TFrame", background=theme_colors["bg"])
        if self.display_frame: self.display_frame.config(style="TFrame")
        if self.buttons_frame: self.buttons_frame.config(style="TFrame")

        self.style.configure("Display.TLabel", background=theme_colors["display_bg"], foreground=theme_colors["display_fg"], font=("Arial", 30), anchor="e", padding=(0,0,5,0))
        if self.display_label: self.display_label.config(style="Display.TLabel")
        self.style.configure("MemorySlot.TLabel", background=theme_colors["display_bg"], foreground=theme_colors["mem_slot_fg"], font=("Arial", 12), anchor="w", padding=(2,0,2,0))
        if self.memory_slot_display_label: self.memory_slot_display_label.config(style="MemorySlot.TLabel")
        
        if self.unit_conversion_window and self.unit_conversion_window.winfo_exists():
            self.unit_conversion_window.config(bg=theme_colors["bg"])
            self.style.configure("UC.TLabel", background=theme_colors["bg"], foreground=theme_colors["uc_label_fg"])
            self.style.configure("UC.TEntry", fieldbackground=theme_colors["entry_bg"], foreground=theme_colors["entry_fg"])
            if hasattr(self.unit_conversion_window, 'uc_frame_ref'): 
                for child in self.unit_conversion_window.uc_frame_ref.winfo_children(): 
                    if isinstance(child, ttk.Label): child.configure(style="UC.TLabel")
                    elif isinstance(child, ttk.Button): child.configure(style="Spec.TButton") 
                    elif isinstance(child, ttk.Entry): child.configure(style="UC.TEntry")
                    elif isinstance(child, ttk.OptionMenu): child.configure(style="TButton")

        self.style.configure("TButton", font=('Arial', 10), padding=(3,3,3,3), background=theme_colors["button_bg"], foreground=theme_colors["button_fg"])
        self.style.map("TButton", background=[('active', theme_colors["button_active_bg"]), ('pressed', theme_colors["button_active_bg"])])
        # ... (rest of button style configurations) ...
        self.style.configure("Num.TButton", background=theme_colors["button_bg"], foreground=theme_colors["button_fg"])
        self.style.map("Num.TButton", background=[('active', theme_colors["button_active_bg"])])
        self.style.configure("Op.TButton", background=theme_colors["operator_button_bg"], foreground=theme_colors["operator_button_fg"])
        self.style.map("Op.TButton", background=[('active', theme_colors["operator_button_active_bg"])])
        self.style.configure("Mem.TButton", background=theme_colors["memory_button_bg"], foreground=theme_colors["memory_button_fg"])
        self.style.map("Mem.TButton", background=[('active', theme_colors["memory_button_active_bg"])])
        self.style.configure("Eq.TButton", background=theme_colors["equals_button_bg"], foreground=theme_colors["equals_button_fg"])
        self.style.map("Eq.TButton", background=[('active', theme_colors["equals_button_active_bg"])])
        self.style.configure("Spec.TButton", background=theme_colors["special_button_bg"], foreground=theme_colors["special_button_fg"])
        self.style.map("Spec.TButton", background=[('active', theme_colors["special_button_active_bg"])])
        
        for btn_widget in self.all_button_widgets:
            text = btn_widget.cget("text")
            style_to_apply = "TButton" 
            if text.isdigit() or text == ".": style_to_apply = "Num.TButton"
            elif text in ["+", "-", "*", "/", "^"]: style_to_apply = "Op.TButton"
            elif text in ["MS", "MR", "MC", "M+", "M-", "MNext", "MAC"]: style_to_apply = "Mem.TButton"
            elif text == "=": style_to_apply = "Eq.TButton"
            elif text in ["C", "Del", "History", "Theme", "Units", "π", "e", "sin", "cos", "tan", "log", "ln", "exp", "√", "x²", "x³"] \
                 or (self.deg_rad_button and btn_widget == self.deg_rad_button): 
                style_to_apply = "Spec.TButton"
            btn_widget.config(style=style_to_apply)
            
        if self.history_window and self.history_listbox and self.history_listbox.winfo_exists():
            self.history_listbox.config(bg=theme_colors["listbox_bg"], fg=theme_colors["listbox_fg"], selectbackground=theme_colors["listbox_select_bg"], selectforeground=theme_colors["listbox_select_fg"])
            self.history_window.config(bg=theme_colors["bg"])

    def toggle_theme(self):
        self.current_theme_name = "Dark" if self.current_theme_name == "Light" else "Light"
        self.apply_theme(); self.save_settings() 

    def toggle_history_window(self):
        if self.history_window is None or not self.history_window.winfo_exists():
            self.history_window = tk.Toplevel(self.root) 
            self.history_window.title("Calculation History"); self.history_window.geometry("250x300"); self.history_window.transient(self.root)
            self.history_listbox = tk.Listbox(self.history_window); self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.update_history_display(); self.history_listbox.bind("<Double-1>", self.recall_history_item)
            self.history_window.protocol("WM_DELETE_WINDOW", self.on_close_history_window)
            self.apply_theme() 
        else: self.on_close_history_window()

    def on_close_history_window(self): 
        if self.history_window: self.history_window.destroy()
        self.history_window = None; self.history_listbox = None
        
    def update_history_display(self): 
        if self.history_window and self.history_listbox and self.history_listbox.winfo_exists():
            self.history_listbox.delete(0, tk.END)
            for item in self.history: self.history_listbox.insert(tk.END, item)

    def recall_history_item(self, event): 
        if not self.history_listbox: return
        selection_indices = self.history_listbox.curselection()
        if not selection_indices: return
        history_item_string = self.history_listbox.get(selection_indices[0])
        try:
            parts = history_item_string.split("=")
            recalled_value = parts[-1] if len(parts) > 1 else ""
            if recalled_value == "Error": self.expression = ""; self.result_var.set("Error")
            else: self.expression = recalled_value; self.result_var.set(self.expression)
        except Exception: self.expression = ""; self.result_var.set("Error")

    def toggle_unit_conversion_window(self):
        if self.unit_conversion_window is None or not self.unit_conversion_window.winfo_exists():
            self.unit_conversion_window = tk.Toplevel(self.root)
            self.unit_conversion_window.title("Unit Converter")
            self.unit_conversion_window.geometry("350x250")
            self.unit_conversion_window.minsize(300, 220) # Min size for UC window
            self.unit_conversion_window.transient(self.root) 

            uc_frame = ttk.Frame(self.unit_conversion_window, padding=10, style="TFrame")
            uc_frame.pack(fill=tk.BOTH, expand=True)
            self.unit_conversion_window.uc_frame_ref = uc_frame 

            # Configure grid columns for uc_frame
            uc_frame.grid_columnconfigure(0, weight=0)  # Label column
            uc_frame.grid_columnconfigure(1, weight=1)  # Widget column (OptionMenu, Entry)
            # Row configurations (optional, but good for consistent spacing or specific row expansion)
            for i in range(6): uc_frame.grid_rowconfigure(i, weight=0) # Default no expansion
            uc_frame.grid_rowconfigure(3, weight=0) # Input entry row - no specific expansion needed
            uc_frame.grid_rowconfigure(5, weight=1) # Result label row can expand if needed

            ttk.Label(uc_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.uc_category_var.set(self.unit_categories[0] if self.unit_categories else "")
            self.uc_category_menu = ttk.OptionMenu(uc_frame, self.uc_category_var, self.uc_category_var.get(), *self.unit_categories, command=self.update_unit_menus, style="TButton")
            self.uc_category_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(uc_frame, text="From:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.uc_from_unit_menu = ttk.OptionMenu(uc_frame, self.uc_from_unit_var, "", style="TButton")
            self.uc_from_unit_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

            ttk.Label(uc_frame, text="To:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.uc_to_unit_menu = ttk.OptionMenu(uc_frame, self.uc_to_unit_var, "", style="TButton")
            self.uc_to_unit_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            ttk.Label(uc_frame, text="Value:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.uc_input_entry = ttk.Entry(uc_frame, textvariable=self.uc_input_var)
            self.uc_input_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

            convert_button = ttk.Button(uc_frame, text="Convert", command=self.perform_unit_conversion, style="Spec.TButton")
            convert_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew") # columnspan=2 to fill

            ttk.Label(uc_frame, text="Result:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
            self.uc_result_label = ttk.Label(uc_frame, textvariable=self.uc_result_var, font=("Arial", 12))
            self.uc_result_label.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
            
            self.update_unit_menus() 
            self.unit_conversion_window.protocol("WM_DELETE_WINDOW", self.on_close_uc_window)
            self.apply_theme() 
        else:
            self.on_close_uc_window()

    def on_close_uc_window(self):
        if self.unit_conversion_window: self.unit_conversion_window.destroy()
        self.unit_conversion_window = None
        if self.unit_categories: self.uc_category_var.set(self.unit_categories[0])
        self.uc_input_var.set(""); self.uc_result_var.set("")

    def update_unit_menus(self, *args):
        category = self.uc_category_var.get()
        units = list(self.conversion_factors.get(category, {}).keys())
        # ... (rest of update_unit_menus logic remains the same) ...
        if self.uc_from_unit_menu:
            menu = self.uc_from_unit_menu["menu"]; menu.delete(0, "end")
            for unit in units: menu.add_command(label=unit, command=lambda u=unit, var=self.uc_from_unit_var: var.set(u))
            if units: self.uc_from_unit_var.set(units[0])
            else: self.uc_from_unit_var.set("")
        if self.uc_to_unit_menu:
            menu = self.uc_to_unit_menu["menu"]; menu.delete(0, "end")
            for unit in units: menu.add_command(label=unit, command=lambda u=unit, var=self.uc_to_unit_var: var.set(u))
            if units: self.uc_to_unit_var.set(units[0]) 
            else: self.uc_to_unit_var.set("")
        self.uc_input_var.set(""); self.uc_result_var.set("")


    def perform_unit_conversion(self):
        # ... (existing perform_unit_conversion logic remains the same) ...
        value_str = self.uc_input_var.get()
        from_unit = self.uc_from_unit_var.get()
        to_unit = self.uc_to_unit_var.get()
        category = self.uc_category_var.get()

        if not all([value_str, from_unit, to_unit, category]):
            self.uc_result_var.set("Missing input"); return
        try: value_float = float(value_str)
        except ValueError: self.uc_result_var.set("Invalid input value"); return

        if category == "Temperature":
            result = None
            if from_unit == to_unit: result = value_float
            elif from_unit == "Celsius (°C)":
                if to_unit == "Fahrenheit (°F)": result = (value_float * 9/5) + 32
                elif to_unit == "Kelvin (K)": result = value_float + 273.15
            elif from_unit == "Fahrenheit (°F)":
                if to_unit == "Celsius (°C)": result = (value_float - 32) * 5/9
                elif to_unit == "Kelvin (K)": result = ((value_float - 32) * 5/9) + 273.15
            elif from_unit == "Kelvin (K)":
                if to_unit == "Celsius (°C)": result = value_float - 273.15
                elif to_unit == "Fahrenheit (°F)": result = ((value_float - 273.15) * 9/5) + 32
            
            if result is not None: self.uc_result_var.set(f"{result:.2f}") 
            else: self.uc_result_var.set("Select units")
            return
        else: 
            try:
                category_factors = self.conversion_factors[category]
                from_factor = category_factors[from_unit]
                to_factor = category_factors[to_unit]
            except KeyError: self.uc_result_var.set("Unit factor error"); return
            if to_factor == 0: self.uc_result_var.set("Conversion error"); return
            value_in_base = value_float * from_factor
            result = value_in_base / to_factor
            self.uc_result_var.set(f"{result:.5g}")
            
    def handle_keypress(self, event):
        # ... (existing keypress logic) ...
        char = event.char; keysym = event.keysym
        if keysym == "Return": self.button_click("=")
        elif keysym == "BackSpace": self.button_click("Del")
        elif keysym == "Escape": self.button_click("C")
        elif char in "0123456789": self.button_click(char)
        elif char in "+-*/.": self.button_click(char)
        elif char == "^": self.button_click("^")

    def button_click(self, text):
        # ... (existing button_click logic) ...
        if text == "Theme" or text == "Units": return 

        if self.deg_rad_button and text == self.deg_rad_button.cget('text'):
            self.degree_mode = not self.degree_mode
            new_button_text = "Deg" if self.degree_mode else "Rad"
            if self.deg_rad_button: self.deg_rad_button.config(text=new_button_text)
            self.result_var.set("Mode: " + new_button_text); self.expression = ""; return

        active_slot = self.active_memory_slot_index
        if text == "MS": 
            try:
                value_to_store = eval(self.expression) if self.expression else float(self.result_var.get())
                self.memory_slots[active_slot] = value_to_store
                self.result_var.set(str(value_to_store)); self.expression = ""; self.save_settings()
            except Exception: self.result_var.set("Error"); self.expression = ""
            return
        elif text == "MR": self.expression = str(self.memory_slots[active_slot]); self.result_var.set(self.expression); return
        elif text == "MC": self.memory_slots[active_slot] = 0.0; self.save_settings(); return
        elif text == "M+" or text == "M-": 
            try:
                value = eval(self.expression) if self.expression else float(self.result_var.get())
                if text == "M+": self.memory_slots[active_slot] += value
                else: self.memory_slots[active_slot] -= value
                self.result_var.set(str(value)); self.expression = ""; self.save_settings()
            except Exception: self.result_var.set("Error"); self.expression = ""
            return
        elif text == "MNext": 
            self.active_memory_slot_index = (self.active_memory_slot_index + 1) % Calculator.NUM_MEMORY_SLOTS
            self.memory_slot_display_var.set(f"M{self.active_memory_slot_index + 1}"); self.save_settings(); return
        elif text == "MAC": self.memory_slots = [0.0] * Calculator.NUM_MEMORY_SLOTS; self.save_settings(); return

        if text == "=": self.calculate()
        elif text == "C": self.clear()
        elif text == "Del":
            if self.result_var.get().startswith("Mode:"): self.clear()
            else: self.delete()
        elif text == "sin": self.apply_math_func(math.sin, is_trig=True)
        elif text == "cos": self.apply_math_func(math.cos, is_trig=True)
        elif text == "tan": self.apply_tan()
        elif text == "log": self.apply_math_func(math.log10, domain_check=lambda x: x > 0)
        elif text == "ln": self.apply_math_func(math.log, domain_check=lambda x: x > 0)
        elif text == "exp": self.apply_math_func(math.exp, overflow_check=lambda x: x > 709)
        elif text == "√": self.apply_math_func(math.sqrt, domain_check=lambda x: x >= 0)
        elif text == "x²": self.apply_power(2)
        elif text == "x³": self.apply_power(3)
        elif text == "^":
            if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')'): self.expression += "**"
            elif not self.expression and self.result_var.get() not in ["0", "Error", "Mode: Rad", "Mode: Deg"]: self.expression = self.result_var.get() + "**"
            else: pass 
            self.result_var.set(self.expression)
        elif text == "π": self.expression = str(math.pi); self.result_var.set(self.expression)
        elif text == "e": self.expression = str(math.e); self.result_var.set(self.expression)
        else: 
            if self.result_var.get().startswith("Mode:"): self.expression = ""; self.result_var.set("0")
            if not text.isdigit() and not text == ".": 
                if not self.expression and text in ["*", "/", "+", "%"]: return
                if self.expression and self.expression[-1] in ["+", "-", "*", "/", ".", "**"]: 
                    if text == self.expression[-1] and text == "*": pass 
                    elif text in ["+", "-", "*", "/","."]: return 
            self.expression += text
            self.result_var.set(self.expression)

    def apply_math_func(self, func, is_trig=False, domain_check=None, overflow_check=None):
        try:
            value = eval(self.expression)
            if domain_check and not domain_check(value): self.result_var.set("Error"); self.expression = ""; return
            if overflow_check and overflow_check(value): self.result_var.set("Error"); self.expression = ""; return
            if is_trig and self.degree_mode: value = math.radians(value)
            result = func(value)
            self.expression = str(result); self.result_var.set(self.expression)
        except Exception: self.result_var.set("Error"); self.expression = ""
            
    def apply_tan(self):
        try:
            value = eval(self.expression)
            angle_rad = math.radians(value) if self.degree_mode else value
            if abs(math.cos(angle_rad)) < 1e-12: self.result_var.set("Error"); self.expression = ""
            else:
                result = math.tan(angle_rad)
                self.expression = str(result); self.result_var.set(self.expression)
        except Exception: self.result_var.set("Error"); self.expression = ""

    def apply_power(self, power):
        try:
            value = eval(self.expression)
            result = value ** power
            self.expression = str(result); self.result_var.set(self.expression)
        except Exception: self.result_var.set("Error"); self.expression = ""

    def calculate(self):
        try:
            if "Error" in self.expression: self.result_var.set("Error"); self.expression = ""; return
            if self.expression.endswith("**") or self.expression.endswith(("+", "-", "*", "/")): self.result_var.set("Error"); return
            original_expression = self.expression 
            result = str(eval(self.expression))
            history_entry = f"{original_expression}={result}"
            self.history.append(history_entry)
            self.update_history_display() 
            self.save_settings() 
            self.result_var.set(result); self.expression = result
        except ZeroDivisionError: self.result_var.set("Error"); self.expression = ""
        except (SyntaxError, NameError, TypeError): self.result_var.set("Error"); self.expression = ""
        except Exception: self.result_var.set("Error"); self.expression = ""

    def delete(self):
        if self.expression:
            self.expression = self.expression[:-1]
            self.result_var.set(self.expression if self.expression else "0")
        elif self.result_var.get() not in ["0", "Error"] and not self.result_var.get().startswith("Mode:"):
            self.expression = ""; self.result_var.set("0")

    def clear(self):
        self.expression = ""; self.result_var.set("0")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
