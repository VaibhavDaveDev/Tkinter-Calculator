import unittest
import tkinter as tk
from calculator import Calculator

class TestCalculatorMemoryFunctions(unittest.TestCase):

    def setUp(self):
        """Set up for each test: create a Tk root and a Calculator instance."""
        self.root = tk.Tk()
        # Prevent the Tk window from showing up during tests
        # and to avoid issues if mainloop isn't run.
        self.root.withdraw() 
        self.calc = Calculator(self.root)

    def tearDown(self):
        """Clean up after each test."""
        # Destroy the root window to clean up Tkinter resources
        self.root.destroy()

    def test_mc_memory_clear(self):
        # Set an initial memory value
        self.calc.memory = 123.45
        self.calc.button_click("MC")
        self.assertEqual(self.calc.memory, 0.0, "MC should clear memory to 0.0")

    def test_m_plus_memory_add(self):
        # 1. With empty expression and result "0"
        self.calc.button_click("5") # expression = "5", result_var = "5"
        self.calc.button_click("M+") # memory = 5.0, expression = "", result_var = "5"
        self.assertEqual(self.calc.memory, 5.0, "M+ failed with initial '0' state.")
        self.assertEqual(self.calc.expression, "", "M+ should clear expression.")
        self.assertEqual(self.calc.result_var.get(), "5", "M+ should show the added value.")

        # 2. With existing memory (memory is 5.0 from above)
        self.calc.button_click("3") # expression = "3", result_var = "3"
        self.calc.button_click("M+") # memory = 5.0 + 3.0 = 8.0, expression = "", result_var = "3"
        self.assertEqual(self.calc.memory, 8.0, "M+ failed with existing memory.")
        self.assertEqual(self.calc.expression, "", "M+ should clear expression after adding to existing memory.")
        self.assertEqual(self.calc.result_var.get(), "3", "M+ should show the newly added value.")

        # 3. After a calculation (memory is 8.0)
        # Reset expression and memory for this specific sub-test for clarity
        self.calc.memory = 0.0 
        self.calc.clear() # expression = "", result_var = "0"
        self.calc.button_click("2")
        self.calc.button_click("+")
        self.calc.button_click("3")
        self.calc.button_click("=") # expression = "5", result_var = "5"
        self.calc.button_click("M+") # memory = 0.0 + 5.0 = 5.0, expression = "", result_var = "5"
        self.assertEqual(self.calc.memory, 5.0, "M+ failed after a calculation.")
        self.assertEqual(self.calc.expression, "", "M+ should clear expression after calculation.")
        self.assertEqual(self.calc.result_var.get(), "5", "M+ should show the result of calculation that was added.")
        
        # 4. Invalid input (memory is 5.0 from previous step)
        initial_memory_before_error = self.calc.memory # should be 5.0
        self.calc.expression = "abc" # Simulate invalid direct input
        self.calc.result_var.set("abc") # Keep display consistent with expression
        self.calc.button_click("M+")
        self.assertEqual(self.calc.result_var.get(), "Error", "M+ with invalid input should show Error.")
        self.assertEqual(self.calc.expression, "", "M+ with invalid input should clear expression.")
        self.assertEqual(self.calc.memory, initial_memory_before_error, "M+ with invalid input should not change memory.")

    def test_m_minus_memory_subtract(self):
        self.calc.memory = 10.0 # Initial memory for M- tests

        # 1. Simple subtraction
        self.calc.button_click("3") # expression = "3", result_var = "3"
        self.calc.button_click("M-") # memory = 10.0 - 3.0 = 7.0, expression = "", result_var = "3"
        self.assertEqual(self.calc.memory, 7.0, "M- failed for simple subtraction.")
        self.assertEqual(self.calc.expression, "", "M- should clear expression.")
        self.assertEqual(self.calc.result_var.get(), "3", "M- should show the subtracted value.")

        # 2. Subtracting from result of a calculation (memory is 7.0)
        self.calc.clear() # expression = "", result_var = "0"
        self.calc.button_click("5")
        self.calc.button_click("-")
        self.calc.button_click("1")
        self.calc.button_click("=") # expression = "4", result_var = "4"
        self.calc.button_click("M-") # memory = 7.0 - 4.0 = 3.0, expression = "", result_var = "4"
        self.assertEqual(self.calc.memory, 3.0, "M- failed after a calculation.")
        self.assertEqual(self.calc.expression, "", "M- should clear expression after calculation.")
        self.assertEqual(self.calc.result_var.get(), "4", "M- should show the result of calculation that was subtracted.")

        # 3. Invalid input (memory is 3.0)
        initial_memory_before_error = self.calc.memory
        self.calc.expression = "xyz" # Simulate invalid direct input
        self.calc.result_var.set("xyz")
        self.calc.button_click("M-")
        self.assertEqual(self.calc.result_var.get(), "Error", "M- with invalid input should show Error.")
        self.assertEqual(self.calc.expression, "", "M- with invalid input should clear expression.")
        self.assertEqual(self.calc.memory, initial_memory_before_error, "M- with invalid input should not change memory.")

    def test_mr_memory_recall(self):
        self.calc.memory = 123.45
        self.calc.button_click("MR")
        self.assertEqual(self.calc.expression, "123.45", "MR should set expression to memory value.")
        self.assertEqual(self.calc.result_var.get(), "123.45", "MR should display memory value.")
        
        # Test MR when memory is 0
        self.calc.memory = 0.0
        self.calc.button_click("MR")
        self.assertEqual(self.calc.expression, "0.0", "MR should set expression to '0.0' when memory is 0.")
        self.assertEqual(self.calc.result_var.get(), "0.0", "MR should display '0.0' when memory is 0.")


    def test_combined_operations(self):
        # Sequence 1: "5", "M+", "2", "M+", "MR"
        self.calc.button_click("5")
        self.calc.button_click("M+") # memory = 5.0, result = "5"
        self.calc.button_click("2")
        self.calc.button_click("M+") # memory = 5.0 + 2.0 = 7.0, result = "2"
        self.calc.button_click("MR") # expression = "7.0", result = "7.0"
        self.assertEqual(self.calc.expression, "7.0", "Combined M+, M+, MR failed for expression.")
        self.assertEqual(self.calc.result_var.get(), "7.0", "Combined M+, M+, MR failed for display.")
        self.assertEqual(self.calc.memory, 7.0, "Combined M+, M+, MR failed for memory state.")

        # Sequence 2: "1", "0", "M+", "3", "M-", "MR"
        self.calc.clear() # Clear expression and result
        self.calc.memory = 0.0 # Clear memory
        
        self.calc.button_click("1")
        self.calc.button_click("0") # expression = "10"
        self.calc.button_click("M+") # memory = 10.0, result = "10"
        self.assertEqual(self.calc.memory, 10.0)
        self.assertEqual(self.calc.result_var.get(), "10")
        self.assertEqual(self.calc.expression, "")


        self.calc.button_click("3") # expression = "3"
        self.calc.button_click("M-") # memory = 10.0 - 3.0 = 7.0, result = "3"
        self.assertEqual(self.calc.memory, 7.0)
        self.assertEqual(self.calc.result_var.get(), "3")
        self.assertEqual(self.calc.expression, "")

        self.calc.button_click("MR") # expression = "7.0", result = "7.0"
        self.assertEqual(self.calc.expression, "7.0", "Combined M+, M-, MR failed for expression.")
        self.assertEqual(self.calc.result_var.get(), "7.0", "Combined M+, M-, MR failed for display.")
        
        # Sequence 3: "MC", "MR" (memory is 7.0 from above)
        self.calc.button_click("MC") # memory = 0.0
        self.assertEqual(self.calc.memory, 0.0)
        self.calc.button_click("MR") # expression = "0.0", result = "0.0"
        self.assertEqual(self.calc.expression, "0.0", "Combined MC, MR failed for expression.")
        self.assertEqual(self.calc.result_var.get(), "0.0", "Combined MC, MR failed for display.")

if __name__ == '__main__':
    unittest.main()
