import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import json
import os
import sys
import ctypes  # For Windows font loading
import pathlib # <-- ADDED FOR MACOS APP SUPPORT

# --- Constants ---
# App Name
APP_NAME = "Vitagotchi"

# Get the standard user-writable data directory for macOS/Windows
# macOS path: /Users/YourName/Library/Application Support/Vitagotchi
# Windows path: C:\Users\YourName\AppData\Roaming\Vitagotchi
if sys.platform == "win32":
    DATA_DIR = pathlib.Path(os.environ.get("APPDATA", pathlib.Path.home())) / APP_NAME
elif sys.platform == "darwin": # macOS
    DATA_DIR = pathlib.Path.home() / "Library" / "Application Support" / APP_NAME
else: # Linux/Other
    DATA_DIR = pathlib.Path.home() / ".local" / "share" / APP_NAME

# Create the directory if it doesn't exist
try:
    os.makedirs(DATA_DIR, exist_ok=True)
except Exception as e:
    print(f"Error creating data directory: {e}")
    # Fallback to current directory if creation fails (for debugging)
    DATA_DIR = pathlib.Path(".")

# File paths for writable data
DB_FILE = DATA_DIR / "patient_database.json"
COUNTER_FILE = DATA_DIR / "patient_id_counter.txt"


def get_assets_dir():
    """
    Get the absolute path to the assets directory.
    This handles running as a script vs. a bundled PyInstaller .exe.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'assets')
    else:
        # Running as a normal Python script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')


ASSETS_DIR = get_assets_dir()

# --- Colors ---
BG_COLOR = "#F0F8FF"        # AliceBlue
CONTENT_BG = "#FFFFFF"      # White
PRIMARY_BLUE = "#6495ED"    # CornflowerBlue
ACCENT_GREEN = "#98FB98"    # PaleGreen
ACCENT_PINK = "#FFB6C1"     # LightPink
MUTED_COLOR = "#B0C4DE"      # LightSteelBlue
TEXT_COLOR = "#363636"      # Dark gray
PLACEHOLDER_COLOR = "grey"
ERROR_COLOR = "#FF6347"     # Tomato
HEALTHY_COLOR = "#32CD32"   # LimeGreen
WARNING_COLOR = "#FFA500"   # Orange

# --- Fonts ---
FONT_NAME = "Press Start 2P"
FONT_LARGE_BOLD = (FONT_NAME, 24, "bold")
FONT_MEDIUM_BOLD = (FONT_NAME, 18, "bold")
FONT_REGULAR_BOLD = (FONT_NAME, 14, "bold")
FONT_BUDDY = (FONT_NAME, 20, "bold")
FONT_REGULAR = (FONT_NAME, 12)
FONT_SMALL = (FONT_NAME, 10)
FONT_TINY = (FONT_NAME, 8, "bold")


# --- Avatar Configuration ---
# Default positions and scales
DEFAULT_HEAD_SCALE = 0.63
DEFAULT_HEAD_POS = {"x": 283.0, "y": 266.0}
DEFAULT_SAD_HEAD_SETTINGS = {"x": 283.0, "y": 266.0, "scale": 0.63}
DEFAULT_SICK_HEAD_SETTINGS = {"x": 283.0, "y": 266.0, "scale": 0.63}

# Special settings for specific assets (overrides defaults)
SPECIAL_HEAD_SETTINGS = {
    "Head M4": {"x": 283.0, "y": 270.0, "scale": 0.63},
    "Head M5": {"x": 283.0, "y": 270.0, "scale": 0.63},
    "Head F1": {"x": 298.0, "y": 342.0, "scale": 1.096},
    "Head F2": {"x": 296.0, "y": 309.0, "scale": 1.000},
    "Head F3": {"x": 299.0, "y": 325.0, "scale": 1.163},
    "Head F4": {"x": 299.0, "y": 325.0, "scale": 1.163},
    "Head F5": {"x": 296.0, "y": 319.0, "scale": 0.172}
}

SPECIAL_SAD_HEAD_SETTINGS = {
    "Head M1": {"x": 286.0, "y": 256.0, "scale": 1.417},
    "Head M2": {"x": 286.0, "y": 256.0, "scale": 1.417},
    "Head M3": {"x": 284.0, "y": 273.0, "scale": 0.316},
    "Head M4": {"x": 286.0, "y": 256.0, "scale": 1.417},
    "Head M5": {"x": 286.0, "y": 256.0, "scale": 1.417},
    "Head F1": {"x": 294.0, "y": 331.0, "scale": 0.700},
    "Head F2": {"x": 292.0, "y": 308.0, "scale": 0.232},
    "Head F3": {"x": 302.0, "y": 334.0, "scale": 0.700},
    "Head F4": {"x": 300.0, "y": 326.0, "scale": 0.700},
    "Head F5": {"x": 301.0, "y": 335.0, "scale": 0.700}
}

SPECIAL_SICK_HEAD_SETTINGS = {
    "Head M1": {"x": 286.0, "y": 256.0, "scale": 1.417},
    "Head M2": {"x": 287.0, "y": 252.0, "scale": 1.417},
    "Head M3": {"x": 286.0, "y": 257.0, "scale": 0.254},
    "Head M4": {"x": 286.0, "y": 260.0, "scale": 1.417},
    "Head M5": {"x": 280.0, "y": 259.0, "scale": 1.417},
    "Head F1": {"x": 293.0, "y": 326.0, "scale": 0.197},
    "Head F2": {"x": 292.0, "y": 308.0, "scale": 0.232},
    "Head F3": {"x": 304.0, "y": 334.0, "scale": 0.209},
    "Head F4": {"x": 300.0, "y": 326.0, "scale": 0.209},
    "Head F5": {"x": 300.0, "y": 329.0, "scale": 0.284}
}

# --- Male Assets ---
CLOTHES_DATA = {
    "Clothes M1": {"file": "clothes_m1.png", "x": 280.0, "y": 541.0, "scale": 0.65},
    "Clothes M2": {"file": "clothes_m2.png", "x": 286.0, "y": 541.0, "scale": 0.65},
    "Clothes M3": {"file": "clothes_m3.png", "x": 293.0, "y": 515.0, "scale": 0.62},
    "Clothes M4": {"file": "clothes_m4.png", "x": 285.0, "y": 534.0, "scale": 0.61},
    "Clothes M5": {"file": "clothes_m5.png", "x": 287.0, "y": 536.0, "scale": 0.52}
}
HEAD_FILES = [f"head_m{i}.png" for i in range(1, 6)]

# --- Female Assets ---
CLOTHES_DATA_FEMALE = {
    "Clothes F1": {"file": "clothes_f1.png", "x": 298.0, "y": 539.0, "scale": 1.087},
    "Clothes F2": {"file": "clothes_f2.png", "x": 303.0, "y": 536.0, "scale": 1.087},
    "Clothes F3": {"file": "clothes_f3.png", "x": 305.0, "y": 536.0, "scale": 1.087},
    "Clothes F4": {"file": "clothes_f4.png", "x": 299.0, "y": 539.0, "scale": 1.131},
    "Clothes F5": {"file": "clothes_f5.png", "x": 301.0, "y": 541.0, "scale": 1.131}
}
HEAD_FILES_FEMALE = [f"head_f{i}.png" for i in range(1, 6)]


# ===================================================================
# HELPER WIDGET CLASS
# ===================================================================

class PlaceholderEntry(tk.Entry):
    """
    A custom tk.Entry widget that supports placeholder text.
    """
    def __init__(self, master, placeholder, *args, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = FONT_REGULAR
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.is_placeholder = False

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self.set_placeholder()

    def set_placeholder(self):
        """Inserts the placeholder text and styles it."""
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self.config(fg=PLACEHOLDER_COLOR)
        self.is_placeholder = True

    def _on_focus_in(self, event):
        """Removes placeholder text on focus."""
        if self.is_placeholder:
            self.delete(0, tk.END)
            self.config(fg=TEXT_COLOR)
            self.is_placeholder = False

    def _on_focus_out(self, event):
        """Adds placeholder text back if entry is empty."""
        if not self.get():
            self.set_placeholder()

    def get_value(self):
        """Returns the entry's value, or an empty string if it's a placeholder."""
        return "" if self.is_placeholder else self.get()
        
    def set_value(self, text):
        """Sets the entry's value, removing any placeholder."""
        self.delete(0, tk.END)
        self.insert(0, text)
        self.config(fg=TEXT_COLOR)
        self.is_placeholder = False

    def reset(self):
        """Resets the entry to its placeholder state."""
        self.set_placeholder()

# ===================================================================
# MAIN APPLICATION CLASS
# ===================================================================

class VitagotchiApp(tk.Tk):
    """
    Main application class for the Vitagotchi Patient Setup.
    Manages all stages, data, and UI logic.
    """
    def __init__(self):
        super().__init__()
        self.title("Vitagotchi")
        self.state('zoomed')
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)

        # --- Core Data Storage ---
        self.patient_id_counter = self._load_json_data(COUNTER_FILE, 0)
        self.all_patients_db = self._load_json_data(DB_FILE, {})
        
        # --- Background Image Storage ---
        self.background_images_pil = {}  # Stores the PIL Image objects
        self.background_image_refs = {}  # Stores the final ImageTk.PhotoImage refs
        
        # Holds info for the *current* session
        self.session_data = {} 
        
        # Temporary selections during the avatar stage
        self.avatar_selection = {'head': None, 'clothes': None}

        # --- Asset Storage ---
        self.head_images = {}
        self.sad_head_images = {}
        self.sick_head_images = {}
        self.clothes_images = {}
        self.head_images_female = {}
        self.sad_head_images_female = {}
        self.sick_head_images_female = {}
        self.clothes_images_female = {}
        
        # --- Storage for selection buttons ---
        self.head_buttons = {"male": {}, "female": {}}
        self.clothes_buttons = {"male": {}, "female": {}}
        
        self._load_assets()
        self._load_custom_font()

        # --- Calibration Mode (F11/F12) ---
        self.calib_mode = False
        self.calib_drag_data = {"item_tag": None, "x": 0, "y": 0}
        self.calib_current_canvas = None
        self.calib_canvas_ids = {'head': None, 'clothes': None}
        self.calib_status_expression = "normal"
        self.calib_settings = {
            'head': {'pos': DEFAULT_HEAD_POS.copy(), 'scale': DEFAULT_HEAD_SCALE},
            'clothes': {'pos': {'x': 0, 'y': 0}, 'scale': 1.0}
        }
        self.calibration_label = None
        self.calibration_label_status = None

        # --- Key Bindings ---
        self.bind("<F12>", self.toggle_calibration)
        self.bind("<F11>", self.toggle_calibration)
        self.bind("<Up>", lambda e: self.on_calib_key_scale("Up"))
        self.bind("<Down>", lambda e: self.on_calib_key_scale("Down"))
        self.bind("1", lambda e: self.on_calib_key_press(e, 'head'))
        self.bind("2", lambda e: self.on_calib_key_press(e, 'clothes'))

        # --- Main UI Container (Stacked Frame/Page Layout) ---
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # --- Global Background Label ---
        # This will be the parent for all stage frames.
        self.background_label = tk.Label(self.main_container)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.stage_frames = {}
        self.current_stage = "Welcome"
        
        stage_names = ("Welcome", "Login", "PatientInfo", "Avatar", 
                       "Congrats", "Vitals", "Status", "DatabaseView")

        for stage_name in stage_names:
            # Frame is a child of the background_label
            frame = tk.Frame(self.background_label) 
            
            # Configure frame to be transparent
            frame.configure(bg="") 
            
            # Make the frame fill the background_label
            frame.place(x=0, y=0, relwidth=1, relheight=1)
            
            self.stage_frames[stage_name] = frame
            frame.lower()  # Hide the frame initially

        # --- Build the static UI for each page ---
        self._build_welcome_stage(self.stage_frames["Welcome"])
        self._build_login_stage(self.stage_frames["Login"])
        self._build_patient_info_stage(self.stage_frames["PatientInfo"])
        self._build_avatar_stage(self.stage_frames["Avatar"])
        self._build_congrats_stage(self.stage_frames["Congrats"])
        self._build_vitals_stage(self.stage_frames["Vitals"])
        self._build_status_stage(self.stage_frames["Status"])
        self._build_database_view_stage(self.stage_frames["DatabaseView"])

        # --- Initialize ---
        # Load backgrounds AFTER window is drawn and sized
        self.after(100, self._load_background_images) 
        
        # Show the first stage
        self.reset_and_show_welcome()

    def _load_custom_font(self):
        """Loads the custom font from the assets directory."""
        font_filename = 'PressStart2P-Regular.ttf'
        font_path = os.path.join(ASSETS_DIR, font_filename)
        
        if sys.platform == "win32":
            try:
                # Check if font is already loaded
                if not ctypes.windll.gdi32.AddFontResourceW(font_path):
                     print(f"Font '{font_filename}' may already be loaded.")
                else:
                    print(f"Successfully loaded font: {font_filename}")
            except Exception as e:
                print(f"ERROR: Could not load font '{font_filename}'. {e}")
        elif sys.platform == "darwin":
            # Font loading on macOS is handled differently, often by installing
            # the font on the system or using platform-specific libraries.
            # For PyInstaller, bundling the font and referring by name
            # *should* work if the name matches the font's internal name.
            # Tkinter on macOS *should* find it by name if loaded.
            print(f"On macOS, ensure font '{font_filename}' is installed or loaded if bundling.")
        else:
            print(f"Font loading not implemented for {sys.platform}.")


    # ===================================================================
    # STAGE (PAGE) NAVIGATION
    # ===================================================================

    def show_stage(self, stage_name):
        """Brings the specified stage (frame) to the front."""
        self.current_stage = stage_name
        frame = self.stage_frames.get(stage_name)
        
        # Update background image
        bg_image_ref = self.background_image_refs.get(stage_name)
        if bg_image_ref:
            self.background_label.config(image=bg_image_ref)
            self.background_label.image = bg_image_ref  # Keep reference
        
        if frame:
            frame.tkraise()
        else:
            print(f"Error: Stage '{stage_name}' not found.")
            
        # If we navigate away, ensure calibration mode is off
        if self.calib_mode and self.current_stage not in ("Avatar", "Status"):
            self.toggle_calibration()
            
    def reset_and_show_welcome(self):
        """
        Resets all session data and UI elements to their default
        state and returns to the Welcome screen.
        """
        self.session_data = {}
        self.avatar_selection = {'head': None, 'clothes': None}
        
        if self.calib_mode:
            self.toggle_calibration()

        # Reset Login Screen
        if hasattr(self, 'login_first_name_entry'):
            self.login_first_name_entry.reset()
            self.login_last_name_entry.reset()

        # Reset Patient Info Screen
        if hasattr(self, 'info_first_name_entry'):
            self.info_first_name_entry.reset()
            self.info_last_name_entry.reset()
            self.mm_entry.reset()
            self.dd_entry.reset()
            self.yyyy_entry.reset()
            self.sex_var.set("Male")

        # Reset Avatar Screen
        if hasattr(self, 'avatar_canvas'):
            self._draw_avatar_on_canvas(self.avatar_canvas, None, None, "normal")
            self.avatar_male_options_frame.tkraise()

        # Reset button highlights
        for g in ["male", "female"]:
            for btn_dict in [self.head_buttons, self.clothes_buttons]:
                for btn in btn_dict[g].values():
                    btn.config(relief="flat", bg=CONTENT_BG, bd=0)

        # Reset Vitals Screen
        if hasattr(self, 'hr_entry'):
            self.hr_entry.config(validate='none')
            self.hr_entry.reset()
            self.temp_entry.config(validate='none')
            self.temp_entry.reset()
            self.systolic_entry.config(validate='none')
            self.systolic_entry.reset()
            self.diastolic_entry.config(validate='none')
            self.diastolic_entry.reset()
        
        self.show_stage("Welcome")
        
    def show_database_view(self):
        """Refreshes the database view and shows it."""
        self._refresh_database_view()
        self.show_stage("DatabaseView")

    # ===================================================================
    # STAGE BUILDER METHODS (Called ONCE at __init__)
    # ===================================================================

    def _build_welcome_stage(self, parent):
        """Builds the UI for the Welcome screen."""
        welcome_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1, padx=20, pady=20)
        welcome_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(welcome_box, text="Welcome to VitaGotchi", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR, padx=20, pady=10).pack(pady=30)
        tk.Label(welcome_box, text="Please select an option", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR, padx=20, pady=10).pack(pady=20)

        buttons_frame = tk.Frame(welcome_box, bg=CONTENT_BG)
        buttons_frame.pack(pady=20, padx=20)

        new_patient_button = tk.Button(buttons_frame, text="New Patient", font=FONT_REGULAR_BOLD,
                                       bg=PRIMARY_BLUE, fg=CONTENT_BG, 
                                       command=lambda: self.show_stage("PatientInfo"), 
                                       relief="flat", padx=30, pady=15)
        new_patient_button.pack(side="left", padx=20)

        existing_patient_button = tk.Button(buttons_frame, text="Existing Patient", font=FONT_REGULAR_BOLD,
                                            bg=ACCENT_GREEN, fg=TEXT_COLOR, 
                                            command=lambda: self.show_stage("Login"), 
                                            relief="flat", padx=30, pady=15)
        existing_patient_button.pack(side="left", padx=20)
        
        db_button_frame = tk.Frame(welcome_box, bg=CONTENT_BG)
        db_button_frame.pack(pady=20, padx=20, fill='x')
        
        database_button = tk.Button(db_button_frame, text="Patient Database", font=FONT_REGULAR_BOLD,
                                    bg=MUTED_COLOR, fg=TEXT_COLOR, 
                                    command=self.show_database_view,
                                    relief="flat", padx=30, pady=15)
        database_button.pack()

    def _build_login_stage(self, parent):
        """Builds the UI for the Existing Patient Login screen."""
        login_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1, padx=20, pady=20)
        login_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_box, text="Existing Patient Login", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=30)

        form_frame = tk.Frame(login_box, bg=CONTENT_BG)
        form_frame.pack(pady=20, padx=50)

        tk.Label(form_frame, text="Patient Name:", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        name_frame = tk.Frame(form_frame, bg=CONTENT_BG)
        name_frame.grid(row=0, column=1, sticky="ew", pady=10, padx=10)
        
        vcmd_alpha = (self.register(self.validate_vitals_alpha_space), '%P')
        
        self.login_first_name_entry = PlaceholderEntry(name_frame, "First Name", font=FONT_REGULAR, width=18)
        self.login_last_name_entry = PlaceholderEntry(name_frame, "Last Name", font=FONT_REGULAR, width=18)
        
        self.login_first_name_entry.bind("<FocusIn>", lambda e, cmd=vcmd_alpha: self.on_vitals_focus_in(e, cmd), add="+")
        self.login_last_name_entry.bind("<FocusIn>", lambda e, cmd=vcmd_alpha: self.on_vitals_focus_in(e, cmd), add="+")
        self.login_first_name_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")
        self.login_last_name_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")

        self.login_first_name_entry.pack(side="left", expand=True, fill='x', padx=(0, 5))
        self.login_last_name_entry.pack(side="left", expand=True, fill='x', padx=(5, 0))

        login_button = tk.Button(login_box, text="Login & Input Vitals", font=FONT_REGULAR_BOLD,
                                 bg=PRIMARY_BLUE, fg=CONTENT_BG, 
                                 command=self.process_login, 
                                 relief="flat", padx=20, pady=10)
        login_button.pack(pady=40)
        
        back_button = tk.Button(login_box, text="← Back", font=FONT_SMALL,
                                  bg=MUTED_COLOR, fg=TEXT_COLOR, 
                                  command=self.reset_and_show_welcome, 
                                  relief="flat", padx=10, pady=5)
        back_button.pack(pady=10)

    def _build_patient_info_stage(self, parent):
        """Builds the UI for the New Patient Info screen."""
        info_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1, padx=20, pady=20)
        info_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(info_box, text="New Patient Info", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=30)

        form_frame = tk.Frame(info_box, bg=CONTENT_BG)
        form_frame.pack(pady=20, padx=50)

        # Patient Name
        tk.Label(form_frame, text="Patient Name:", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        name_frame = tk.Frame(form_frame, bg=CONTENT_BG)
        name_frame.grid(row=0, column=1, sticky="ew", pady=10, padx=10)
        
        vcmd_alpha = (self.register(self.validate_vitals_alpha_space), '%P')
        
        self.info_first_name_entry = PlaceholderEntry(name_frame, "First Name", font=FONT_REGULAR, width=18)
        self.info_last_name_entry = PlaceholderEntry(name_frame, "Last Name", font=FONT_REGULAR, width=18)
        self.info_first_name_entry.bind("<FocusIn>", lambda e, cmd=vcmd_alpha: self.on_vitals_focus_in(e, cmd), add="+")
        self.info_last_name_entry.bind("<FocusIn>", lambda e, cmd=vcmd_alpha: self.on_vitals_focus_in(e, cmd), add="+")
        self.info_first_name_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")
        self.info_last_name_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")
        self.info_first_name_entry.pack(side="left", expand=True, fill='x', padx=(0, 5))
        self.info_last_name_entry.pack(side="left", expand=True, fill='x', padx=(5, 0))

        # Birthdate
        tk.Label(form_frame, text="Birthdate:", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        birthdate_frame = tk.Frame(form_frame, bg=CONTENT_BG)
        birthdate_frame.grid(row=1, column=1, sticky="w", pady=10, padx=10)

        self.mm_entry = PlaceholderEntry(birthdate_frame, "MM", font=FONT_REGULAR, width=3, justify='center')
        self.dd_entry = PlaceholderEntry(birthdate_frame, "DD", font=FONT_REGULAR, width=3, justify='center')
        self.yyyy_entry = PlaceholderEntry(birthdate_frame, "YYYY", font=FONT_REGULAR, width=5, justify='center')
        self.mm_entry.pack(side="left")
        tk.Label(birthdate_frame, text="/", font=FONT_REGULAR, bg=CONTENT_BG, fg=TEXT_COLOR).pack(side="left")
        self.dd_entry.pack(side="left")
        tk.Label(birthdate_frame, text="/", font=FONT_REGULAR, bg=CONTENT_BG, fg=TEXT_COLOR).pack(side="left")
        self.yyyy_entry.pack(side="left")
        
        # Validation and auto-tab
        self.mm_entry.bind("<KeyRelease>", lambda e: self.handle_date_key_release(e, self.dd_entry, 2))
        self.dd_entry.bind("<KeyRelease>", lambda e: self.handle_date_key_release(e, self.yyyy_entry, 2))
        self.yyyy_entry.bind("<KeyRelease>", lambda e: self.handle_date_key_release(e, None, 4))

        # Live Validation on FocusOut
        self.mm_entry.bind("<FocusOut>", self.validate_month_entry, add="+")
        self.dd_entry.bind("<FocusOut>", self.validate_day_entry, add="+")
        self.yyyy_entry.bind("<FocusOut>", self.validate_year_entry, add="+")

        # Sex
        tk.Label(form_frame, text="Sex:", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        self.sex_var = tk.StringVar(value="Male")
        radio_frame = tk.Frame(form_frame, bg=CONTENT_BG)
        male_radio = tk.Radiobutton(radio_frame, text="Male", variable=self.sex_var, value="Male", 
                                    font=FONT_SMALL, bg=CONTENT_BG, activebackground=CONTENT_BG, 
                                    fg=TEXT_COLOR, selectcolor=CONTENT_BG)
        female_radio = tk.Radiobutton(radio_frame, text="Female", variable=self.sex_var, value="Female", 
                                      font=FONT_SMALL, bg=CONTENT_BG, activebackground=CONTENT_BG, 
                                      fg=TEXT_COLOR, selectcolor=CONTENT_BG)
        male_radio.pack(side="left", padx=5)
        female_radio.pack(side="left", padx=5)
        radio_frame.grid(row=2, column=1, sticky="w", pady=10, padx=10)

        # Navigation Buttons
        buttons_frame = tk.Frame(info_box, bg=CONTENT_BG)
        buttons_frame.pack(pady=40, fill='x', expand=True)

        back_button = tk.Button(buttons_frame, text="← Back", font=FONT_REGULAR_BOLD,
                                  bg=MUTED_COLOR, fg=TEXT_COLOR, 
                                  command=self.reset_and_show_welcome, 
                                  relief="flat", padx=20, pady=10)
        back_button.pack(side="left", padx=10)
        
        next_button = tk.Button(buttons_frame, text="Next →", font=FONT_REGULAR_BOLD,
                                  bg=PRIMARY_BLUE, fg=CONTENT_BG, 
                                  command=self.process_patient_info, 
                                  relief="flat", padx=20, pady=10)
        next_button.pack(side="right", padx=10)

    def _build_avatar_stage(self, parent):
        """Builds the UI for the Avatar Customization screen."""
        avatar_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1)
        avatar_box.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)
        
        avatar_box.grid_rowconfigure(0, weight=1)
        avatar_box.grid_columnconfigure(0, weight=1)
        avatar_box.grid_columnconfigure(1, weight=1)
 
        # Left Frame for Avatar Preview
        left_frame = tk.Frame(avatar_box, bg="#E6E6FA")  # Lavender "Stage"
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        canvas_container = tk.Frame(left_frame, bg="#E6E6FA")
        canvas_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.avatar_canvas = tk.Canvas(canvas_container, width=600, height=800, 
                                       bg=CONTENT_BG, highlightthickness=0, 
                                       relief="solid", bd=2)
        self.avatar_canvas.pack()
        
        # Calibration Info Label (hidden by default)
        self.calibration_label = tk.Label(left_frame, text="", font=FONT_TINY, 
                                          bg="#222222", fg="#00ff00", 
                                          justify="left", anchor="nw", 
                                          padx=10, pady=10, 
                                          relief="solid", borderwidth=1)

        # Right Frame for Customization Options
        right_frame = tk.Frame(avatar_box, bg=CONTENT_BG, bd=1, relief="solid")
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        # ===================================================================
        # START OF LAYOUT FIX
        # ===================================================================
        
        # --- FIX: Pack the button FIRST ---
        # This reserves space at the bottom of right_frame.
        tk.Button(right_frame, text="✅ Confirm Buddy", font=FONT_REGULAR_BOLD,
                  bg=ACCENT_GREEN, fg=TEXT_COLOR, 
                  command=self.process_avatar_selection, 
                  relief="flat", padx=20, pady=10).pack(side="bottom", pady=20)

        # --- FIX: Pack the container SECOND ---
        # It will now expand to fill the *remaining* space above the button.
        container = tk.Frame(right_frame, bg=CONTENT_BG)
        container.pack(fill="both", expand=True)
        
        # ===================================================================
        # END OF LAYOUT FIX
        # ===================================================================

        # Simple non-scrolling frame for options
        options_frame = tk.Frame(container, bg=CONTENT_BG)
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(options_frame, text="Customize Your Buddy!", font=FONT_BUDDY, 
                 bg=CONTENT_BG, fg=PRIMARY_BLUE).pack(pady=30)

        # Options Container
        self.avatar_options_container = tk.Frame(options_frame, bg=CONTENT_BG)
        self.avatar_options_container.pack(fill="both", expand=True)
        self.avatar_options_container.grid_rowconfigure(0, weight=1)
        self.avatar_options_container.grid_columnconfigure(0, weight=1)

        self.avatar_male_options_frame = tk.Frame(self.avatar_options_container, bg=CONTENT_BG)
        self.avatar_female_options_frame = tk.Frame(self.avatar_options_container, bg=CONTENT_BG)
        self.avatar_male_options_frame.grid(row=0, column=0, sticky="nsew")
        self.avatar_female_options_frame.grid(row=0, column=0, sticky="nsew")

        # Populate the frames
        self._populate_avatar_options(self.avatar_male_options_frame, self.head_images, 
                                      self.clothes_images, "male")
        self._populate_avatar_options(self.avatar_female_options_frame, self.head_images_female, 
                                      self.clothes_images_female, "female")
        
        self.avatar_male_options_frame.tkraise()

        # --- FIX: The Confirm Button was moved from here up ---

    def _populate_avatar_options(self, parent, head_dict, clothes_dict, gender_key):
        """Helper to build the buttons for a given set of assets."""
        tk.Label(parent, text="Choose a Head:", font=FONT_REGULAR_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=(15, 5))
        head_frame = tk.Frame(parent, bg=CONTENT_BG)
        head_frame.pack(pady=5)
        
        self.head_buttons[gender_key] = {}
        
        for head_name, img_data in head_dict.items():
            base_width = 140 if head_name in ("Head F5", "Head F2") else 80
            if img_data.width == 0: 
                continue
            
            w_percent = (base_width / float(img_data.width))
            h_size = max(1, int((float(img_data.height) * float(w_percent))))
            preview = ImageTk.PhotoImage(img_data.resize((base_width, h_size), 
                                         Image.Resampling.LANCZOS))
            
            btn = tk.Button(head_frame, image=preview, 
                            command=lambda h=head_name, g=gender_key: self.select_head(h, g), 
                            relief="flat", bg=CONTENT_BG, bd=0, activebackground=CONTENT_BG)
            btn.image = preview
            btn.pack(side="left", padx=10, pady=5)
            self.head_buttons[gender_key][head_name] = btn

        tk.Label(parent, text="Choose Clothes:", font=FONT_REGULAR_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=(20, 5))
        clothes_frame = tk.Frame(parent, bg=CONTENT_BG)
        clothes_frame.pack(pady=5)
        
        self.clothes_buttons[gender_key] = {}
        
        for cloth_name, data in clothes_dict.items():
            img = data["img"]
            base_width = 65 if cloth_name == "Clothes M5" else 80
            if img.width == 0: 
                continue
                
            w_percent = (base_width / float(img.width))
            h_size = max(1, int((float(img.height) * float(w_percent))))
            preview = ImageTk.PhotoImage(img.resize((base_width, h_size), 
                                         Image.Resampling.LANCZOS))

            btn = tk.Button(clothes_frame, image=preview, 
                            command=lambda c=cloth_name, g=gender_key: self.select_clothes(c, g), 
                            relief="flat", bg=CONTENT_BG, bd=0, activebackground=CONTENT_BG)
            btn.image = preview
            btn.pack(side="left", padx=10, pady=5)
            self.clothes_buttons[gender_key][cloth_name] = btn

    def _build_congrats_stage(self, parent):
        """Builds the UI for the Congratulations screen."""
        congrats_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1, padx=30, pady=30)
        congrats_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(congrats_box, text="🎉 Congrats! 🎉", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=30)
        tk.Label(congrats_box, text="Your buddy is ready!\nPlease hand the device back.",
                 font=FONT_REGULAR, bg=CONTENT_BG, fg=TEXT_COLOR, 
                 justify="center").pack(pady=20)
        tk.Button(congrats_box, text="Proceed to Vitals", font=FONT_REGULAR_BOLD,
                  bg=PRIMARY_BLUE, fg=CONTENT_BG, 
                  command=lambda: self.show_stage("Vitals"), 
                  relief="flat", padx=20, pady=10).pack(pady=40)

    def _build_vitals_stage(self, parent):
        """Builds the UI for the Vitals Input screen."""
        vitals_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1, padx=20, pady=20)
        vitals_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(vitals_box, text="Input Child's Vitals", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=30)
        
        vitals_frame = tk.Frame(vitals_box, bg=CONTENT_BG)
        vitals_frame.pack(pady=20, padx=50)

        vcmd_numeric = (self.register(self.validate_vitals_numeric), '%P', 3)
        vcmd_decimal = (self.register(self.validate_vitals_decimal), '%P', 4)

        # Heart Rate
        tk.Label(vitals_frame, text="Heart Rate (bpm):", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        self.hr_entry = PlaceholderEntry(vitals_frame, "e.g., 80", font=FONT_REGULAR, width=20)
        self.hr_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=10)
        self.hr_entry.bind("<FocusIn>", lambda e, cmd=vcmd_numeric: self.on_vitals_focus_in(e, cmd), add="+")
        self.hr_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")

        # Blood Pressure
        tk.Label(vitals_frame, text="Blood Pressure (mmHg):", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        bp_frame = tk.Frame(vitals_frame, bg=CONTENT_BG)
        bp_frame.grid(row=1, column=1, sticky="w")
        self.systolic_entry = PlaceholderEntry(bp_frame, "e.g., 110", font=FONT_REGULAR, 
                                             width=10, justify='center')
        self.diastolic_entry = PlaceholderEntry(bp_frame, "e.g., 70", font=FONT_REGULAR, 
                                              width=10, justify='center')
        self.systolic_entry.pack(side="left")
        tk.Label(bp_frame, text="/", font=FONT_REGULAR, bg=CONTENT_BG, fg=TEXT_COLOR).pack(side="left")
        self.diastolic_entry.pack(side="left")
        self.systolic_entry.bind("<FocusIn>", lambda e, cmd=vcmd_numeric: self.on_vitals_focus_in(e, cmd), add="+")
        self.diastolic_entry.bind("<FocusIn>", lambda e, cmd=vcmd_numeric: self.on_vitals_focus_in(e, cmd), add="+")
        self.systolic_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")
        self.diastolic_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")

        # Temperature
        tk.Label(vitals_frame, text="Temperature (°C):", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        self.temp_entry = PlaceholderEntry(vitals_frame, "e.g., 37.0", font=FONT_REGULAR, width=20)
        self.temp_entry.grid(row=2, column=1, sticky="ew", pady=10, padx=10)
        self.temp_entry.bind("<FocusIn>", lambda e, cmd=vcmd_decimal: self.on_vitals_focus_in(e, cmd), add="+")
        self.temp_entry.bind("<FocusOut>", self.on_vitals_focus_out, add="+")
        
        # Submit Button
        tk.Button(vitals_box, text="Submit", font=FONT_REGULAR_BOLD,
                  bg=ACCENT_GREEN, fg=TEXT_COLOR, 
                  command=self.process_vitals, 
                  relief="flat", padx=20, pady=10).pack(pady=40)

    def _build_status_stage(self, parent):
        """Builds the UI for the final Patient Status screen."""
        status_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1)
        status_box.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        status_box.grid_rowconfigure(0, weight=1)
        status_box.grid_columnconfigure(0, weight=1)
        status_box.grid_columnconfigure(1, weight=1)

        # Left Frame for Final Avatar Display
        self.status_left_frame = tk.Frame(status_box, bg=CONTENT_BG)
        self.status_left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.status_canvas = tk.Canvas(self.status_left_frame, width=600, height=800, 
                                       bg=CONTENT_BG, highlightthickness=0)
        self.status_canvas.place(relx=0.5, rely=0.5, anchor="center")
        
        self.calibration_label_status = tk.Label(self.status_left_frame, text="", font=FONT_TINY, 
                                                 bg="#222222", fg="#00ff00",
                                                 justify="left", anchor="nw", 
                                                 padx=10, pady=10, 
                                                 relief="solid", borderwidth=1)

        # Right Frame for Patient Info and Status
        right_frame = tk.Frame(status_box, bg=CONTENT_BG)
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        # --- START OF SCROLLABLE LAYOUT FIX ---
        
        # 3. Create a container for the SCROLLABLE area
        scroll_container = tk.Frame(right_frame, bg=CONTENT_BG)
        scroll_container.pack(fill="both", expand=True, pady=20, padx=30)
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)

        # 4. Create Canvas and Scrollbar
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
        canvas = tk.Canvas(scroll_container, bg=CONTENT_BG, highlightthickness=0, yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=canvas.yview)
        
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")

        # 5. Create the frame INSIDE the canvas
        # This is where the content will go
        info_container = tk.Frame(canvas, bg=CONTENT_BG)
        info_window = canvas.create_window((0, 0), window=info_container, anchor="nw")

        # 6. Bind canvas updates
        
        # --- START: MODIFIED on_configure FUNCTION ---
        def on_configure(event):
            canvas_width = event.width
            canvas_height = event.height

            # Update canvas window width to match canvas width
            canvas.itemconfig(info_window, width=canvas_width)
            
            # Dynamically update wraplength (subtract a little padding)
            wrap_width = max(1, canvas_width - 10)
            # Add try/except block for safety during initialization
            try:
                if hasattr(self, 'status_vitals_label'):
                    self.status_vitals_label.config(wraplength=wrap_width)
                if hasattr(self, 'status_message_label'):
                    self.status_message_label.config(wraplength=wrap_width)
            except tk.TclError:
                pass # Widget might not exist yet

            # Update scrollregion
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # --- FIX: Center content if it's smaller than the canvas ---
            info_height = info_container.winfo_reqheight()
            
            new_y = 0
            if info_height < canvas_height:
                # Calculate vertical padding
                new_y = (canvas_height - info_height) // 2
            
            # Horizontally center by setting x to half canvas width
            new_x = canvas_width // 2
            
            # Set anchor to "n" (top-center)
            canvas.itemconfig(info_window, anchor="n")
            # Set coordinates using canvas.coords()
            canvas.coords(info_window, new_x, new_y)
        # --- END: MODIFIED on_configure FUNCTION ---

        def on_mouse_wheel(event):
            # Linux scroll down/up
            if event.num == 5:
                canvas.yview_scroll(1, "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            # Windows/macOS scroll
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Configure>", on_configure)
        # Bind mouse wheel to canvas
        canvas.bind("<MouseWheel>", on_mouse_wheel) 
        canvas.bind("<Button-4>", on_mouse_wheel) # Linux scroll up
        canvas.bind("<Button-5>", on_mouse_wheel) # Linux scroll down
        
        # --- Center info_container inside canvas ---
        # This makes it look better on large screens
        info_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # --- END OF SCROLLABLE LAYOUT FIX ---
        
        # All content is now packed into the expanding 'info_container'
        
        # --- MOVED INSIDE info_container ---
        tk.Label(info_container, text="Patient's Status", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=30)
        
        self.status_name_label = tk.Label(info_container, text="Name: N/A", font=FONT_REGULAR, 
                                          bg=CONTENT_BG, fg=TEXT_COLOR)
        self.status_name_label.pack(pady=5, fill='x')
        self.status_age_label = tk.Label(info_container, text="Age: N/A", font=FONT_REGULAR, 
                                         bg=CONTENT_BG, fg=TEXT_COLOR)
        self.status_age_label.pack(pady=5, fill='x')
        self.status_sex_label = tk.Label(info_container, text="Sex: N/A", font=FONT_REGULAR, 
                                         bg=CONTENT_BG, fg=TEXT_COLOR)
        self.status_sex_label.pack(pady=5, fill='x')
        self.status_id_label = tk.Label(info_container, text="Patient ID: N/A", font=FONT_REGULAR, 
                                        bg=CONTENT_BG, fg=TEXT_COLOR)
        self.status_id_label.pack(pady=5, fill='x')
        
        self.status_vitals_label = tk.Label(info_container, text="Status: N/A", font=FONT_MEDIUM_BOLD, 
                                            bg=CONTENT_BG, fg=TEXT_COLOR, 
                                            justify="center") # Wraplength set by on_configure
        self.status_vitals_label.pack(pady=40, fill='x')
        
        self.status_message_label = tk.Label(info_container, text="", font=FONT_SMALL, 
                                             bg=CONTENT_BG, fg=TEXT_COLOR, 
                                             justify="center") # Wraplength set by on_configure
        self.status_message_label.pack(pady=10, fill='x')

        # --- MOVED INSIDE info_container (in _build_status_stage) ---
        new_session_button = tk.Button(info_container, text="↻ New Session", font=FONT_REGULAR_BOLD,
                                       bg=MUTED_COLOR, fg=TEXT_COLOR, 
                                       command=self.reset_and_show_welcome, 
                                       relief="flat", padx=20, pady=10)
        new_session_button.pack(pady=40)

        # --- FIX: Bind mouse wheel recursively to all content ---
        # This ensures scrolling works even when hovering over labels/buttons
        self._bind_mouse_wheel_recursively(info_container, on_mouse_wheel)

    def _build_database_view_stage(self, parent):
        """Builds the UI for the new Patient Database screen."""
        db_box = tk.Frame(parent, bg=CONTENT_BG, relief="solid", bd=1, padx=10, pady=10)
        db_box.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        db_box.grid_rowconfigure(1, weight=1)
        db_box.grid_columnconfigure(0, weight=1)
        db_box.grid_columnconfigure(1, weight=2)
        
        # Top Frame (Title and Back Button)
        top_frame = tk.Frame(db_box, bg=CONTENT_BG)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        tk.Label(top_frame, text="Patient Database", font=FONT_LARGE_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(side="left", padx=10)
        
        back_button = tk.Button(top_frame, text="← Back", font=FONT_SMALL,
                                  bg=MUTED_COLOR, fg=TEXT_COLOR, 
                                  command=self.reset_and_show_welcome, 
                                  relief="flat", padx=10, pady=5)
        back_button.pack(side="right", padx=10)

        # Left Frame (Patient List)
        left_frame = tk.Frame(db_box, bg=CONTENT_BG)
        left_frame.grid(row=1, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(left_frame, text="All Patients", font=FONT_REGULAR_BOLD, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=5)
        
        tree_frame_left = tk.Frame(left_frame)
        tree_frame_left.grid(row=1, column=0, sticky="nsew")
        tree_frame_left.grid_rowconfigure(0, weight=1)
        tree_frame_left.grid_columnconfigure(0, weight=1)

        # Style the Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=CONTENT_BG,
                        foreground=TEXT_COLOR,
                        rowheight=25,
                        fieldbackground=CONTENT_BG,
                        font=(FONT_NAME, 10))
        style.configure("Treeview.Heading", font=(FONT_NAME, 12, 'bold'))
        style.map('Treeview', background=[('selected', PRIMARY_BLUE)])

        cols_left = ("pid", "name", "sex", "age")
        self.patient_list_tree = ttk.Treeview(tree_frame_left, columns=cols_left, show="headings")
        
        self.patient_list_tree.heading("pid", text="Patient ID")
        self.patient_list_tree.column("pid", width=80, anchor="w")
        self.patient_list_tree.heading("name", text="Name")
        self.patient_list_tree.column("name", width=150, anchor="w")
        self.patient_list_tree.heading("sex", text="Sex")
        self.patient_list_tree.column("sex", width=50, anchor="w")
        self.patient_list_tree.heading("age", text="Age")
        self.patient_list_tree.column("age", width=40, anchor="w")
        
        self.patient_list_tree.grid(row=0, column=0, sticky="nsew")
        
        scrollbar_left = ttk.Scrollbar(tree_frame_left, orient="vertical", 
                                       command=self.patient_list_tree.yview)
        self.patient_list_tree.configure(yscrollcommand=scrollbar_left.set)
        scrollbar_left.grid(row=0, column=1, sticky="ns")
        
        self.patient_list_tree.bind("<<TreeviewSelect>>", self.on_patient_select)

        # Right Frame (Vitals History)
        right_frame = tk.Frame(db_box, bg=CONTENT_BG)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        self.db_details_label = tk.Label(right_frame, text="Select a patient...", 
                                         font=FONT_REGULAR_BOLD, bg=CONTENT_BG, 
                                         fg=TEXT_COLOR, wraplength=500, justify="left")
        self.db_details_label.grid(row=0, column=0, sticky="w", pady=5)
        
        tree_frame_right = tk.Frame(right_frame)
        tree_frame_right.grid(row=1, column=0, sticky="nsew")
        tree_frame_right.grid_rowconfigure(0, weight=1)
        tree_frame_right.grid_columnconfigure(0, weight=1)
        
        cols_right = ("timestamp", "hr", "temp", "bp")
        self.vitals_history_tree = ttk.Treeview(tree_frame_right, columns=cols_right, show="headings")
        
        self.vitals_history_tree.heading("timestamp", text="Date & Time")
        self.vitals_history_tree.column("timestamp", width=160, anchor="w")
        self.vitals_history_tree.heading("hr", text="HR (bpm)")
        self.vitals_history_tree.column("hr", width=70, anchor="center")
        self.vitals_history_tree.heading("temp", text="Temp (°C)")
        self.vitals_history_tree.column("temp", width=70, anchor="center")
        self.vitals_history_tree.heading("bp", text="BP (mmHg)")
        self.vitals_history_tree.column("bp", width=100, anchor="center")
        
        self.vitals_history_tree.grid(row=0, column=0, sticky="nsew")
        
        scrollbar_right = ttk.Scrollbar(tree_frame_right, orient="vertical", 
                                        command=self.vitals_history_tree.yview)
        self.vitals_history_tree.configure(yscrollcommand=scrollbar_right.set)
        scrollbar_right.grid(row=0, column=1, sticky="ns")

    # ===================================================================
    # DATABASE VIEW HELPERS
    # ===================================================================

    def _refresh_database_view(self):
        """Populates the main patient list treeview."""
        # Clear both trees
        for row in self.patient_list_tree.get_children():
            self.patient_list_tree.delete(row)
        for row in self.vitals_history_tree.get_children():
            self.vitals_history_tree.delete(row)
            
        self.db_details_label.config(text="Select a patient to view vitals history")
        
        self.all_patients_db = self._load_json_data(DB_FILE, {})
        
        # Populate left tree
        for patient_id, data in self.all_patients_db.items():
            pid = patient_id
            name = data.get("Patient Name", "N/A")
            sex = data.get("Sex", "N/A")
            age = data.get("Computed Age", "N/A")
            self.patient_list_tree.insert("", "end", iid=pid, 
                                          values=(pid, name, sex, age))

    def on_patient_select(self, event):
        """Called when a patient is clicked in the list. Populates the history."""
        try:
            selected_item = self.patient_list_tree.focus()
            if not selected_item:
                return
            
            patient_data = self.all_patients_db.get(selected_item)
            if not patient_data:
                return

            name = patient_data.get("Patient Name", "N/A")
            self.db_details_label.config(text=f"History for: {name} (ID: {selected_item})")
            
            # Clear right tree
            for row in self.vitals_history_tree.get_children():
                self.vitals_history_tree.delete(row)
            
            # Populate right tree
            history = patient_data.get("vitals_history", [])
            
            # Insert in reverse order to show newest first
            for entry in reversed(history):
                ts = entry.get("timestamp", "N/A")
                hr = entry.get("hr", "N/A")
                temp = entry.get("temp", "N/A")
                bp = f"{entry.get('systolic', 'N/A')} / {entry.get('diastolic', 'N/A')}"
                self.vitals_history_tree.insert("", "end", values=(ts, hr, temp, bp))
                
        except Exception as e:
            print(f"Error in on_patient_select: {e}")
            self.db_details_label.config(text="Error loading patient history.")


    # ===================================================================
    # LOGIC AND PROCESSING METHODS
    # ===================================================================

    def process_login(self):
        """Validates login, loads patient data, and moves to Vitals."""
        first_name = self.login_first_name_entry.get_value()
        last_name = self.login_last_name_entry.get_value()

        if not first_name:
            self.show_error_popup("Please enter a first name.")
            return
        if not last_name:
            self.show_error_popup("Please enter a last name.")
            return

        full_name = f"{first_name} {last_name}".strip()
        
        self.all_patients_db = self._load_json_data(DB_FILE, {})
        
        found_patients = []
        for patient_data in self.all_patients_db.values():
            if patient_data.get("Patient Name", "").lower() == full_name.lower():
                found_patients.append(patient_data)

        if len(found_patients) == 0:
            self.show_error_popup("Patient not found.")
        
        elif len(found_patients) == 1:
            self._on_tiebreaker_success(found_patients[0])
            
        else:
            self._show_birthdate_tiebreaker(found_patients, self._on_tiebreaker_success)

    def process_patient_info(self):
        """Validates new patient info and moves to Avatar screen."""
        first_name = self.info_first_name_entry.get_value()
        last_name = self.info_last_name_entry.get_value()
        mm = self.mm_entry.get_value()
        dd = self.dd_entry.get_value()
        yyyy = self.yyyy_entry.get_value()

        if not first_name:
            self.show_error_popup("Please enter a first name.")
            return
        if not last_name:
            self.show_error_popup("Please enter a last name.")
            return
        if not (mm and dd and yyyy):
            self.show_error_popup("Please enter a complete birthdate.")
            return

        # Granular Date Validation
        is_valid = True
        error_messages = []

        try:
            mm_val = int(mm)
            if not (1 <= mm_val <= 12):
                is_valid = False
                error_messages.append("Month must be between 01 and 12.")
                self.mm_entry.reset()
        except ValueError:
            is_valid = False
            error_messages.append("Month must be a number.")
            self.mm_entry.reset()
            
        try:
            dd_val = int(dd)
            if not (1 <= dd_val <= 31):
                is_valid = False
                error_messages.append("Day must be between 01 and 31.")
                self.dd_entry.reset()
        except ValueError:
            is_valid = False
            error_messages.append("Day must be a number.")
            self.dd_entry.reset()

        try:
            yyyy_val = int(yyyy)
            if not (2007 <= yyyy_val <= 2025):
                is_valid = False
                error_messages.append("Year must be between 2007 and 2025.")
                self.yyyy_entry.reset()
        except ValueError:
            is_valid = False
            error_messages.append("Year must be a number.")
            self.yyyy_entry.reset()
            
        if not is_valid:
            self.show_error_popup("Invalid birthdate:\n" + "\n".join(error_messages))
            return

        # All info is valid, proceed
        self.patient_id_counter += 1
        new_patient_id = f"{self.patient_id_counter:05d}"
        
        birthdate_str = f"{mm}/{dd}/{yyyy}"
        age = self._calculate_age(birthdate_str)
        sex = self.sex_var.get()
        
        self.session_data = {
            "Patient ID": new_patient_id,
            "Patient Name": f"{first_name} {last_name}".strip(),
            "Birthdate": birthdate_str,
            "Sex": sex,
            "Computed Age": age,
            "selected_head": None,
            "selected_clothes": None,
            "vitals_history": []  # Initialize new history list
        }

        # Reset vitals placeholders
        self.hr_entry.config(validate='none')
        self.hr_entry.reset()
        self.temp_entry.config(validate='none')
        self.temp_entry.reset()
        self.systolic_entry.config(validate='none')
        self.systolic_entry.reset()
        self.diastolic_entry.config(validate='none')
        self.diastolic_entry.reset()

        # Reset avatar selection
        self.avatar_selection = {'head': None, 'clothes': None}
        self._draw_avatar_on_canvas(self.avatar_canvas, None, None, "normal")
        
        if sex == 'Female':
            self.avatar_female_options_frame.tkraise()
        else:
            self.avatar_male_options_frame.tkraise()

        self.show_stage("Avatar")

    def process_avatar_selection(self):
        """Saves avatar choice and moves to Congrats screen."""
        if not self.avatar_selection['head'] or not self.avatar_selection['clothes']:
            self.show_error_popup("Please select a head and clothes.")
            return

        self.session_data['selected_head'] = self.avatar_selection['head']
        self.session_data['selected_clothes'] = self.avatar_selection['clothes']
        
        patient_id = self.session_data.get('Patient ID')
        if not patient_id:
            print("CRITICAL ERROR: No Patient ID in session data.")
            self.show_error_popup("A critical error occurred. No Patient ID.")
            return
            
        patient_name = self.session_data.get('Patient Name', 'N/A')
        
        print(f"Saving new patient: {patient_name} with ID: {patient_id}")
        self.all_patients_db[patient_id] = self.session_data
        self._save_json_data(DB_FILE, self.all_patients_db)
        self._save_json_data(COUNTER_FILE, self.patient_id_counter)
        
        self.show_stage("Congrats")

    def process_vitals(self):
        """
        Validates vitals, saves them to session_data AND history,
        saves to file, refreshes the status screen, and navigates to it.
        """
        # --- NEW VALIDATION BLOCK ---
        # Get all values from the PlaceholderEntry widgets
        hr_val = self.hr_entry.get_value()
        temp_val = self.temp_entry.get_value()
        systolic_val = self.systolic_entry.get_value()
        diastolic_val = self.diastolic_entry.get_value()

        # Create a dictionary of fields to check
        vitals_to_check = {
            "Heart Rate": hr_val,
            "Temperature": temp_val,
            "Systolic BP": systolic_val,
            "Diastolic BP": diastolic_val
        }
        
        # Find any fields that are still empty
        empty_fields = [name for name, value in vitals_to_check.items() if not value]
        
        if empty_fields:
            # If any fields are empty, show a specific error and stop
            error_message = "Please fill in all vitals fields:\n- " + "\n- ".join(empty_fields)
            self.show_error_popup(error_message)
            return  # Stop the function here
        # --- END OF NEW VALIDATION BLOCK ---

        # Validation passed, proceed with processing...
        patient_id = self.session_data.get("Patient ID")
        if not patient_id:
            print("CRITICAL ERROR: No Patient ID in session during vitals processing.")
            self.show_error_popup("Critical Error: No patient in session. Returning to Welcome.")
            self.reset_and_show_welcome()
            return
            
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # This dict is for the *current* status display
        latest_vitals = {
            "hr": hr_val,
            "temp": temp_val,
            "systolic": systolic_val,
            "diastolic": diastolic_val
        }
        
        # This dict is for the *historical* record
        historical_entry = {
            "timestamp": timestamp,
            "hr": hr_val,
            "temp": temp_val,
            "systolic": systolic_val,
            "diastolic": diastolic_val
        }

        # 1. Update session_data for the status screen
        self.session_data["vitals"] = latest_vitals
        
        # 2. Update session_data with the new historical entry
        if "vitals_history" not in self.session_data:
            self.session_data["vitals_history"] = []
        self.session_data["vitals_history"].append(historical_entry)
        
        # 3. Update the master in-memory DB
        self.all_patients_db[patient_id] = self.session_data
        
        # 4. Save the updated DB to the file
        self._save_json_data(DB_FILE, self.all_patients_db)

        # 5. Refresh and show the status screen
        self._refresh_status_screen()
        self.show_stage("Status")

    def _on_tiebreaker_success(self, patient_data):
        """Callback for successful tiebreaker login."""
        self.session_data = patient_data
        
        # Reset vitals placeholders
        self.hr_entry.config(validate='none')
        self.hr_entry.reset()
        self.temp_entry.config(validate='none')
        self.temp_entry.reset()
        self.systolic_entry.config(validate='none')
        self.systolic_entry.reset()
        self.diastolic_entry.config(validate='none')
        self.diastolic_entry.reset()
        
        self.show_stage("Vitals")

    # ===================================================================
    # DYNAMIC UI UPDATE METHODS
    # ===================================================================

    def select_head(self, head_name, gender_key):
        """Callback for head selection button."""
        self.avatar_selection['head'] = head_name
        self._update_avatar_preview()
        
        # Update button visuals
        for btn in self.head_buttons[gender_key].values():
            btn.config(relief="flat", bg=CONTENT_BG, bd=0)  # Deselect all
        
        selected_btn = self.head_buttons[gender_key].get(head_name)
        if selected_btn:
            selected_btn.config(relief="solid", bg=ACCENT_PINK, bd=3)

    def select_clothes(self, clothes_name, gender_key):
        """Callback for clothes selection button."""
        self.avatar_selection['clothes'] = clothes_name
        self._update_avatar_preview()
        
        # Update button visuals
        for btn in self.clothes_buttons[gender_key].values():
            btn.config(relief="flat", bg=CONTENT_BG, bd=0)  # Deselect all
            
        selected_btn = self.clothes_buttons[gender_key].get(clothes_name)
        if selected_btn:
            selected_btn.config(relief="solid", bg=ACCENT_PINK, bd=3)

    def _update_avatar_preview(self):
        """Updates the canvas on the Avatar screen."""
        self._draw_avatar_on_canvas(
            self.avatar_canvas, 
            self.avatar_selection['head'], 
            self.avatar_selection['clothes'], 
            expression_state="normal" 
        )

    def _get_vitals_status(self):
        """
        Determines the status string, color, and message from session data.
        Returns: (expression_state, status, status_color, message)
        """
        vitals = self.session_data.get("vitals", {})
        hr_val = vitals.get("hr", "")
        temp_val = vitals.get("temp", "")
        systolic_val = vitals.get("systolic", "")
        diastolic_val = vitals.get("diastolic", "")

        status = "Invalid Input"
        status_color = WARNING_COLOR
        expression_state = "sad"
        message = "Invalid data entered."
        abnormal_count = 0
        abnormal_messages = []
        
        try:
            # Convert all vitals first
            hr = int(hr_val)
            temp = float(temp_val)
            systolic = int(systolic_val)
            diastolic = int(diastolic_val)
            
            # Check Heart Rate
            if not (60 <= hr <= 100):
                abnormal_count += 1
                abnormal_messages.append(f"Heart Rate of {hr} bpm is outside the normal range (60-100 bpm).")
                
            # Check Temperature
            if not (36.5 <= temp <= 37.5):
                abnormal_count += 1
                abnormal_messages.append(f"Temperature of {temp} °C is outside the normal range (36.5-37.5 °C).")
                
            # Check Blood Pressure (Systolic)
            if not (100 <= systolic <= 120):
                abnormal_count += 1
                abnormal_messages.append(f"Systolic BP of {systolic} mmHg is outside the normal range (100-120 mmHg).") 

            # Check Blood Pressure (Diastolic)
            if not (60 <= diastolic <= 80):
                abnormal_count += 1
                abnormal_messages.append(f"Diastolic BP of {diastolic} mmHg is outside the normal range (60-80 mmHg).")

            # Determine status
            if abnormal_count == 0:
                status = "Healthy"
                status_color = HEALTHY_COLOR
                expression_state = "normal"
                message = "All vitals are in the normal range. Great job!"
            elif abnormal_count == 1:
                status = "Needs Attention"
                status_color = WARNING_COLOR
                expression_state = "sad"
                message = "\n".join(abnormal_messages)
            else:  # 2 or more
                status = "Needs Urgent Attention"
                status_color = ERROR_COLOR
                expression_state = "sick"
                message = "\n".join(abnormal_messages)

        except (ValueError, KeyError, TypeError):
            # This handles cases where vals are "" or invalid
            pass
        
        return expression_state, status, status_color, message

    def _refresh_status_screen(self):
        """
        Pulls all data from self.session_data and updates the
        labels and canvas on the Status screen.
        """
        if not self.session_data:
            print("Warning: _refresh_status_screen called with no session data.")
            return

        info = self.session_data
        
        name = info.get('Patient Name', 'N/A')
        age = info.get('Computed Age', 'N/A')
        sex = info.get('Sex', 'N/A')
        pid = info.get('Patient ID', 'N/A')
        
        head = info.get('selected_head')
        clothes = info.get('selected_clothes')

        expression_state, status, status_color, message = self._get_vitals_status()
        self.calib_status_expression = expression_state

        # Update Labels
        self.status_name_label.config(text=f"Name: {name}")
        self.status_age_label.config(text=f"Age: {age}")
        self.status_sex_label.config(text=f"Sex: {sex}")
        self.status_id_label.config(text=f"Patient ID: {pid}")
        
        self.status_vitals_label.config(text=f"Status: {status}", fg=status_color)
        self.status_message_label.config(text=message, fg=status_color if status != "Healthy" else PRIMARY_BLUE)

        # Update Avatar
        self._draw_avatar_on_canvas(self.status_canvas, head, clothes, expression_state)

    # ===================================================================
    # AVATAR DRAWING
    # ===================================================================

    def _get_avatar_part_config(self, part_type, part_name, expression_state):
        """
        Gets the PIL image, position, and scale for an avatar part.
        Returns: (pil_image, pos_dict, scale_float)
        """
        sex = self.session_data.get("Sex", "Male")
        
        # 1. Get Base Image, Position, and Scale
        if part_type == 'head':
            if sex == 'Female':
                img_dict = self.head_images_female
                sad_img_dict = self.sad_head_images_female
                sick_img_dict = self.sick_head_images_female
            else:
                img_dict = self.head_images
                sad_img_dict = self.sad_head_images
                sick_img_dict = self.sick_head_images

            # Select image
            base_img = img_dict.get(part_name)  # Default to normal
            if expression_state == "sad" and part_name in sad_img_dict:
                base_img = sad_img_dict[part_name]
            elif expression_state == "sick" and part_name in sick_img_dict:
                base_img = sick_img_dict[part_name]
                
            # Select settings
            base_pos = DEFAULT_HEAD_POS.copy()
            base_scale = DEFAULT_HEAD_SCALE
            
            if expression_state == "normal":
                if part_name in SPECIAL_HEAD_SETTINGS:
                    settings = SPECIAL_HEAD_SETTINGS[part_name]
                    base_pos = {"x": settings["x"], "y": settings["y"]}
                    base_scale = settings["scale"]
            
            elif expression_state == "sad":
                settings = DEFAULT_SAD_HEAD_SETTINGS
                if part_name in SPECIAL_SAD_HEAD_SETTINGS:
                    settings = SPECIAL_SAD_HEAD_SETTINGS[part_name]
                elif part_name in SPECIAL_HEAD_SETTINGS:
                    settings = SPECIAL_HEAD_SETTINGS[part_name]
                base_pos = {"x": settings["x"], "y": settings["y"]}
                base_scale = settings["scale"]

            elif expression_state == "sick":
                settings = DEFAULT_SICK_HEAD_SETTINGS
                if part_name in SPECIAL_SICK_HEAD_SETTINGS:
                    settings = SPECIAL_SICK_HEAD_SETTINGS[part_name]
                elif part_name in SPECIAL_HEAD_SETTINGS:
                    settings = SPECIAL_HEAD_SETTINGS[part_name]
                base_pos = {"x": settings["x"], "y": settings["y"]}
                base_scale = settings["scale"]

        elif part_type == 'clothes':
            clothes_dict = self.clothes_images if sex == "Male" else self.clothes_images_female
            data = clothes_dict.get(part_name)
            if data:
                base_img = data["img"]
                base_pos = {"x": data["x"], "y": data["y"]}
                base_scale = data["scale"]
            else:
                base_img, base_pos, base_scale = None, {"x": 0, "y": 0}, 1.0
        
        else:
             base_img, base_pos, base_scale = None, {"x": 0, "y": 0}, 1.0

        # 2. Apply Calibration Override if Active
        if self.calib_mode:
            current_calib_settings = self.calib_settings.get(part_type)
            if current_calib_settings:
                if self.current_stage == "Avatar":
                    base_pos = current_calib_settings['pos']
                    base_scale = current_calib_settings['scale']
                
                elif (self.current_stage == "Status" and 
                      part_type == 'head' and 
                      expression_state == self.calib_status_expression):
                    base_pos = current_calib_settings['pos']
                    base_scale = current_calib_settings['scale']

        return base_img, base_pos, base_scale

    def _draw_avatar_on_canvas(self, canvas, head_name, clothes_name, expression_state="normal"):
        """Master function to draw the avatar on a given canvas."""
        if not canvas or not canvas.winfo_exists():
            return
            
        canvas.delete("all")
        sex = self.session_data.get("Sex", "Male")
        
        self.calib_canvas_ids = {'head': None, 'clothes': None}
        head_tk = None
        clothes_tk = None

        # Draw Head
        if head_name:
            head_img, h_pos, h_scale = self._get_avatar_part_config('head', head_name, expression_state)
            
            if head_img:
                if sex == "Female" or (sex == "Male" and expression_state in ("sad", "sick")):
                    original_w, original_h = head_img.width, head_img.height
                else:
                    original_w, original_h = 315, 427  # Fixed size for 'normal' Males
                
                new_w = max(1, int(original_w * h_scale))
                new_h = max(1, int(original_h * h_scale))
                
                head_img_resized = head_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                head_tk = ImageTk.PhotoImage(head_img_resized)
                
                canvas_id = canvas.create_image(h_pos["x"], h_pos["y"], image=head_tk, anchor="center")
                self.calib_canvas_ids['head'] = canvas_id

        # Draw Clothes
        if clothes_name:
            clothes_img, c_pos, c_scale = self._get_avatar_part_config('clothes', clothes_name, expression_state)

            if clothes_img:
                if sex == "Female":
                    original_w, original_h = clothes_img.width, clothes_img.height
                else:
                    original_w, original_h = 469, 702  # Fixed size for 'normal' Males
                
                new_w = max(1, int(original_w * c_scale))
                new_h = max(1, int(original_h * c_scale))

                clothes_img_resized = clothes_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                clothes_tk = ImageTk.PhotoImage(clothes_img_resized)
                
                canvas_id = canvas.create_image(c_pos["x"], c_pos["y"], image=clothes_tk, anchor="center")
                self.calib_canvas_ids['clothes'] = canvas_id
                
                # Always raise clothes on top
                canvas.tag_raise(canvas_id)

        # Keep Image References
        canvas.head_image_ref = head_tk
        canvas.clothes_image_ref = clothes_tk
        
        if self.calib_mode and self.calib_current_canvas == canvas:
            self._update_calib_display()

    # ===================================================================
    # ASSET AND DATA HELPERS
    # ===================================================================

    def _load_assets(self):
        """Loads all image assets from files."""
        # Load Male Heads
        for i, filename in enumerate(HEAD_FILES, 1):
            head_name = f"Head M{i}" 
            base, ext = os.path.splitext(filename)
            self.head_images[head_name] = self._load_image_asset(filename, 315, 427, 'lightgrey', head_name)
            self.sad_head_images[head_name] = self._load_image_asset(f"{base}_sad{ext}", 315, 427, 'yellow', f"{head_name} Sad")
            self.sick_head_images[head_name] = self._load_image_asset(f"{base}_sick{ext}", 315, 427, 'orangered', f"{head_name} Sick")

        # Load Male Clothes
        for name, data in CLOTHES_DATA.items():
            img = self._load_image_asset(data["file"], 469, 702, 'lightblue', name)
            self.clothes_images[name] = data.copy()
            self.clothes_images[name]["img"] = img

        # Load Female Heads
        for i, filename in enumerate(HEAD_FILES_FEMALE, 1):
            head_name = f"Head F{i}" 
            base, ext = os.path.splitext(filename)
            self.head_images_female[head_name] = self._load_image_asset(filename, 315, 427, 'lightpink', head_name)
            self.sad_head_images_female[head_name] = self._load_image_asset(f"{base}_sad{ext}", 315, 427, 'yellow', f"{head_name} Sad")
            self.sick_head_images_female[head_name] = self._load_image_asset(f"{base}_sick{ext}", 315, 427, 'orangered', f"{head_name} Sick")

        # Load Female Clothes
        for name, data in CLOTHES_DATA_FEMALE.items():
            img = self._load_image_asset(data["file"], 469, 702, 'pink', name)
            self.clothes_images_female[name] = data.copy()
            self.clothes_images_female[name]["img"] = img

    def _load_image_asset(self, filename, default_w, default_h, color, text):
        """Helper to load a single image or create a placeholder."""
        filepath = os.path.join(ASSETS_DIR, filename)
        try:
            return Image.open(filepath)
        except (FileNotFoundError, IOError):
            print(f"Warning: '{filepath}' not found. Creating placeholder.")
            return Image.new('RGB', (default_w, default_h), color)

    def _load_json_data(self, filepath, default=None):
        """Robustly loads data from a JSON file."""
        if not os.path.exists(filepath):
            return default
        try:
            with open(filepath, "r") as f:
                content = f.read()
                if not content:
                    return default
                return json.loads(content)
        except (json.JSONDecodeError, IOError):
            print(f"Warning: Could not read or decode {filepath}. Returning default.")
            return default

    def _save_json_data(self, filepath, data):
        """Robustly saves data to a JSON file."""
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error: Could not save data to {filepath}. {e}")
            self.show_error_popup(f"Error saving data:\n{e}")
        except TypeError as e:
            print(f"Error: Data is not serializable for {filepath}. {e}")
            self.show_error_popup(f"Error serializing data:\n{e}")

    def _calculate_age(self, birthdate_str):
        """Calculates age from a MM/DD/YYYY string."""
        try:
            birth_date = datetime.strptime(birthdate_str, "%m/%d/%Y").date()
            today = datetime.today().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except (ValueError, IndexError):
            print(f"Invalid date format: {birthdate_str}")
            return "Invalid Date"
            
    def _load_background_images(self):
        """Loads and resizes all stage background images to fit the window."""
        self.update_idletasks() 
        w = self.winfo_width()
        h = self.winfo_height()
        
        if w < 1 or h < 1:
            print("Window not sized, retrying background load...")
            self.after(100, self._load_background_images)
            return
            
        stage_names = ("Welcome", "Login", "PatientInfo", "Avatar", 
                       "Congrats", "Vitals", "Status", "DatabaseView")
        
        print(f"Loading backgrounds for window size: {w}x{h}")

        for name in stage_names:
            filename = f"{name}_bg.png"
            filepath = os.path.join(ASSETS_DIR, filename)
            
            try:
                img_pil = Image.open(filepath)
                img_pil_resized = img_pil.resize((w, h), Image.Resampling.LANCZOS)
                self.background_images_pil[name] = img_pil_resized
                self.background_image_refs[name] = ImageTk.PhotoImage(img_pil_resized)
                print(f"Successfully loaded {filename}")

            except Exception as e:
                print(f"Error loading {filename}: {e}")
                # Create a placeholder
                img_pil_placeholder = Image.new('RGB', (w, h), (240, 248, 255))
                self.background_image_refs[name] = ImageTk.PhotoImage(img_pil_placeholder)
                
        # Set the background for the current stage
        self.show_stage(self.current_stage)

    # ===================================================================
    # FORM WIDGET HELPERS (Validation, Popups)
    # ===================================================================

    # --- ADDED: Mouse wheel recursive binding helper ---
    def _bind_mouse_wheel_recursively(self, widget, func):
        """Binds mouse wheel events recursively to a widget and all its children."""
        widget.bind("<MouseWheel>", func)
        widget.bind("<Button-4>", func)
        widget.bind("<Button-5>", func)
        for child in widget.winfo_children():
            self._bind_mouse_wheel_recursively(child, func)

    def handle_date_key_release(self, event, next_widget, max_len):
        """Handles key input, filtering, and auto-tabbing for date fields."""
        entry = event.widget
        if event.keysym in ("BackSpace", "Delete", "Tab", "Shift_L", 
                            "Shift_R", "Control_L", "Control_R"):
            return

        current_text = entry.get()
        filtered_text = "".join(filter(str.isdigit, current_text))[:max_len]
        
        if current_text != filtered_text:
            cursor_pos = entry.index(tk.INSERT)
            entry.delete(0, tk.END)
            entry.insert(0, filtered_text)
            entry.icursor(cursor_pos)

        if next_widget and len(entry.get()) == max_len and not entry.is_placeholder:
             entry.config(fg=TEXT_COLOR)
             next_widget.focus_set()
        elif not next_widget and len(entry.get()) == max_len and not entry.is_placeholder:
             entry.config(fg=TEXT_COLOR)

    def validate_month_entry(self, event):
        """Live validates the month entry on FocusOut."""
        entry = self.mm_entry
        val = entry.get_value()
        if val:
            try:
                if not (1 <= int(val) <= 12):
                    entry.reset()
            except ValueError:
                entry.reset()

    def validate_day_entry(self, event):
        """Live validates the day entry on FocusOut."""
        entry = self.dd_entry
        val = entry.get_value()
        if val:
            try:
                if not (1 <= int(val) <= 31):
                    entry.reset()
            except ValueError:
                entry.reset()

    def validate_year_entry(self, event):
        """Live validates the year entry on FocusOut."""
        entry = self.yyyy_entry
        val = entry.get_value()
        if val:
            try:
                if not (2007 <= int(val) <= 2025):
                    entry.reset()
            except ValueError:
                entry.reset()

    def on_vitals_focus_in(self, event, vcmd):
        """Applies validation when a vitals entry is focused."""
        entry = event.widget
        entry.config(validate='key', validatecommand=vcmd)

    def on_vitals_focus_out(self, event):
        """Removes validation and re-triggers placeholder if it failed."""
        entry = event.widget
        entry.config(validate='none')
        if not entry.get():
            try:
                entry.set_placeholder()
            except AttributeError:
                pass  # Should be a PlaceholderEntry

    def validate_vitals_numeric(self, P, max_len):
        """Validation command for numeric-only fields."""
        if P == "" or (P.isdigit() and len(P) <= int(max_len)):
            try:
                if P and int(P) > 300:
                    return False
                return True
            except ValueError:
                return False
        return False

    def validate_vitals_alpha_space(self, P):
        """Validation command for alpha + space fields."""
        return all(c.isalpha() or c.isspace() for c in P)

    def validate_vitals_decimal(self, P, max_len):
        """Validation command for decimal fields (like temperature)."""
        if P == "": 
            return True
        if P.count('.') > 1: 
            return False
        if len(P) > int(max_len): 
            return False
        if all(c in "0123456789." for c in P):
            try:
                val_str = P
                if P == ".": 
                    return True
                if P.endswith('.') and P.count('.') == 1:
                    val_str = P[:-1]
                if val_str and float(val_str) > 45.0:
                    return False
                return True
            except ValueError:
                return False
        return False

    def show_error_popup(self, message):
        """Displays a modal error popup."""
        popup = tk.Toplevel(self)
        popup.title("Input Error")
        
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 175
        y = self.winfo_y() + (self.winfo_height() // 2) - 75
        popup.geometry(f'350x150+{x}+{y}')
        popup.configure(bg=CONTENT_BG)
        
        tk.Label(popup, text=message, font=FONT_SMALL, bg=CONTENT_BG, 
                 fg=ERROR_COLOR, wraplength=330).pack(pady=20, padx=10, 
                                                      fill="both", expand=True)
        tk.Button(popup, text="OK", font=FONT_SMALL, command=popup.destroy, 
                  relief="flat", bg=PRIMARY_BLUE, fg=CONTENT_BG, 
                  width=10).pack(pady=10)
        
        popup.transient(self)
        popup.grab_set()
        self.wait_window(popup)

    def _show_birthdate_tiebreaker(self, matches, callback):
        """Shows a popup to select a patient by birthdate."""
        popup = tk.Toplevel(self)
        popup.title("Multiple Patients Found")
        
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 125
        popup.geometry(f'400x250+{x}+{y}')
        popup.configure(bg=CONTENT_BG)
        
        tk.Label(popup, text="Multiple patients found.", font=FONT_REGULAR, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=10)
        tk.Label(popup, text="Enter birthdate to confirm.", font=FONT_SMALL, 
                 bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=5)

        birthdate_frame = tk.Frame(popup, bg=CONTENT_BG)
        birthdate_frame.pack(pady=10)

        mm_entry = PlaceholderEntry(birthdate_frame, "MM", font=FONT_REGULAR, width=3, justify='center')
        dd_entry = PlaceholderEntry(birthdate_frame, "DD", font=FONT_REGULAR, width=3, justify='center')
        yyyy_entry = PlaceholderEntry(birthdate_frame, "YYYY", font=FONT_REGULAR, width=5, justify='center')
        
        mm_entry.pack(side="left")
        tk.Label(birthdate_frame, text="/", font=FONT_REGULAR, bg=CONTENT_BG, fg=TEXT_COLOR).pack(side="left")
        dd_entry.pack(side="left")
        tk.Label(birthdate_frame, text="/", font=FONT_REGULAR, bg=CONTENT_BG, fg=TEXT_COLOR).pack(side="left")
        yyyy_entry.pack(side="left")

        mm_entry.bind("<KeyRelease>", lambda e: self.handle_date_key_release(e, dd_entry, 2))
        dd_entry.bind("<KeyRelease>", lambda e: self.handle_date_key_release(e, yyyy_entry, 2))
        yyyy_entry.bind("<KeyRelease>", lambda e: self.handle_date_key_release(e, None, 4))
        
        error_label = tk.Label(popup, text="", font=FONT_SMALL, bg=CONTENT_BG, fg=ERROR_COLOR)
        error_label.pack(pady=5)

        def _check_login():
            birthdate_str = f"{mm_entry.get_value()}/{dd_entry.get_value()}/{yyyy_entry.get_value()}"
            if not (mm_entry.get_value() and dd_entry.get_value() and yyyy_entry.get_value()):
                error_label.config(text="Please enter a full birthdate.")
                return

            for patient in matches:
                if patient.get("Birthdate") == birthdate_str:
                    callback(patient)  # Run the success function
                    popup.destroy()
                    return
            
            error_label.config(text="Birthdate does not match.")

        tk.Button(popup, text="Login", font=FONT_REGULAR_BOLD, command=_check_login, 
                  bg=PRIMARY_BLUE, fg=CONTENT_BG, relief="flat", padx=20, pady=5).pack(pady=10)
        
        popup.transient(self)
        popup.grab_set()
        self.wait_window(popup)

    # ===================================================================
    # CALIBRATION MODE (F11/F12)
    # ===================================================================

    def toggle_calibration(self, event=None):
        """Toggles the consolidated calibration mode."""
        self.calib_mode = not self.calib_mode
        
        if not self.calib_mode:
            # Deactivating Mode
            print("Calibration Mode OFF")
            if self.calib_current_canvas:
                self.calib_current_canvas.unbind("<ButtonPress-1>")
                self.calib_current_canvas.unbind("<B1-Motion>")
                self.calib_current_canvas.unbind("<ButtonRelease-1>")
                self.calib_current_canvas.unbind("<MouseWheel>")
                self.calib_current_canvas.unbind("<Button-4>")
                self.calib_current_canvas.unbind("<Button-5>")
            
            if self.calibration_label: 
                self.calibration_label.place_forget()
            if self.calibration_label_status: 
                self.calibration_label_status.place_forget()
            
            self.calib_current_canvas = None
            self.calib_drag_data["item_tag"] = None
            return

        # Activating Mode
        self.calib_current_canvas = None
        calib_label = None
        
        if self.current_stage == "Avatar":
            self.calib_current_canvas = self.avatar_canvas
            calib_label = self.calibration_label
            print("Avatar Calibration Mode (F12) ON")
            
        elif self.current_stage == "Status":
            expression = self._get_vitals_status()[0]
            if expression == "normal":
                print("F11 Calibration only available for 'sad' or 'sick' states.")
                self.calib_mode = False  # Abort activation
                return
            
            self.calib_current_canvas = self.status_canvas
            self.calib_status_expression = expression
            calib_label = self.calibration_label_status
            print(f"Status Calibration Mode (F11) ON. Calibrating: {expression}")

        else:
            print("Calibration only available on Avatar or Status screens.")
            self.calib_mode = False  # Abort activation
            return
            
        self._load_calib_settings()

        # Bind events
        self.calib_current_canvas.bind("<ButtonPress-1>", self.on_calib_drag_start)
        self.calib_current_canvas.bind("<B1-Motion>", self.on_calib_drag_motion)
        self.calib_current_canvas.bind("<ButtonRelease-1>", self.on_calib_drag_stop)
        self.calib_current_canvas.bind("<MouseWheel>", self.on_calib_scale)
        self.calib_current_canvas.bind("<Button-4>", self.on_calib_scale)
        self.calib_current_canvas.bind("<Button-5>", self.on_calib_scale)
        
        if calib_label:
            calib_label.place(x=10, y=10, anchor="nw")
            
        self._redraw_active_canvas()

    def _load_calib_settings(self):
        """Loads current avatar/status settings into self.calib_settings."""
        sex = self.session_data.get("Sex", "Male")
        
        if self.current_stage == "Avatar":
            # Load Head Settings
            head_name = self.avatar_selection.get('head')
            settings = DEFAULT_HEAD_POS
            scale = DEFAULT_HEAD_SCALE
            if head_name and head_name in SPECIAL_HEAD_SETTINGS:
                settings = SPECIAL_HEAD_SETTINGS[head_name]
                scale = settings.get("scale", DEFAULT_HEAD_SCALE)
            self.calib_settings['head']['pos'] = {"x": settings["x"], "y": settings["y"]}
            self.calib_settings['head']['scale'] = scale
            
            # Load Clothes Settings
            clothes_name = self.avatar_selection.get('clothes')
            clothes_dict = self.clothes_images if sex == "Male" else self.clothes_images_female
            if clothes_name and clothes_name in clothes_dict:
                data = clothes_dict[clothes_name]
                self.calib_settings['clothes']['pos'] = {"x": data["x"], "y": data["y"]}
                self.calib_settings['clothes']['scale'] = data["scale"]
            else:
                self.calib_settings['clothes']['pos'] = {"x": 300, "y": 500}
                self.calib_settings['clothes']['scale'] = 1.0

        elif self.current_stage == "Status":
            # Load Head Settings (Sad or Sick)
            head_name = self.session_data.get('selected_head')
            expression = self.calib_status_expression
            
            if expression == 'sad':
                lookup, fallback, default = SPECIAL_SAD_HEAD_SETTINGS, SPECIAL_HEAD_SETTINGS, DEFAULT_SAD_HEAD_SETTINGS
            else:  # 'sick'
                lookup, fallback, default = SPECIAL_SICK_HEAD_SETTINGS, SPECIAL_HEAD_SETTINGS, DEFAULT_SICK_HEAD_SETTINGS

            settings = default
            if head_name and head_name in lookup:
                settings = lookup[head_name]
            elif head_name and head_name in fallback:
                settings = fallback[head_name]
            
            self.calib_settings['head']['pos'] = {"x": settings["x"], "y": settings["y"]}
            self.calib_settings['head']['scale'] = settings["scale"]
            
            self.calib_settings['clothes']['pos'] = {"x": 0, "y": 0}
            self.calib_settings['clothes']['scale'] = 0.0

    def _redraw_active_canvas(self):
        """Helper to redraw the avatar on the currently active canvas."""
        if self.current_stage == "Avatar":
            self._update_avatar_preview()
        elif self.current_stage == "Status":
            self._refresh_status_screen()

    def on_calib_key_press(self, event, item_tag):
        """Handles '1' (head) and '2' (clothes) key presses."""
        if not self.calib_mode: 
            return
        
        if self.current_stage == "Status" and item_tag == 'clothes':
            self.calib_drag_data["item_tag"] = 'head'
        else:
            self.calib_drag_data["item_tag"] = item_tag
            
        print(f"Active calibration item set to: {self.calib_drag_data['item_tag']}")
        self._update_calib_display()

    def on_calib_drag_start(self, event):
        """Starts dragging a canvas item."""
        item_tag = self.calib_drag_data["item_tag"]
        if not item_tag or not self.calib_canvas_ids.get(item_tag):
            try:
                canvas_id = event.widget.find_closest(event.x, event.y)[0]
            except IndexError:
                return  # Clicked on empty canvas
                
            if canvas_id == self.calib_canvas_ids['head']:
                item_tag = 'head'
            elif canvas_id == self.calib_canvas_ids['clothes'] and self.current_stage == "Avatar":
                item_tag = 'clothes'
            else:
                return
            self.calib_drag_data["item_tag"] = item_tag

        self.calib_drag_data["x"] = event.x
        self.calib_drag_data["y"] = event.y

    def on_calib_drag_motion(self, event):
        """Moves the selected canvas item."""
        item_tag = self.calib_drag_data["item_tag"]
        if not item_tag or not self.calib_current_canvas:
            return

        dx = event.x - self.calib_drag_data["x"]
        dy = event.y - self.calib_drag_data["y"]
        
        canvas_id = self.calib_canvas_ids.get(item_tag)
        if canvas_id:
            self.calib_current_canvas.move(canvas_id, dx, dy)
            self.calib_drag_data["x"] = event.x
            self.calib_drag_data["y"] = event.y
            
            try:
                new_coords = self.calib_current_canvas.coords(canvas_id)
                self.calib_settings[item_tag]["pos"]["x"] = new_coords[0]
                self.calib_settings[item_tag]["pos"]["y"] = new_coords[1]
            except (tk.TclError, IndexError):
                pass
            
            self._update_calib_display()

    def on_calib_drag_stop(self, event):
        """Updates display on drag release."""
        self._update_calib_display() 

    def on_calib_scale(self, event):
        """Handles MouseWheel scaling."""
        item_tag = self.calib_drag_data["item_tag"]
        if not item_tag: 
            return
        
        # Determine scroll direction
        delta = 0
        if event.num in (4, 5): # Linux
             delta = 120 if event.num == 4 else -120
        else: # Windows/macOS
             delta = event.delta
        
        scale_factor = 1.02 if delta > 0 else 0.98
        self.calib_settings[item_tag]["scale"] *= scale_factor
        
        self._redraw_active_canvas()
        return "break"

    def on_calib_key_scale(self, direction):
        """Handles Up/Down arrow key scaling."""
        if not self.calib_mode: 
            return
        
        item_tag = self.calib_drag_data["item_tag"]
        if not item_tag:
            print("Select an item to scale (1 for head, 2 for clothes)")
            return
        
        scale_factor = 1.02 if direction == "Up" else 0.98
        self.calib_settings[item_tag]["scale"] *= scale_factor
        
        self._redraw_active_canvas()

    def _update_calib_display(self):
        """Updates the calibration info label."""
        if not self.calib_mode:
            if self.calibration_label: 
                self.calibration_label.config(text="")
            if self.calibration_label_status: 
                self.calibration_label_status.config(text="")
            return

        active_item = self.calib_drag_data.get("item_tag", "None")
        
        if self.current_stage == "Avatar":
            label = self.calibration_label
            text = "--- AVATAR CALIB ON (F12) ---\n"
            text += f"ACTIVE: {active_item.upper()} (1/2)\n"
            text += "--- ARROWS TO SCALE ---\n"
            text += f"HEAD:({self.calib_settings['head']['pos']['x']:.1f}, {self.calib_settings['head']['pos']['y']:.1f})\n"
            text += f"SCALE: {self.calib_settings['head']['scale']:.3f}\n"
            text += f"CLOTHES:({self.calib_settings['clothes']['pos']['x']:.1f}, {self.calib_settings['clothes']['pos']['y']:.1f})\n"
            text += f"SCALE: {self.calib_settings['clothes']['scale']:.3f}"
            
        elif self.current_stage == "Status":
            label = self.calibration_label_status
            expression = self.calib_status_expression.upper()
            text = f"--- STATUS CALIB ON (F11) ---\n"
            text += f"CALIBRATING: {expression} HEAD\n"
            text += "--- ARROWS TO SCALE ---\n"
            text += f"HEAD:({self.calib_settings['head']['pos']['x']:.1f}, {self.calib_settings['head']['pos']['y']:.1f})\n"
            text += f"SCALE: {self.calib_settings['head']['scale']:.3f}"
        
        else:
            return

        if label:
            label.config(text=text)
        
        print("--- CALIBRATION UPDATE ---")
        print(text)
        print("--------------------------")

if __name__ == "__main__":
    app = VitagotchiApp()
    app.mainloop()