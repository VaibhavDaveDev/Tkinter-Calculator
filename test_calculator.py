import unittest
import tkinter as tk
from tkinter import ttk # Import ttk for style checks
from calculator import Calculator # Assuming Calculator class is in calculator.py
import collections
import os   # For file operations in tests
import json # For creating test settings files

class TestCalculatorMemoryFunctions(unittest.TestCase):
    # This test class is for the *original* single-slot memory system.
    # It has been commented out as the memory system was replaced.
    pass

class TestCalculatorAdvancedFeatures(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        if os.path.exists(Calculator.SETTINGS_FILE):
            os.remove(Calculator.SETTINGS_FILE)
        self.calc = Calculator(self.root)

    def tearDown(self):
        if self.calc.history_window and self.calc.history_window.winfo_exists():
            self.calc.on_close_history_window() # Use the proper close method
        if self.calc.unit_conversion_window and self.calc.unit_conversion_window.winfo_exists():
            self.calc.on_close_uc_window() # Use the proper close method for UC window
        self.root.destroy()
        if os.path.exists(Calculator.SETTINGS_FILE):
            os.remove(Calculator.SETTINGS_FILE)

    def test_history_population_and_recall(self):
        self.calc.expression = "2+3"; self.calc.calculate()
        self.calc.expression = "10-4"; self.calc.calculate()
        self.assertEqual(list(self.calc.history), ["2+3=5", "10-4=6"])

        self.calc.toggle_history_window()
        self.assertIsNotNone(self.calc.history_listbox)
        self.assertEqual(self.calc.history_listbox.size(), 2)

        self.calc.history_listbox.selection_set(0) 
        self.calc.recall_history_item(None) 
        self.assertEqual(self.calc.expression, "5")
        self.assertEqual(self.calc.result_var.get(), "5")

        self.calc.history_listbox.selection_clear(0, tk.END)
        self.calc.history_listbox.selection_set(1)
        self.calc.recall_history_item(None)
        self.assertEqual(self.calc.expression, "6")
        self.assertEqual(self.calc.result_var.get(), "6")
        self.calc.toggle_history_window()

    def test_theme_switching(self):
        self.assertEqual(self.calc.current_theme_name, "Light")
        self.calc.toggle_theme()
        self.assertEqual(self.calc.current_theme_name, "Dark")
        self.calc.toggle_theme()
        self.assertEqual(self.calc.current_theme_name, "Light")

    def test_theme_colors_applied_basic(self):
        self.calc.toggle_theme() # To Dark
        dark_colors = self.calc.themes["Dark"]
        self.assertEqual(self.calc.style.lookup("TFrame", "background"), dark_colors["bg"])
        self.assertEqual(self.calc.style.lookup(self.calc.display_label.cget("style") or "Display.TLabel", "background"), dark_colors["display_bg"])
        self.assertEqual(self.calc.style.lookup("Num.TButton", "background"), dark_colors["button_bg"])

        self.calc.toggle_theme() # Back to Light
        light_colors = self.calc.themes["Light"]
        self.assertEqual(self.calc.style.lookup("TFrame", "background"), light_colors["bg"])
        self.assertEqual(self.calc.style.lookup(self.calc.display_label.cget("style") or "Display.TLabel", "background"), light_colors["display_bg"])
        self.assertEqual(self.calc.style.lookup("Num.TButton", "background"), light_colors["button_bg"])

    def test_save_load_theme_setting(self):
        self.calc.toggle_theme() 
        self.assertEqual(self.calc.current_theme_name, "Dark")
        
        calc2_root = tk.Tk(); calc2_root.withdraw()
        calc2 = Calculator(calc2_root)
        self.assertEqual(calc2.current_theme_name, "Dark")
        calc2_root.destroy()

    def test_load_settings_no_file(self):
        self.assertEqual(self.calc.current_theme_name, "Light")
        self.assertEqual(len(self.calc.history), 0)
        self.assertEqual(self.calc.memory_slots, [0.0] * Calculator.NUM_MEMORY_SLOTS)
        self.assertEqual(self.calc.active_memory_slot_index, 0)

    def test_load_settings_corrupt_json(self):
        with open(Calculator.SETTINGS_FILE, "w") as f: f.write("this is not json")
        new_root = tk.Tk(); new_root.withdraw()
        calc_corrupt = Calculator(new_root)
        self.assertEqual(calc_corrupt.current_theme_name, "Light")
        self.assertEqual(len(calc_corrupt.history), 0)
        self.assertEqual(calc_corrupt.memory_slots, [0.0] * Calculator.NUM_MEMORY_SLOTS)
        new_root.destroy()

    def test_load_settings_missing_keys(self):
        settings_data = {"some_other_key": "value"}
        with open(Calculator.SETTINGS_FILE, "w") as f: json.dump(settings_data, f)
        new_root = tk.Tk(); new_root.withdraw()
        calc_missing_keys = Calculator(new_root)
        self.assertEqual(calc_missing_keys.current_theme_name, "Light")
        self.assertEqual(len(calc_missing_keys.history), 0)
        self.assertEqual(calc_missing_keys.memory_slots, [0.0] * Calculator.NUM_MEMORY_SLOTS)
        new_root.destroy()

    def test_save_load_history(self):
        self.calc.expression = "1+1"; self.calc.calculate()
        self.calc.expression = "2+2"; self.calc.calculate()
        expected_history = ["1+1=2", "2+2=4"]
        self.assertEqual(list(self.calc.history), expected_history)

        calc2_root = tk.Tk(); calc2_root.withdraw()
        calc2 = Calculator(calc2_root)
        self.assertEqual(list(calc2.history), expected_history)
        calc2_root.destroy()

    def test_save_load_empty_history(self):
        self.calc.save_settings() 
        calc2_root = tk.Tk(); calc2_root.withdraw()
        calc2 = Calculator(calc2_root)
        self.assertEqual(len(calc2.history), 0)
        self.assertEqual(calc2.current_theme_name, "Light")
        calc2_root.destroy()

    def test_initial_memory_state(self):
        self.assertEqual(len(self.calc.memory_slots), Calculator.NUM_MEMORY_SLOTS)
        for i in range(Calculator.NUM_MEMORY_SLOTS):
            self.assertEqual(self.calc.memory_slots[i], 0.0)
        self.assertEqual(self.calc.active_memory_slot_index, 0)
        self.assertEqual(self.calc.memory_slot_display_var.get(), "M1")

    def test_ms_mr_mc_mac_per_slot(self):
        self.calc.expression = "10"; self.calc.button_click("MS")
        self.assertEqual(self.calc.memory_slots[0], 10.0)
        self.calc.button_click("MNext") 
        self.calc.expression = "20"; self.calc.button_click("MS")
        self.assertEqual(self.calc.memory_slots[1], 20.0)
        self.calc.button_click("MR"); self.assertEqual(self.calc.expression, "20.0")
        self.calc.button_click("MC"); self.assertEqual(self.calc.memory_slots[1], 0.0)
        self.calc.button_click("MAC")
        self.assertEqual(self.calc.memory_slots, [0.0] * Calculator.NUM_MEMORY_SLOTS)

    def test_m_plus_m_minus_per_slot(self):
        self.calc.expression = "10"; self.calc.button_click("MS")
        self.calc.expression = "5"; self.calc.button_click("M+")
        self.assertEqual(self.calc.memory_slots[0], 15.0)
        self.calc.button_click("MNext") 
        self.calc.expression = "30"; self.calc.button_click("MS")
        self.calc.expression = "7"; self.calc.button_click("M-")
        self.assertEqual(self.calc.memory_slots[1], 23.0)
        self.assertEqual(self.calc.memory_slots[0], 15.0)

    def test_mnext_cycling(self):
        for i in range(Calculator.NUM_MEMORY_SLOTS * 2): 
            expected_index = i % Calculator.NUM_MEMORY_SLOTS
            self.assertEqual(self.calc.active_memory_slot_index, expected_index)
            self.assertEqual(self.calc.memory_slot_display_var.get(), f"M{expected_index + 1}")
            self.calc.button_click("MNext")

    def test_memory_persistence_save_load_slots_and_active_index(self):
        self.calc.memory_slots[0] = 11.0; self.calc.memory_slots[1] = 22.0
        self.calc.active_memory_slot_index = 1; self.calc.memory_slot_display_var.set("M2")
        self.calc.save_settings()

        calc2_root = tk.Tk(); calc2_root.withdraw()
        calc2 = Calculator(calc2_root)
        self.assertEqual(calc2.memory_slots[:2], [11.0, 22.0])
        self.assertEqual(calc2.active_memory_slot_index, 1)
        self.assertEqual(calc2.memory_slot_display_var.get(), "M2")
        calc2_root.destroy()

    def test_length_conversions(self):
        self.calc.toggle_unit_conversion_window()
        self.calc.uc_category_var.set("Length")
        self.calc.uc_from_unit_var.set("Meter (m)"); self.calc.uc_to_unit_var.set("Foot (ft)")
        self.calc.uc_input_var.set("10"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 32.8084, places=4)
        self.calc.toggle_unit_conversion_window()

    def test_unit_conversion_invalid_input(self):
        self.calc.toggle_unit_conversion_window()
        self.calc.uc_category_var.set("Length")
        self.calc.uc_from_unit_var.set("Meter (m)"); self.calc.uc_to_unit_var.set("Foot (ft)")
        self.calc.uc_input_var.set("abc"); self.calc.perform_unit_conversion()
        self.assertEqual(self.calc.uc_result_var.get(), "Invalid input value")
        self.calc.toggle_unit_conversion_window()

    def test_update_unit_menus_logic(self):
        self.calc.toggle_unit_conversion_window()
        length_units = list(self.calc.conversion_factors["Length"].keys())
        self.assertIn(self.calc.uc_from_unit_var.get(), length_units)
        self.assertIn(self.calc.uc_to_unit_var.get(), length_units)
        self.calc.toggle_unit_conversion_window()

    # --- Tests for New Unit Conversion Categories ---
    def test_weight_conversions(self):
        self.calc.toggle_unit_conversion_window()
        self.assertIsNotNone(self.calc.unit_conversion_window, "Unit conversion window should be created.")
        
        self.calc.uc_category_var.set("Weight")
        # Test 1: Kilograms to Grams (1 kg = 1000 g)
        self.calc.uc_from_unit_var.set("Kilogram (kg)")
        self.calc.uc_to_unit_var.set("Gram (g)")
        self.calc.uc_input_var.set("1")
        self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 1000.0, places=4)

        # Test 2: Kilograms to Pounds (1 kg ≈ 2.20462 lb)
        self.calc.uc_from_unit_var.set("Kilogram (kg)")
        self.calc.uc_to_unit_var.set("Pound (lb)")
        self.calc.uc_input_var.set("1")
        self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 2.20462, places=5)

        # Test 3: Pounds to Ounces (1 lb = 16 oz)
        self.calc.uc_from_unit_var.set("Pound (lb)")
        self.calc.uc_to_unit_var.set("Ounce (oz)")
        self.calc.uc_input_var.set("1")
        self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 16.0, places=4)
        
        # Test 4: Grams to Kilograms (1000g = 1kg)
        self.calc.uc_from_unit_var.set("Gram (g)")
        self.calc.uc_to_unit_var.set("Kilogram (kg)")
        self.calc.uc_input_var.set("1000")
        self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 1.0, places=4)

        self.calc.toggle_unit_conversion_window() # Close window

    def test_temperature_conversions(self):
        self.calc.toggle_unit_conversion_window()
        self.assertIsNotNone(self.calc.unit_conversion_window, "Unit conversion window should be created.")

        self.calc.uc_category_var.set("Temperature")

        # Celsius to Fahrenheit (0°C = 32°F; 100°C = 212°F)
        self.calc.uc_from_unit_var.set("Celsius (°C)"); self.calc.uc_to_unit_var.set("Fahrenheit (°F)")
        self.calc.uc_input_var.set("0"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 32.00, places=2)
        self.calc.uc_input_var.set("100"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 212.00, places=2)

        # Fahrenheit to Celsius (32°F = 0°C; 212°F = 100°C)
        self.calc.uc_from_unit_var.set("Fahrenheit (°F)"); self.calc.uc_to_unit_var.set("Celsius (°C)")
        self.calc.uc_input_var.set("32"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 0.00, places=2)
        self.calc.uc_input_var.set("212"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 100.00, places=2)

        # Celsius to Kelvin (0°C = 273.15K)
        self.calc.uc_from_unit_var.set("Celsius (°C)"); self.calc.uc_to_unit_var.set("Kelvin (K)")
        self.calc.uc_input_var.set("0"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 273.15, places=2)

        # Kelvin to Celsius (273.15K = 0°C)
        self.calc.uc_from_unit_var.set("Kelvin (K)"); self.calc.uc_to_unit_var.set("Celsius (°C)")
        self.calc.uc_input_var.set("273.15"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 0.00, places=2)

        # Fahrenheit to Kelvin (32°F -> 273.15K)
        self.calc.uc_from_unit_var.set("Fahrenheit (°F)"); self.calc.uc_to_unit_var.set("Kelvin (K)")
        self.calc.uc_input_var.set("32"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 273.15, places=2)
        
        # Kelvin to Fahrenheit (273.15K -> 32°F)
        self.calc.uc_from_unit_var.set("Kelvin (K)"); self.calc.uc_to_unit_var.set("Fahrenheit (°F)")
        self.calc.uc_input_var.set("273.15"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 32.00, places=2)

        # Same unit conversion (10°C to 10°C)
        self.calc.uc_from_unit_var.set("Celsius (°C)"); self.calc.uc_to_unit_var.set("Celsius (°C)")
        self.calc.uc_input_var.set("10"); self.calc.perform_unit_conversion()
        self.assertAlmostEqual(float(self.calc.uc_result_var.get()), 10.00, places=2)

        self.calc.toggle_unit_conversion_window() # Close window

if __name__ == '__main__':
    unittest.main()
