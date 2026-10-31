# Required libraries
import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

window = tk.Tk()

window.title("Random Password Generator")
window.geometry("500x650")

title = tk.Label(window, text="Random Password Generator", font=("Arial", 18))

title.pack(pady=20)

length_label = tk.Label(window, text="Password Length:")

length_label.pack()

length_spinbox = tk.Spinbox(window, from_=8, to=50, width=10)

length_spinbox.pack(pady=5)

uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

uppercase_check = tk.Checkbutton(window, text="Uppercase (A-Z)", variable=uppercase_var)

uppercase_check.pack()

lowercase_check = tk.Checkbutton(window, text="Lowercase (a-z)", variable=lowercase_var)

lowercase_check.pack()

numbers_check = tk.Checkbutton(window, text="Numbers (0-9)", variable=numbers_var)

numbers_check.pack()

symbols_check = tk.Checkbutton(window, text="Symbols (!@#$)", variable=symbols_var)

symbols_check.pack()

# Store the last 5 generated passwords during the current session
password_history = []


# Copy the generated password to the clipboard
def copy_password():
    password = password_label.cget("text")
    pyperclip.copy(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")


# Generate a secure password based on the selected criteria
def generate_password():

    # Count the number of selected character types
    select_type = sum(
        [uppercase_var.get(), lowercase_var.get(), numbers_var.get(), symbols_var.get()]
    )

    if select_type < 2:
        messagebox.showwarning(
            "Selection Required", "Please select at least 2 character types."
        )
        return

    length = int(length_spinbox.get())

    if length < 8:
        messagebox.showwarning("Invalid Length", "Password length must be at least 8.")
        return

    # Store the selected character sets
    selected_characters = []

    if uppercase_var.get():
        selected_characters.append(string.ascii_uppercase)

    if lowercase_var.get():
        selected_characters.append(string.ascii_lowercase)

    if numbers_var.get():
        selected_characters.append(string.digits)

    if symbols_var.get():
        selected_characters.append(string.punctuation)

    if exclude_ambiguous_var.get():
        selected_characters = [
            chars.replace("0", "").replace("O", "").replace("l", "").replace("1", "")
            for chars in selected_characters
        ]

    # Guarantee at least one character from each selected type
    password_list = [secrets.choice(chars) for chars in selected_characters]

    for _ in range(length - len(password_list)):
        password_list.append(secrets.choice("".join(selected_characters)))

    secrets.SystemRandom().shuffle(password_list)

    password = "".join(password_list)

    pyperclip.copy(password)

    password_label.config(text=password)

    password_history.append(password)

    if len(password_history) > 5:
        password_history.pop(0)

    history_label.config(text="History:\n" + "\n".join(password_history))

    strength = "Weak"

    if length >= 12 and select_type >= 3:
        strength = "Strong"

    elif length >= 8 and select_type >= 2:
        strength = "Medium"

    strength_label.config(text="Strength: " + strength)


password_label = tk.Label(window, text="", font=("Arial", 14))

password_label.pack(pady=10)

strength_label = tk.Label(window, text="Strength:", font=("Arial", 12))

strength_label.pack(pady=5)

history_label = tk.Label(window, text="history:", font=("Arial", 12))

history_label.pack(pady=5)

copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_password)

copy_button.pack(pady=5)

generate_button = tk.Button(window, text="Generate Password", command=generate_password)

generate_button.pack(pady=5)

exclude_ambiguous_var = tk.BooleanVar()

exclude_ambiguous_check = tk.Checkbutton(
    window, text="Exclude ambiguous characters(0,O,l,1)", variable=exclude_ambiguous_var
)

exclude_ambiguous_check.pack(pady=5)

window.mainloop()
