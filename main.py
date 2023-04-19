from tkinter import Tk
from db_connect import *
from signup import signup_window
# from signup import root


root = Tk()
# Call the signup_frame function to display the GUI
signup_window()

# Start the main event loop
root.mainloop()
