import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


def create_database():
    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS bmi_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL)""")

    conn.commit()
    conn.close()


create_database()


def save_bmi_record(name, weight, height, bmi, category):
    conn = None

    try:
        conn = sqlite3.connect("bmi_history.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                name,
                weight,
                height,
                bmi,
                category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        conn.commit()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if conn:
            conn.close()


# Main window
root = tk.Tk()
root.title("BMI Dashboard")
root.state("zoomed")
root.configure(bg="#F1F5F9")

# Header
header = tk.Frame(root, bg="#172554", height=110)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header, text="BMI DASHBOARD", font=("Arial", 23, "bold"), bg="#172554", fg="white"
).pack(pady=(22, 3))

tk.Label(
    header,
    text="Your Personal Health Tracker",
    font=("Arial", 10),
    bg="#172554",
    fg="#BFDBFE",
).pack()

# Main card
card = tk.Frame(root, bg="white", padx=25, pady=20)
card.pack(fill="x", padx=25, pady=20)


def create_input(label_text):
    tk.Label(
        card, text=label_text, font=("Arial", 10, "bold"), bg="white", fg="#334155"
    ).pack(anchor="w", pady=(8, 4))

    entry = tk.Entry(
        card, font=("Arial", 11), bg="#F1F5F9", fg="#0F172A", relief="flat", bd=0
    )
    entry.pack(fill="x", ipady=7)
    return entry


name_entry = create_input("Your Name")
weight_entry = create_input("Weight (KG)")
height_entry = create_input("Height (Meters)")

# Result card
result_lable = tk.Label(
    root,
    text="Enter your details to calculate BMI",
    font=("Arial", 13, "bold"),
    bg="#DBEAFE",
    fg="#1E3A8A",
    padx=15,
    pady=18,
)
result_lable.pack(fill="x", padx=25, pady=5)


def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and height must be positive.")
            return

        bmi = weight / (height**2)

        if bmi < 18.5:
            category = "Underweight"
            color = "Orange"

        elif bmi < 25:
            category = "Normal"
            color = "Green"

        elif bmi < 30:
            category = "Overweight"
            color = "Orange"

        else:
            category = "Obese"
            color = "Red"

        result_lable.config(
            text=f"{name}'s BMI:{bmi:.2f}\nCategory: {category}", fg=color
        )

        save_bmi_record(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")


def view_history():
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter your name first.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("700x450")
    history_window.configure(bg="#F1F5F9")

    tk.Label(
        history_window,
        text=f"{name}'s BMI HISTORY",
        font=("Arial", 18, "bold"),
        bg="#F1F5F9",
        fg="#1E3A8A",
    ).pack(pady=15)

    try:
        with sqlite3.connect("bmi_history.db") as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT weight, height, bmi, category, date
                FROM bmi_records
                WHERE name = ?
                ORDER BY id DESC
            """,
                (name,),
            )

            records = cursor.fetchall()

        if not records:
            tk.Label(
                history_window,
                text="No records found.",
                bg="#F1F5F9",
                font=("Arial", 12),
            ).pack(pady=20)
            return

        for record in records:
            text = (
                f"Weight: {record[0]} kg | "
                f"Height: {record[1]} m | "
                f"BMI: {record[2]:.2f} | "
                f"{record[3]} | {record[4]}"
            )

            tk.Label(
                history_window,
                text=text,
                font=("Arial", 10),
                bg="white",
                fg="#334155",
                padx=10,
                pady=8,
            ).pack(fill="x", padx=15, pady=4)

    except sqlite3.Error as e:
        history_window.destroy()
        messagebox.showerror("Database Error", str(e))


# Button styling
button_style = {
    "font": ("Arial", 11, "bold"),
    "bg": "#2563EB",
    "fg": "white",
    "activebackground": "#1D4ED8",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "cursor": "hand2",
}

# Calculate button
calculate_button = tk.Button(
    root, text="Calculate BMI", command=calculate_bmi, **button_style
)
calculate_button.pack(fill="x", padx=25, pady=8, ipady=9)

# History button
history_button = tk.Button(
    root, text="View BMI History", command=view_history, **button_style
)
history_button.pack(fill="x", padx=25, pady=8, ipady=9)


def show_bmi_graph():
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    try:
        with sqlite3.connect("bmi_history.db") as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT date, bmi
                FROM bmi_records
                WHERE name = ?
                ORDER BY id ASC
            """,
                (name,),
            )

            records = cursor.fetchall()

        if not records:
            messagebox.showinfo("No Data", "No BMI records available.")
            return

        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime

        dates = [
            datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S") for record in records
        ]
        bmi_values = [record[1] for record in records]

        fig, ax = plt.subplots(figsize=(11, 6))

        ax.axhspan(18.5, 24.9, alpha=0.12, label="Normal range")
        ax.axhline(18.5, linestyle="--", alpha=0.5)
        ax.axhline(25, linestyle="--", alpha=0.5)
        ax.axhline(30, linestyle="--", alpha=0.5)

        ax.plot(
            dates,
            bmi_values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label="BMI Trend",
        )

        ax.set_title(f"{name}'s BMI Progress", fontsize=17, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
        fig.autofmt_xdate()

        ax.grid(alpha=0.25)
        ax.legend()
        fig.tight_layout()
        plt.show()

    except (sqlite3.Error, ValueError) as e:
        messagebox.showerror("Error", str(e))


# graph button
graph_button = tk.Button(
    root, text="View BMI Trend Graph", command=show_bmi_graph, **button_style
)
graph_button.pack(fill="x", padx=25, pady=8, ipady=9)
root.mainloop()
