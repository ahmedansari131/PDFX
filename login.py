from tkinter import Tk, filedialog, messagebox, Frame, Label, Entry, Button, LEFT, RIGHT, BOTH
from db_connect import *
root = Tk()

bg_color = "#f5f5f5"
label_color = "#4d4d4d"
button_color = "#008CBA"

def login_form():
    # Create the login frame
    login_frame = Frame(root, bg=bg_color)
    login_frame.pack(pady=115)

    # Create labels and entries for the login form
    title_label = Label(login_frame, text="Login", font=("Arial", 20, "bold"), bg=bg_color, fg=label_color, anchor="w")
    title_label.pack(pady=20)

    name_label = Label(login_frame, text="Full Name", font=("Arial", 14), bg=bg_color, fg=label_color, anchor="w")
    name_label.pack(pady=10)

    login_user_entry = Entry(login_frame, font=("Arial", 14), bg="#fff", fg="#333", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
    login_user_entry.pack(ipady=8, ipadx=45)

    password_label = Label(login_frame, text="Password", font=("Arial", 14), bg=bg_color, fg=label_color, anchor="w")
    password_label.pack(pady=10)

    login_password_entry = Entry(login_frame, font=("Arial", 14), bg="#fff", fg="#333", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
    login_password_entry.pack(ipady=8, ipadx=45)

    button_frame = Frame(login_frame, bg=bg_color)
    button_frame.pack(pady=20)

    # Create a button to go back to the signup form
    back_button = Button(button_frame, text="Back", font=("Arial", 16), bg=bg_color, fg="black", bd=0, highlightthickness=0)
    back_button.pack(side=LEFT, ipadx=40, ipady=5, padx=15)

    login_button = Button(button_frame, text="Login", font=("Arial", 16), bg=button_color, fg="#fff", bd=0, highlightthickness=0)
    login_button.pack(side=RIGHT, ipadx=40, ipady=5, padx=15, pady=10)
