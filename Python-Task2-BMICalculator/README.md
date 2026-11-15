BMI Calculator

A Python-based BMI (Body Mass Index) Calculator with a simple command-line version and an advanced Tkinter GUI dashboard.

Features

Basic Version

- Calculates BMI using weight and height.
- Displays BMI category: Underweight, Normal, Overweight, or Obese.
- Handles invalid inputs and non-positive values.

Advanced Version

- User-friendly Tkinter dashboard.
- Calculates BMI and displays the category.
- Saves BMI records using SQLite.
- Displays user-specific BMI history.
- Visualizes BMI progress with a Matplotlib trend graph.
- Validates user inputs.

Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

Project Structure

BMI-Calculator/
├── bmi_calculator.py
├── bmi_calculator_advanced.py
├── bmi_history.db
├── README.md
└── screenshots/

How to Run

1. Install Python.

2. Install Matplotlib:

   pip install matplotlib

3. Run the basic version:

   python bmi_calculator.py

4. Run the advanced version:

   python bmi_calculator_advanced.py

BMI Categories

BMI Range| Category
Below 18.5| Underweight
18.5–24.9| Normal
25–29.9| Overweight
30 or above| Obese

Author

Oasis Infobyte Python Internship Project

Note

This project is developed for educational purposes. BMI categories are general screening guidelines and are not a medical diagnosis.
