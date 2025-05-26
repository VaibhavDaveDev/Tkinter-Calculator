# Tkinter Calculator Application

An enhanced calculator application built using Python and Tkinter. It supports basic arithmetic, memory functions, and a range of scientific operations, with a user-friendly interface and keyboard support.

## Features

- **Core Arithmetic Operations**: Addition, Subtraction, Multiplication, Division. Supports decimal points and large numbers.
- **Memory Functions**: Advanced multi-slot memory (5 slots) with operations like Store (MS), Recall (MR), Clear (MC), Add (M+), Subtract (M-), Next Slot (MNext), and All Clear (MAC). Active slot and contents are persistent.
- **Scientific Operations**:
    - **Trigonometric Functions**: `sin`, `cos`, `tan` with a toggle for **Degrees/Radians** mode.
    - **Logarithmic Functions**: `log` (base 10) and `ln` (natural log).
    - **Exponential Functions**: `exp` (e^x), `x²` (square), `x³` (cube), `xⁿ` (power, using "^" button).
    - **Root Operations**: `√` (square root).
    - **Mathematical Constants**: Access `π` (Pi) and `e` (Euler's number) via dedicated buttons.
- **Keyboard Input**: Perform calculations using your keyboard for numbers (0-9), operators (+, -, *, /, .), power (^), Enter (=), Backspace (Del), and Escape (C).
- **Calculation History**: Displays the last 10 calculations in a separate window, allowing recall of results. History is **saved and loaded between sessions**.
- **Theming System**: Choose between 'Light' and 'Dark' visual themes. Your preference is saved.
- **Unit Conversion System**: Built-in converter for various units. Currently supports Length (m, km, mi, ft, in, cm, mm), Weight (kg, g, lb, oz), and Temperature (°C, °F, K) conversions.
- **Persistent Settings**: Your preferred theme (Light/Dark), calculation history, and memory slot contents/active slot are automatically saved and restored when you reopen the calculator.
- **Error Handling**: Robust error messages for invalid inputs like division by zero, incorrect syntax, and mathematical domain errors (e.g., log of a negative number).
- **Clear (C) and Delete (Del)**: Standard clear and delete functionalities to manage input.
- **User-Friendly Interface**: A clear and intuitive button layout, including a dynamic display for the current angle mode (Radians/Degrees).

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python; install if missing)
- `collections` module (part of Python's standard library, used for history)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VaibhavDaveDev/Tkinter-Calculator.git 
   ```
2. Navigate to the project directory:
   ```bash
   cd Tkinter-Calculator
   ```

## How to Run
1. Ensure you are in the project directory (`Tkinter-Calculator`).
2. Run the application with:
   ```bash
   python calculator.py
   ```
   The calculator window will appear, ready for use.
## Documentation
- **User Manual**: See `User_manual.md` for detailed usage instructions for all calculator features.
- **Code Documentation**: See `Code_documentation.md` for an overview of the codebase structure and main components.
