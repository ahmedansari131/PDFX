import tkinter as tk

def copy_text(event):
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(label_text.get())  # Append the text to the clipboard
    status_label.config(text="Text copied!")  # Update the status label text

root = tk.Tk()

# Create a label widgetClick 
label_text = tk.StringVar()
label_text.set("Click to copy!")
label = tk.Label(root, textvariable=label_text, fg="blue", cursor="hand2")

# Bind the label to the copy_text function when it is clicked
label.bind("<Button-1>", copy_text)

# Create a status label to display the copy status
status_label = tk.Label(root, text="")

# Pack the labels in the window
label.pack()
status_label.pack()

root.mainloop()
