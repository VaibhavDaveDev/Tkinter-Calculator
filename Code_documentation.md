# Code Documentation - Tkinter Calculator

This document provides an overview of the codebase for the Tkinter Calculator application.

## Project Structure

- `calculator.py`: Main application script containing the `Calculator` class and UI logic.
- `test_calculator.py`: Unit tests for the calculator functionality.
- `README.md`: General information about the project.
- `Code_documentation.md`: This file.
- `User_manual.md`: User guide for the calculator.
- `calc_settings.json`: (Generated at runtime) Stores user preferences like theme, history, and memory slots.

## Main Class: `Calculator` (in `calculator.py`)

The `Calculator` class is responsible for the application's logic and user interface.

- **`Calculator.SETTINGS_FILE`**: A class attribute (string) defining the name of the JSON file used for storing settings.
- **`Calculator.NUM_MEMORY_SLOTS`**: A class attribute (int) defining the number of memory slots available.

### Initialization (`__init__`)
- Sets up the main window (`self.root`).
- Initializes state variables:
    - `self.expression`, `self.result_var`.
    - Advanced Memory: `self.memory_slots`, `self.active_memory_slot_index`, `self.memory_slot_display_var`, `self.memory_slot_display_label`.
    - `self.degree_mode`, `self.deg_rad_button`.
    - `self.history`, `self.history_window`, `self.history_listbox`.
    - Theming: `self.themes`, `self.current_theme_name`, `self.style`, `self.all_button_widgets`.
    - **Unit Conversion**:
        - `self.unit_conversion_window` (tk.Toplevel or None).
        - `self.conversion_factors` (dict): Stores conversion factors and unit definitions.
          ```python
          self.conversion_factors = {
              "Length": {
                  "Meter (m)": 1.0, "Kilometer (km)": 1000.0, "Mile (mi)": 1609.34,
                  "Foot (ft)": 0.3048, "Inch (in)": 0.0254, "Centimeter (cm)": 0.01,
                  "Millimeter (mm)": 0.001,
              },
              "Weight": {
                  "Kilogram (kg)": 1.0, # Base unit
                  "Gram (g)": 0.001,
                  "Pound (lb)": 0.453592,
                  "Ounce (oz)": 0.0283495,
              },
              "Temperature": { # Factors are placeholders; logic is formula-based
                  "Celsius (°C)": "Celsius",
                  "Fahrenheit (°F)": "Fahrenheit",
                  "Kelvin (K)": "Kelvin",
              }
          }
          ```
        - `self.unit_categories` (list): Populated from `self.conversion_factors.keys()`.
        - `tk.StringVar` instances for UI elements: `self.uc_category_var`, `self.uc_from_unit_var`, `self.uc_to_unit_var`, `self.uc_input_var`, `self.uc_result_var`.
        - Widget references: `self.uc_category_menu`, etc.
- Calls `self.load_settings()`.
- Initializes `self.memory_slot_display_var` text.
- Calls `self.create_widgets()`.
- Calls `self.apply_theme()`.
- Binds keyboard events.

### UI Creation (`create_widgets`)
- Sets up the main display area and memory slot display.
- Creates and lays out all main calculator buttons, including "History", "Theme", memory buttons, scientific functions, "Units" button, etc.
- The "Units" button is configured to call `self.toggle_unit_conversion_window`.
- Stores button widgets in `self.all_button_widgets`.

### Core Logic (`button_click`, `calculate`, `handle_keypress`, etc.)
- ... (other core logic methods) ...

### History Management (...)
### Theme Management
- **`apply_theme(self)`:**
    - ... (main calculator theming) ...
    - Themes the Unit Conversion window and its elements if active.

### Unit Conversion System
- **`self.conversion_factors` Structure**: As detailed in the `__init__` section, this dictionary holds the definitions and conversion factors (or placeholders for formula-based units like Temperature).
- **`toggle_unit_conversion_window(self)`:** Creates or destroys the `Toplevel` window for unit conversion. Sets up UI elements (Labels, OptionMenus, Entry, Button, Result Label).
- **`on_close_uc_window(self)`:** Handles closing of the unit conversion window.
- **`update_unit_menus(self, *args)`:** Dynamically populates "From Unit" and "To Unit" OptionMenus based on the selected category.
- **`perform_unit_conversion(self)`:**
    - Retrieves input value, category, and selected units.
    - Validates input.
    - **Conditional Logic**:
        - **If `category == "Temperature"`**:
            - Applies specific conversion formulas:
                - Celsius to Fahrenheit: `(C * 9/5) + 32`
                - Celsius to Kelvin: `C + 273.15`
                - Fahrenheit to Celsius: `(F - 32) * 5/9`
                - Fahrenheit to Kelvin: `((F - 32) * 5/9) + 273.15`
                - Kelvin to Celsius: `K - 273.15`
                - Kelvin to Fahrenheit: `((K - 273.15) * 9/5) + 32`
            - Handles `from_unit == to_unit` case.
            - Formats result to two decimal places (e.g., `f"{result:.2f}"`).
        - **Else (for "Length", "Weight", and other factor-based categories)**:
            - Retrieves `from_factor` and `to_factor` from `self.conversion_factors[category]`.
            - Converts the input value to the base unit: `value_in_base = value_float * from_factor`.
            - Converts from the base unit to the target unit: `result = value_in_base / to_factor`.
            - Formats result using `f"{result:.5g}"`.
    - Displays the result or an error message in `self.uc_result_var`.

### Settings Management (...)
- **`load_settings(self)`:** Loads theme, history, memory slots, and active memory slot.
- **`save_settings(self)`:** Saves theme, history, memory slots, and active memory slot.
- **`calc_settings.json` File Structure Example:** (Unchanged, as unit conversion settings are not persistent).

## Adding New Operations (...)
## Adding New Unit Conversion Categories
1.  Add a new key to `self.conversion_factors` (e.g., "Area").
2.  If factor-based: Populate its dictionary with unit names as keys and their conversion factor relative to a chosen base unit for that category.
3.  If formula-based: Add placeholder values in `self.conversion_factors` and implement the specific logic in `perform_unit_conversion`.
4.  `self.unit_categories` will be updated dynamically. The `update_unit_menus` method should handle the new units.
