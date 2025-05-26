# User Manual - Tkinter Calculator

Welcome to the Tkinter Calculator! This guide explains how to use its features.

## Basic Operations
- **Number Input:** Click the number buttons (0-9) or use your keyboard's number keys to build an expression.
- **Decimal Point:** Use the "." button or key.
- **Operators:** Click the operator buttons (+, -, *, /) or use the corresponding keyboard keys.
- **Equals (=):** Click the "=" button or press Enter to evaluate the current expression.
- **Clear (C):** Click the "C" button or press Escape to clear the current expression and result.
- **Delete (Del):** Click the "Del" button or press Backspace to remove the last character from the expression.

## Advanced Memory Functions (Multi-Slot)

The calculator features an advanced memory system with 5 persistent memory slots (M1 to M5). The currently active memory slot is shown on the display (e.g., "M1").

- **MNext (Next Memory Slot):** Cycles through the active memory slots (M1 -> M2 -> ... -> M5 -> M1).
- **MS (Memory Store):** Stores the current expression's value (or the displayed result) into the **active memory slot**.
- **MR (Memory Recall):** Recalls the value from the **active memory slot** and places it in the current expression.
- **MC (Memory Clear):** Clears the value in the **active memory slot** to 0.0.
- **M+ (Memory Add):** Adds the current expression's value (or the displayed result) to the value in the **active memory slot**.
- **M- (Memory Subtract):** Subtracts the current expression's value (or the displayed result) from the value in the **active memory slot**.
- **MAC (Memory All Clear):** Clears all 5 memory slots to 0.0 simultaneously.

**Persistence:** The contents of all memory slots and the currently selected active slot are automatically saved and will be available when you next open the calculator.

## Scientific Operations

The calculator supports several scientific functions:

### Angle Mode (Radians/Degrees)
- The **Rad/Deg** button (initially shows "Rad") toggles the angle mode for trigonometric functions.
- When "Rad" is shown, inputs for sin, cos, tan are expected in radians.
- When "Deg" is shown, inputs for sin, cos, tan are expected in degrees.
- The display will briefly show "Mode: Rad" or "Mode: Deg" when toggled.

### Trigonometric Functions
- **sin:** Calculates the sine of the current expression.
- **cos:** Calculates the cosine of the current expression.
- **tan:** Calculates the tangent of the current expression.
  *(Angle mode applies)*

### Logarithmic Functions
- **log:** Calculates the base-10 logarithm of the current expression.
- **ln:** Calculates the natural logarithm (base e) of the current expression.

### Exponential Functions
- **exp:** Calculates e raised to the power of the current expression (e^x).
- **x²:** Calculates the square of the current expression.
- **x³:** Calculates the cube of the current expression.
- **^ (Power):** Raises the current expression (or previous result) to the power of the next number entered. Example: `2 ^ 3 =` results in 8.

### Root Functions
- **√:** Calculates the square root of the current expression.

### Constants
- **π:** Inserts the value of Pi (approx. 3.14159...) into the expression.
- **e:** Inserts the value of Euler's number (approx. 2.71828...) into the expression.

## Unit Conversion
- **Accessing the Converter:** Click the "Units" button on the main calculator to open the Unit Converter window.
- **User Interface:**
    - **Category:** Select the type of unit you want to convert (e.g., "Length", "Weight", "Temperature").
    - **From Unit:** Choose the unit you are converting from using the dropdown menu.
    - **To Unit:** Choose the unit you are converting to using the dropdown menu.
    - **Value:** Enter the numerical value you wish to convert in the input field.
    - **Convert Button:** Click this button to perform the conversion.
    - **Result:** The converted value will be displayed below the "Convert" button.

### Supported Categories and Units:
-   **Length:**
    -   Units: Meter (m), Kilometer (km), Mile (mi), Foot (ft), Inch (in), Centimeter (cm), Millimeter (mm).
    -   Example: Convert 10 Meters to Feet. The result will be approximately 32.8084 ft.
-   **Weight:**
    -   Units: Kilogram (kg), Gram (g), Pound (lb), Ounce (oz).
    -   Example: Convert 5 Kilograms to Pounds. The result will be approximately 11.0231 lb.
-   **Temperature:**
    -   Units: Celsius (°C), Fahrenheit (°F), Kelvin (K).
    -   Conversions are formula-based.
    -   Example: Convert 25 Celsius to Fahrenheit. The result will be 77.00 °F.

## Keyboard Input
- **Numbers 0-9:** Direct input.
- **Operators +, -, *, /, . , ^:** Direct input.
- **Enter:** Equals operation.
- **Backspace:** Delete last character (Del).
- **Escape:** Clear current expression (C).

## Calculation History
- The calculator automatically stores the last 10 successful calculations (e.g., "2+3=5").
- **Viewing History:** Click the "History" button to open a separate window displaying these calculations.
- **Recalling Results:** Double-click an entry in the history window to load its *result* into the main calculator display for further use.
- **Persistence:** Your calculation history is automatically saved and will be available when you next open the calculator.

## Settings and Preferences

### Theme Customization
- You can switch between "Light" and "Dark" visual themes using the "Theme" button.
- **Persistence:** Your chosen theme is automatically saved and will be applied when you next open the calculator.

### Settings File
- Settings (like your preferred theme, calculation history, memory slot contents, and active memory slot) are stored in a file named `calc_settings.json` in the same directory as the calculator application. Modifying this file directly is not recommended.
