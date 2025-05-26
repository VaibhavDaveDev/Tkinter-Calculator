import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.memory = 0.0
        self.create_widgets()

    def create_widgets(self):
        # Display Screen
        display_frame = ttk.Frame(self.root, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)
        display_label = ttk.Label(display_frame, textvariable=self.result_var, font=("Arial", 30), anchor="e")
        display_label.pack(fill=tk.BOTH, expand=True)

        # Buttons Frame
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        # Button Layout
        buttons = [
            ("MC", 0, 0), ("MR", 0, 1), ("M-", 0, 2), ("M+", 0, 3),
            ("C", 1, 0), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2), ("Del", 5, 3)
        ]

        for (text, row, col) in buttons:
            button = ttk.Button(buttons_frame, text=text, command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            buttons_frame.grid_columnconfigure(col, weight=1)
            buttons_frame.grid_rowconfigure(row, weight=1)

    def button_click(self, text):
        if text == "=":
            self.calculate()
        elif text == "C":
            self.clear()
        elif text == "Del":
            self.delete()
        elif text == "MC":
            self.memory = 0.0
        elif text == "MR":
            self.expression = str(self.memory)
            self.result_var.set(self.expression)
        elif text == "M+" or text == "M-":
            current_value_str = ""
            value_to_operate = None

            if self.expression: # Prioritize active expression
                current_value_str = self.expression
            else: # Otherwise, use the displayed value (e.g., result of a calculation)
                current_value_str = self.result_var.get()
            
            try:
                # If there's an active expression (e.g., "2+3"), eval it.
                # Otherwise, the value in result_var (e.g. "5" from a previous calc) should be a direct float.
                if self.expression: 
                    value_to_operate = eval(current_value_str)
                else:
                    value_to_operate = float(current_value_str)

                if text == "M+":
                    self.memory += value_to_operate
                elif text == "M-":
                    self.memory -= value_to_operate
                
                # Display the value that was actually added/subtracted to/from memory
                self.result_var.set(str(value_to_operate)) 
                self.expression = "" # Clear current expression after memory operation

            except (SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError):
                # These errors can occur from eval() or float()
                self.result_var.set("Error")
                self.expression = ""
            except Exception: # Catch-all for any other unexpected errors
                self.result_var.set("Error")
                self.expression = ""
        else:
            self.expression += text
            self.result_var.set(self.expression)

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.result_var.set(result)
            self.expression = result
        except Exception as e:
            self.result_var.set("Error")
            self.expression = ""

    def delete(self):
        self.expression = self.expression[:-1]
        self.result_var.set(self.expression if self.expression else "0")

    def clear(self):
        self.expression = ""
        self.result_var.set("0")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
