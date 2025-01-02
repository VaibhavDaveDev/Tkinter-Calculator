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
