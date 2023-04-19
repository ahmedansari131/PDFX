from tkinter import messagebox
from db_connect import *
from tkinter import *
from login import login_form
from main import root

# Create a function to validate the form
def signup_form():
    name = name_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if name == "":
        messagebox.showerror("Error", "Please enter your name")
    elif password == "":
        messagebox.showerror("Error", "Please enter a password")
    elif len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters")
    elif confirm_password == "":
        messagebox.showerror("Error", "Please confirm your password")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")

    try:
        if password == confirm_password:
            # Execute an INSERT query to add the new user to the database
            mycursor.execute("INSERT INTO signup (username, password) VALUES (%s, %s)", (name, password))
           
            # Commit the changes to the database
            mydb.commit()

            # Display a message to confirm the user was added
            messagebox.showinfo("User created successfully")
        else:
            messagebox.showerror("Confirm Password does not match")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")


bg_color = "#f5f5f5"
label_color = "#4d4d4d"
button_color = "#008CBA"

def signup_window():
    global name_entry
    global password_entry
    global confirm_password_entry

    # Create a frame for the signup form
    signup_frame = Frame(root, bg=bg_color)
    signup_frame.pack(fill=BOTH, expand=True, padx=20, pady=50)

    # Create labels and entries for the form
    title_label = Label(signup_frame, text="Create an Account", font=("Arial", 20, "bold"), bg=bg_color, fg=label_color, anchor="w")
    title_label.pack(pady=20)

    name_label = Label(signup_frame, text="Full Name", font=("Arial", 14), bg=bg_color, fg=label_color, anchor="w")
    name_label.pack(pady=10)

    name_entry = Entry(signup_frame, font=("Arial", 14), bg="#fff", fg="#333", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
    name_entry.pack(ipady=8, ipadx=45)

    password_label = Label(signup_frame, text="Password", font=("Arial", 14), bg=bg_color, fg=label_color, anchor="w")
    password_label.pack(pady=10)

    password_entry = Entry(signup_frame, font=("Arial", 14), bg="#fff", fg="#333", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
    password_entry.pack(ipady=8, ipadx=45)

    confirm_password_label = Label(signup_frame, text="Confirm Password", font=("Arial", 14), bg=bg_color, fg=label_color, anchor="w")
    confirm_password_label.pack(pady=10)

    confirm_password_entry = Entry(signup_frame, font=("Arial", 14), bg="#fff", fg="#333", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
    confirm_password_entry.pack(ipady=10, ipadx=45)

    # Create a frame for the buttons
    button_frame = Frame(signup_frame, bg=bg_color)
    button_frame.pack(pady=20)

    # Signup button
    submit_button = Button(button_frame, text="Signup", font=("Arial", 16), bg=button_color, fg="#fff", bd=0, highlightthickness=0, command=signup_form)
    submit_button.pack(side=LEFT, ipadx=40, ipady=5, padx=15)

    # Login button
    login_button = Button(button_frame, text="Login", font=("Arial", 16), bg=bg_color, fg="black", bd=0, highlightthickness=0, command=login_form)
    login_button.pack(side=RIGHT, ipadx=40, ipady=5, padx=15, pady=10)


# root = Tk()
root.title("Signup Form")
root.geometry("500x600")
root.resizable(False, False)

# Centering the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (500/2))
y_cordinate = int((screen_height/2) - (600/2))
root.geometry("{}x{}+{}+{}".format(500, 600, x_cordinate, y_cordinate))