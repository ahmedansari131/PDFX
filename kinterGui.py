import difflib
import io
from tkinter import Image, Tk, filedialog, messagebox, Frame, Label, Entry, Button, LEFT, RIGHT, BOTH, END
from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
import pytesseract
import PyPDF2
from db_connect import *
import os
import copy
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
from tkcalendar import DateEntry

allPDF = {}
assign_details = {}
plag = {}
avg_plag = {}
plag_values_list = []
calc_avg_plag = []
sum_of_similarity= []
plag_key = []
a = {}
b = 0
sum_of_value = []
create_assign = {}
count_of_assignment = 0
# global st_loggedin, te_loggedin
st_loggedin = False
te_loggedin = False
path_list = []
plagiarism = []
comp_plag = {}

###############################  COLORS VARIABLE  ###############################
bg_color = "#f2f2f3"
label_color = "#1B1212"
button_color = "#003151"
btn_hover_color = "#004d80"
btn_hover_white = "#C6E6FB"
btn_color = "#003151"
success = "#3bb54a"
error = "#ff3333"


def open_signup_frame():
    main_frame.pack_forget()
    login_frame.place_forget()
    signup_frame.place(relx=.5, rely=.5, anchor="center")
    dialog_frame.place_forget()

def open_login_frame():
    main_frame.pack_forget()
    signup_frame.place_forget()
    login_frame.place(relx=.5, rely=.5, anchor="center")
    dialog_frame.place_forget()

def close_login_frame():
    login_frame.pack_forget()

def open_main_frame():
    main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

def open_student_home_frame():
    student_home_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    student_upload_frame.pack_forget()
    close_dialog_box()

def open_assignment_card_frame():
    assignment_main_card_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    student_home_frame.pack_forget()


def close_assignment_main_card_frame():
    if st_loggedin:
        assignment_main_card_frame.pack_forget()
        student_home_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    elif te_loggedin:
        assignment_main_card_frame.pack_forget()
        assignment_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

def open_assignment_main_card_frame():
    assignment_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

def open_assignment_frame():
    assignment_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    home_main_frame.pack_forget()

def close_assignment_frame():
    assignment_main_frame.pack_forget()
    home_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

def close_detail_frame():
    detail_main_frame.pack_forget()
    open_home_frame()

def clear_signup_form():
    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    c_pass_entry.delete(0, tk.END)

def clear_login_form():
    login_user_entry.delete(0, tk.END)
    login_pass_entry.delete(0, tk.END)

def clear_details_form():
    sub_name_entry.delete(0, tk.END)
    te_name_entry.delete(0, tk.END)
    t_marks_entry.delete(0, tk.END)
    p_marks_entry.delete(0, tk.END)

###############################  sIGNUP LOGIC  ###############################
def signup_form(db_name):
    print("Entering into the database", db_name)
    global name
    name = user_entry.get()
    password = pass_entry.get()
    confirm_password = c_pass_entry.get()

    if name == "":
        dialog_box("Enter your name", open_signup_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif password == "":
        dialog_box("Enter the password", open_signup_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif len(password) < 8:
        dialog_box("Password must be at least 8 characters", open_signup_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif password != confirm_password:
        dialog_box("Password do not match", open_signup_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    try:
        if password == confirm_password and name != None and password != None and confirm_password != None:
            # Execute an INSERT query to add the new user to the database
            print(db_name)
            mycursor.execute("INSERT INTO {} (username, password) VALUES (%s, %s)".format(db_name), (name, password))
            # Commit the changes to the database
            mydb.commit()

            dialog_box("Registered successfully!", open_login_frame, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
            clear_signup_form()
        else:
            messagebox.showerror("Confirm Password does not match")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

############################### LOGIN LOGIC  ###############################
def validate_login(db_name):
    # Get the username and password values from the form
    global name
    name = login_user_entry.get()
    password = login_pass_entry.get()
    print("User name is",name)
    print(password)
    try:
        # Execute a SELECT query to check if the username and password exist in the database
        query = ("SELECT * FROM {} WHERE username = %s AND password = %s".format(db_name))
        mycursor.execute(query, (name, password))

        # Get the result of the query
        result = mycursor.fetchone()
        print(result)

        # If the result is not empty, the user is logged in
        if result:
            if db_name == "te_signup":
                dialog_box("You are loggedin!", open_home_frame, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
                clear_login_form()
                global te_loggedin, st_loggedin
                te_loggedin = True
                st_loggedin = False
            else:
                dialog_box("You are loggedin!", open_student_home_frame, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
                clear_login_form()
                st_loggedin = True
                te_loggedin = False
            
            # select_files_gui()
        elif len(name) == 0:
            dialog_box("Enter the details", open_login_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
        elif len(password) == 0:
            dialog_box("Enter the details", open_login_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
        else:
            dialog_box("Incorrect Credentials", open_login_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")


###############################  SELECT FILE LOGIC  ###############################
def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    path_list.extend(file_paths)
    for path in file_paths:
        print("Selected file:", path)
        pdf_name = os.path.basename(path)
        pdf_name = os.path.splitext(pdf_name)[0]
        allPDF[pdf_name] = path
        print(allPDF)
        print(pdf_name)


###############################  UPLOADING PDF LOGIC  ###############################
def upload_files():
    if len(path_list) == 0:
        print("No files selected!")
        return

    print("Uploading files...")
    for path in path_list:
        # Store the path of each file in a database or a text file
        print("File path:", path)

    path_list.clear()
    print("Upload complete!")
    if te_loggedin:
        calc_plag()
        plag_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
        upload_main_frame.pack_forget()
    else:
        dialog_box("Files are uploaded", close_dialog_box, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
    print("Executed")

###############################  EXTRACTING IMAGE LOGIC  ###############################
def extractImg(allPDF):
    for key in allPDF:
        pdf_file = key
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        images = []
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            try:
                xObject = page['/Resources']['/XObject'].getObject()
            except KeyError:
                continue
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj]._data
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"
                    stream = io.BytesIO(data)
                    image = Image.open(stream)
                    image = image.convert(mode)
                    images.append(image)
        return stream

###############################  EXTRACTING DATA FROM IMAGE LOGIC  ###############################
def readFrmImg(allPDF):
        # Reading the text from the image
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        try:
            for key in allPDF:
                imgData = extractImg(allPDF)
                images = Image.open(key)  #Opening the image
                custom_config = r'-l eng --oem 3 --psm 6'
                text = pytesseract.image_to_string(images,config=custom_config)  #Storing the extracted text in the variable

                #Storing the text extracted from the image into the txt file
                filename = r"C:\Users\ANSHARI\Desktop\demo3.txt"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w") as f:
                    f.write(text)
                return text
        except:
            return "0"

###############################  EXTRACT DATA FROM PDF LOGIC  ###############################
def getTxt(allPDF, imgTxt):
    newPDF = copy.deepcopy(allPDF)
    for key in allPDF:
        for i in range(PyPDF2.PdfFileReader(allPDF[key]).getNumPages()):
            page = PyPDF2.PdfFileReader(allPDF[key]).getPage(i)
            pdfText = imgTxt + page.extractText()
            rm_line_txt = '\n'.join([line for line in pdfText.split('\n') if line.strip()])
            low_pdf_txt = rm_line_txt.lower()
            cln_pdf_txt = low_pdf_txt.replace(" ", "")
            # print("This is clean text",cln_pdf_txt)
            newPDF[key] = cln_pdf_txt
    return newPDF

###############################  STORING ENTIRE DATA INTO THE VARIABLE  ###############################
def entire_text():
    entireTxt = ''
    imgTxt = readFrmImg(allPDF)
    entireTxt = getTxt(allPDF, imgTxt)
    # print(entireTxt)
    return entireTxt

############################### CALCULATING THE PLAGIARISM  ###############################
def calc_plag():
    entireTxt = entire_text()
    for file1, txt1 in entireTxt.items():
        for file2, txt2 in entireTxt.items():
            if file1 < file2:
                seq = difflib.SequenceMatcher(None, txt1, txt2)
                similarity_ratio = seq.ratio()
                # print("Keys are",allPDF.keys())
                plag[file1, file2] = round(similarity_ratio*100, 2)
                print("This is dictionary of similarity",plag)

                matches = seq.get_matching_blocks()
                # for match in matches:
                #     match_text = txt1[match.a:match.a+match.size]
                #     print("Match text is:", match_text)
                if similarity_ratio > 0.8:  # adjust the threshold as needed
                    print(f"{file1} and {file2} have a high plagiarism: {round(similarity_ratio*100, 2)} %\n")
                else:
                    print(f"{file1} and {file2} has plagiarism: {round(similarity_ratio*100, 2)} %\n")

    plag_values = plag.values()
    global plag_values_list 
    plag_values_list = list(plag_values)

    def dynamic_label():
        pdf_list = list(allPDF)
        length_of_pdf = len(pdf_list)
        print("This is length of pdf",length_of_pdf)

        for first_key, value in plag.items():
              first_char = first_key[0]
              if first_char in comp_plag:
                comp_plag[first_char].append(value)
              else:
                comp_plag[first_char] = [value]
        print("This is new dictionary", comp_plag)
        i = 0
        for key, value in comp_plag.items():
            greatest_value = max(value)
            print(f"The greatest value in the list {key} is {greatest_value}.")
            plagiarism.append(greatest_value)
        print(greatest_value)
                
        table.place(relx=.5, rely=.55, anchor="center")
        for i, key in enumerate(allPDF.keys()):
            try:
                table.insert(parent='', index='end', iid=i, text=f"{i+1}.", values=(key, plagiarism[i]))
            except:
                table.insert(parent='', index='end', iid=i, text=f"{i+1}.", values=(key, plagiarism[i-1]))
    return dynamic_label

############################### CREATING THE ASSIGNMENT CARDS  ###############################
def open_st_upload(event):
    student_upload_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    assignment_main_card_frame.pack_forget()


def create_assignment_cards():
    global count_of_assignment
    print("this is count", count_of_assignment)

    for i in range(1, count_of_assignment+1):
        print("this is i", i)
        assign_card = Frame(assignment_card_frame, bg=button_color, padx=30, pady=15)
        assign_card.place(relx=0, rely=(0.25*i), anchor="nw", width=1180)
        
        assignment_label = Label(assign_card, text=f'{create_assign["assignment title"]}'[0].upper() + f'{create_assign["assignment title"]}'[1:],  font=("Roboto", 16, "bold", "underline"), bg=button_color, fg="white", anchor="w", cursor="hand2")
        assignment_label.grid(row=1, column=0, sticky="w", pady=(0,10))

        assignment_subject_label = Label(assign_card, text=f"Subject: "+f'{create_assign["subject"]}'[0].upper() + f'{create_assign["subject"]}'[1:],  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
        assignment_subject_label.grid(row=2, column=0, sticky="w")

        assignment_marks_label = Label(assign_card, text=f'Marks: {create_assign["marks"]}',  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
        assignment_marks_label.grid(row=3, column=0, sticky="w")

        assignment_date_label = Label(assign_card, text=f'Due date: {create_assign["due date"]}',  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
        assignment_date_label.grid(row=4, column=0, sticky="w")
        print("This is student login", st_loggedin)

        if st_loggedin:
            assignment_label.bind("<Button-1>", open_st_upload)

def clear_assignment_details():
    assign_name_entry.delete(0, tk.END)
    subject_name_entry.delete(0, tk.END)
    t_marks_entry.delete(0, tk.END)
    due_date_entry.delete(0, END)

def close_assignment_detail_frame():
    assignment_main_frame.pack_forget()

def get_assignment_details():
    global count_of_assignment  # declare the variable as global
    assign_title = assign_name_entry.get()
    subject = subject_name_entry.get()
    assign_total_marks = t_marks_entry.get()
    assign_due_date = due_date_entry.get()

    create_assign["assignment title"] = assign_title
    create_assign["subject"] = subject
    create_assign["marks"] = assign_total_marks
    create_assign["due date"] = assign_due_date

    print(create_assign)
    print("This is before increment",count_of_assignment)

    if subject == "" and assign_title == "" and assign_total_marks == "":
        print("This is none")
        dialog_box("Enter the details", lambda:(close_dialog_box(), open_assignment_main_card_frame()), error, bg_color, "white", r"C:\Users\ANSHARI\Downloads\Python project\close.png")
        assignment_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    else:
        try:
            # Execute an INSERT query to add the new user to the database
            assign_table_name = "assignments"
            mycursor.execute(f"INSERT INTO {assign_table_name} (assign_name, sub_name, total_marks, due_date) VALUES (%s, %s, %s, %s)".format(assign_table_name), (create_assign['assignment title'], create_assign["subject"], create_assign["marks"], create_assign["due date"]))
            # Commit the changes to the database
            mydb.commit()

            dialog_box("Assignment created successfullly!", close_dialog_box, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")

        except mysql.connector.Error as e:
             print(f"The error '{e}' occurred")

        def open_assignment_card_frame():
            assignment_main_card_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
            close_assignment_detail_frame()
        open_assignment_card_frame()
        count_of_assignment = count_of_assignment + 1
        print("After increment",count_of_assignment)

        return create_assign

dynamic_label = calc_plag()

###############################  GET DETAILS FOR THE FORM  ###############################
def get_details():
    teacher_name = te_name_entry.get()
    subject_name = sub_name_entry.get()
    total_marks = t_marks_entry.get()
    pass_marks = p_marks_entry.get()

    if pass_marks != "":
        try:
            pass_marks = int(pass_marks)
            assign_details["pmarks"] = pass_marks
        except ValueError:
            dialog_box("Number is required for the passing marks", open_student_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    if total_marks != "":
        try:
            total_marks = int(pass_marks)
            assign_details["tmarks"] = pass_marks
        except ValueError:
            dialog_box("Number is required for the passing marks", open_student_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    if teacher_name== "":
        print(teacher_name)
        dialog_box("Enter the details", open_student_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif subject_name == "":
        dialog_box("Enter the details", open_student_frame, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    else:
        dialog_box("Details entered successfully!", lambda:(select_files_gui(), close_dialog_box()), success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")


    clear_details_form()
    print(assign_details)

###############################  FILE SELECTING GUI  ###############################
def select_files_gui():
    detail_main_frame.pack_forget()
    def close_select_files_gui():
        upload_main_frame.place_forget()
    global path_list
    path_list = []
    global upload_main_frame

    upload_main_frame = Frame(root, bg="white")
    upload_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

    upload_sub_frame = Frame(upload_main_frame, bg="white")
    upload_sub_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

    label_frame = Frame(upload_sub_frame, bg="white")
    label_frame.place(relx=.5, rely=.5, anchor="center")

    label = Label(label_frame, text=f"FOR {(assign_details['subject']).upper()}", font=("Roboto", 18, "bold", "underline"), bg="white", fg=button_color)
    label.pack(anchor="center", pady=20)

    label = Label(label_frame, text="Note: Pdf's name should be the name of the students", font=("Roboto", 12,), bg="white", fg=button_color)
    label.pack(anchor="center", pady=(0,10))

    sel_upl_btn_frame = Frame(label_frame, bg="white")
    sel_upl_btn_frame.pack(anchor="center", pady=5)

    create_btn(sel_upl_btn_frame, LEFT, "Select Files", select_files, button_color, "white", 14, 5, 40, btn_hover_color, button_color)
    create_btn(sel_upl_btn_frame, RIGHT, "Upload Files", lambda:(upload_files(), close_select_files_gui(), dynamic_label()), "white", button_color, 14, 5, 40, btn_hover_white, "white")

score = []

###############################  BUTTON FUNCTION TO USE THROUGHOUT THE PROGRAM  ###############################
def create_btn(button_frame, align, btn_text, com, bg_col, fg_col, ft_size, y, x, btn_hover_color, btn_color):
    button = Button(button_frame, text=btn_text, font=("Roboto", ft_size, "bold"), bg=bg_col, fg=fg_col, bd=0, highlightthickness=0, cursor="hand2", command=com, )
    button.pack(side=align, ipadx=x, ipady=y, padx=15, pady=15)
    button.bind("<Enter>", lambda event: on_enter(event, btn_hover_color))
    button.bind("<Leave>", lambda event: on_leave(event, btn_color))

###############################  HOVER EFFECT FUNCITONS ###############################
def on_enter(event, btn_hover_color):
    event.widget.config(bg=btn_hover_color)
def on_leave(event, btn_color):
    event.widget.config(bg=btn_color)

###############################  REGISTRATION MODAL  ###############################
def create_modal(name):
    modal_frame = Frame(root, padx=50, pady=20, bg=button_color)
    modal_frame.place(relx=.5, rely=.5, anchor="center")

    modal_title = Label(modal_frame, text=name, font=("Roboto", 25, "bold"), bg=button_color, fg="white", anchor="w")
    modal_title.pack(pady=(0,10))

    button_frame = Frame(modal_frame, bg=button_color)
    button_frame.pack()

    create_btn(button_frame, LEFT, "Login", lambda:(close_modal(), open_login_frame()), "white", label_color, 12, 5, 32, btn_hover_white, "white")
    create_btn(button_frame, RIGHT, "Signup", lambda:(close_modal(), open_signup_frame()), "white", label_color, 12, 5, 32, btn_hover_white, "white")

    # Bind the mouse click event to a function that closes the modal frame
    main_frame.bind("<Button-1>", lambda event: modal_frame.destroy())

    def close_modal():
        modal_frame.destroy()

root = tk.Tk()
root.iconbitmap(r"C:\Users\ANSHARI\Downloads\Python project\pdfx1-02.ico")

###############################  MAIN FRAME  ###############################
main_frame = Frame(root, bg="white")
main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

title_frame = Frame(main_frame, bg="white")
title_frame.place(relx=.5, rely=.5, anchor="center")

global logo_main_img
logo_main_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\pdfx1-02.png")
logo_main_img = logo_main_img.subsample(2)
label = Label(title_frame, image= logo_main_img, bg="white")
label.pack(pady=30)

welcome_title = Label(title_frame, text="Welcome to PDFX", font=("Roboto", 30, "bold"), bg="white", fg=label_color)
welcome_title.pack(padx=20)

main_title = Label(title_frame, text="Login to proceed with the app", font=("Roboto", 15), bg="white", fg=label_color)
main_title.pack(pady=10)

button_frame = Frame(title_frame, bg="white")
button_frame.pack()

def count_st():
    i = 0
    i = i + 1
    global db_name
    db_name = "st_signup"
    print("Student clicked")

def count_te():
    i = 1
    i = i + 1
    global db_name
    db_name = "te_signup"
    print("Teacher clicked")

create_btn(button_frame, LEFT, "Students", lambda: (create_modal("For students"), count_st()), button_color, "white", 12, 7, 22, btn_hover_color, button_color)
create_btn(button_frame, RIGHT, "Teachers", lambda: (create_modal("For teachers"), count_te()), button_color, "white", 12, 7, 22, btn_hover_color, button_color)

###############################  SIGNUP FRAME  ###############################
signup_frame = Frame(root, bg="white", padx=50, pady=40)

small_title_label = Label(signup_frame, text= "Teacher registration", font=("Roboto", 12, "underline"), bg="white", fg="#003d66", anchor="w")
small_title_label.pack(pady=(0, 20))

title_label = Label(signup_frame, text="Create an account", font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w")
title_label.pack(pady=(0, 10))

user_frame = Frame(signup_frame, bg="white")
user_frame.pack(pady=(25, 25))
user_label = Label(user_frame, text="Username", font=("Roboto", 14), bg="white", fg=button_color)
user_label.grid(row=0, column=0, sticky=tk.W)
user_entry = Entry(user_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
user_entry.grid(row=1, column=0,ipady=8, ipadx=50, pady=(0,25))

pass_frame = Frame(signup_frame, bg="white")
pass_frame.pack()
pass_label = Label(user_frame, text="Password", font=("Roboto", 14), bg="white", fg=button_color)
pass_label.grid(row=4, column=0, sticky=tk.W)
pass_entry = Entry(user_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", show="*")
pass_entry.grid(row=5, column=0,ipady=8, ipadx=50, pady=(0,25))

c_pass_frame = Frame(signup_frame, bg="white")
c_pass_frame.pack()
c_pass_label = Label(user_frame, text="Confirm Password", font=("Roboto", 14), bg="white", fg=button_color)
c_pass_label.grid(row=7, column=0, sticky=tk.W)
c_pass_entry = Entry(user_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", show="*")
c_pass_entry.grid(row=8, column=0,ipady=8, ipadx=50)

# Create a frame for the buttons
button_frame = Frame(signup_frame, bg="white")
button_frame.pack()

create_btn(button_frame, LEFT, "Signup", lambda:signup_form(db_name), button_color, "white", 14, 5, 40, btn_hover_color, button_color)
create_btn(button_frame, LEFT, "Login", open_login_frame, "white", button_color, 14, 5, 40, "#FAF9F6", "white")

root.title("PDFX")
root.geometry("1900x1000")
root.resizable(False, False)

# Centering the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (1350/2))
y_cordinate = int((screen_height/2) - (750/2))
root.geometry("{}x{}+{}+{}".format(1350, 750, x_cordinate, y_cordinate))

###############################  LOGIN FRAME  ###############################
# Create the login frame
login_frame = Frame(root, bg="white", padx=50, pady=40)

small_title_label = Label(login_frame, text= "Teacher sign in", font=("Roboto", 12, "underline"), bg="white", fg="#003d66", anchor="w")
small_title_label.pack(pady=(0, 20))

login_title_label = Label(login_frame, text="Log In", font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w")
login_title_label.pack(pady=(0, 10))

login_user_frame = Frame(login_frame, bg="white")
login_user_frame.pack(pady=(25, 25))
login_user_label = Label(login_user_frame, text="Username", font=("Roboto", 14), bg="white", fg=button_color)
login_user_label.grid(row=0, column=0, sticky=tk.W)
login_user_entry = Entry(login_user_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
login_user_entry.grid(row=1, column=0,ipady=8, ipadx=50, pady=(0,5))

login_pass_frame = Frame(login_frame, bg="white")
login_pass_frame.pack()
login_pass_label = Label(login_pass_frame, text="Password", font=("Roboto", 14), bg="white", fg=button_color)
login_pass_label.grid(row=2, column=0, sticky=tk.W)
login_pass_entry = Entry(login_pass_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", show="*")
login_pass_entry.grid(row=3, column=0,ipady=8, ipadx=50, pady=(0,35))

# Create a frame for the buttons
login_button_frame = Frame(login_frame, bg="white")
login_button_frame.pack()

create_btn(login_button_frame, RIGHT, "Login", lambda:(validate_login(db_name)),button_color, "white", 14, 5, 40, btn_hover_color, button_color)
create_btn(login_button_frame, LEFT, "Signup", open_signup_frame, "white", button_color, 14, 5, 40, "#FAF9F6", "white")

###############################  HOME FRAME AFTER LOGIN  ###############################
def open_home_frame():
    login_frame.place_forget()
    dialog_frame.place_forget()

    def logout():
        dialog_box("You are logged out!", close_dialog_box, button_color, "white", "white", r"C:\Users\ANSHARI\Downloads\Python project\logout.png")
        home_main_frame.destroy()
        open_main_frame()
        detail_main_frame.pack_forget()
        det_logout_button_frame.place_forget()

    def open_details_frame():
        home_main_frame.destroy()
        detail_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
        # detail_frame.place(relx=.5, rely=.5, anchor="center")

    global home_main_frame
    home_main_frame = Frame(root, bg="white")
    home_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

    home_frame = Frame(home_main_frame, bg="white")
    home_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

    home2_frame = Frame(home_frame, bg="white", padx=50)
    home2_frame.place(relx=.5, rely=.5, anchor="center")

    img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\profile.png")
    img= img.subsample(13)

    # Create a label with an image and text, and place it at the top left of the frame
    user_id = Label(home_frame, text=name, font=("Roboto", 14), bg='white', image=img, compound="left",padx=15, pady=10)
    user_id.image = img
    user_id.place(relx=0, rely=0, anchor='nw')

    # Create a label with an image and text, and place it at the top left of the frame
    user_id = Label(detail_frame, text=name, font=("Roboto", 14), bg='white', image=img, compound="left",padx=15, pady=10)
    user_id.image = img
    user_id.place(relx=0, rely=0, anchor='nw')

    # Logout button
    logout_button_frame = Frame(home_frame, bg="white")
    logout_button_frame.place(relx=1, rely=0, anchor='ne')
    create_btn(logout_button_frame, RIGHT, "Logout", lambda:(logout()), button_color, "white", 14, 3, 25, btn_hover_color, button_color)

    container_frame1 = Frame(home2_frame, bg="white", bd=0, relief="solid", highlightbackground=button_color, highlightthickness=1)
    container_frame2 = Frame(home2_frame, bg="white", bd=0, relief="solid", highlightbackground=button_color, highlightthickness=1)
    container_frame3 = Frame(home2_frame, bg="white", bd=0, relief="solid", highlightbackground=button_color, highlightthickness=1)
    container_frame4 = Frame(home2_frame, bg="white", bd=0, relief="solid", highlightbackground=button_color, highlightthickness=1)

    container_frame1.grid(row=0, column=1,sticky="nw",ipadx=140, ipady=110, pady=(50,0), padx=80)
    container_frame2.grid(row=0, column=2, sticky="ne", ipadx=140, ipady=110, pady=(50,0), padx=80)
    container_frame3.grid(row=1, column=1,sticky="sw",ipadx=140, ipady=110, pady=(50,0), padx=80)
    container_frame4.grid(row=1, column=2, sticky="se", ipadx=140, ipady=110, pady=(50,0), padx=80)

    global assignment_img, plag_img, sub_assign_img, assign_img
    assignment_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\assignment.png")
    assignment_img = assignment_img.subsample(10)
    assignment_logo_label = tk.Label(container_frame1, image=assignment_img, bg="white")
    assignment_logo_label.place(relx=.5, rely=.45, anchor="s")
    button_frame = Frame(container_frame1, bg="white")
    button_frame.place(relx=.5, rely=.9, anchor='s')
    create_btn(button_frame, 'bottom', "Create Assignments",open_assignment_frame, button_color, "white", 12, 7, 25, btn_hover_color, button_color)

    plag_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\plag.png")
    plag_img = plag_img.subsample(10)
    plag_logo_label = tk.Label(container_frame2, image=plag_img, bg="white")
    plag_logo_label.place(relx=.5, rely=.45, anchor="s")
    button_frame = Frame(container_frame2, bg="white")
    button_frame.place(relx=.5, rely=.9, anchor='s')
    create_btn(button_frame, 'bottom', "Check Plagiarism", open_details_frame, button_color, "white", 12, 7, 25, btn_hover_color, button_color)

    assign_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\plag.png")
    assign_img = assign_img.subsample(10)
    assignment_logo_label = tk.Label(container_frame3, image=assign_img, bg="white")
    assignment_logo_label.place(relx=.5, rely=.45, anchor="s")
    button_frame = Frame(container_frame3, bg="white")
    button_frame.place(relx=.5, rely=.9, anchor='s')
    create_btn(button_frame, 'bottom', "Show Assignments", "open_details_frame", button_color, "white", 12, 7, 25, btn_hover_color, button_color)

    sub_assign_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\plag.png")
    sub_assign_img = sub_assign_img.subsample(10)
    sub_assign_logo_label = tk.Label(container_frame4, image=sub_assign_img, bg="white")
    sub_assign_logo_label.place(relx=.5, rely=.45, anchor="s")
    button_frame = Frame(container_frame4, bg="white")
    button_frame.place(relx=.5, rely=.9, anchor='s')
    create_btn(button_frame, 'bottom', "Submitted Assignments", "open_details_frame", button_color, "white", 12, 7, 25, btn_hover_color, button_color)

def open_student_frame():
    close_dialog_box()
    print("You are in the student frame")
    
###############################  DIALOG BOX  ###############################
def dialog_box(msg, cmd, bgColor, btnColor, labelColor, logo_path):
    global dialog_frame, logo_img
    
    dialog_frame = Frame(root, bg=bgColor, padx=25, pady=20)
    dialog_frame.place(relx=.5, rely=.5, anchor="center")

    logo_img = tk.PhotoImage(file=logo_path)
    logo_img = logo_img.subsample(9)
    logo_label = Label(dialog_frame, image=logo_img, bg=bgColor)
    logo_label.pack(pady=(0,20))

    dialog_label = Label(dialog_frame, text=msg, font=("Roboto", 15), bg=bgColor, fg=labelColor, anchor="w")
    dialog_label.pack()

    create_btn(dialog_frame, "top", "Ok", cmd, btnColor, label_color, 14, 0, 40, btn_hover_white, btnColor)

def close_dialog_box():
    dialog_frame.place_forget()

###############################  DETAILS FORM ###############################

detail_main_frame = Frame(root, bg="white", padx=15, pady=15)
# home_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

detail_frame = Frame(detail_main_frame, bg="white")
detail_frame.pack(fill='both', expand=True)

img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\profile.png")
img= img.subsample(13)

det_form_frame = Frame(detail_frame, bg="white")
det_form_frame.place(relx=.5, rely=.5, anchor="center")

subject_frame = Frame(det_form_frame, bg="white")
subject_frame.grid(row=0, column=0, sticky="w", padx=(0,80))

teacher_frame = Frame(det_form_frame, bg="white")
teacher_frame.grid(row=0, column=1, sticky="w")

t_marks_frame = Frame(det_form_frame, bg="white")
t_marks_frame.grid(row=1, column=0,  padx=(0,80), pady=(50,0))

p_marks_frame = Frame(det_form_frame, bg="white")
p_marks_frame.grid(row=1, column=1, sticky="w", pady=(50,0))

sub_name = Label(subject_frame, text="Subject",  font=("Roboto", 14, "bold"), bg="white", fg=button_color, anchor="w")
sub_name_entry = Entry(subject_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
sub_name.grid(row=0, column=0, sticky="w")
sub_name_entry.grid(row=1, column=0, ipady=8, ipadx=50)

te_name = Label(teacher_frame, text="Teacher",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
te_name_entry = Entry(teacher_frame, font=("Roboto", 14), bg="#fff", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
te_name.grid(row=0, column=0, sticky="w")
te_name_entry.grid(row=1, column=0, sticky="w", ipady=8, ipadx=50)

t_marks = Label(t_marks_frame, text="Total Marks",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
t_marks_entry = Entry(t_marks_frame, font=("Roboto", 14), bg="white", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
t_marks.grid(row=0, column=0, sticky="w")
t_marks_entry.grid(row=1, column=0,ipady=8, ipadx=50)

p_marks = Label(p_marks_frame, text="Passing Marks",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
p_marks_entry = Entry(p_marks_frame, font=("Roboto", 14), bg="white", fg=button_color, bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
p_marks.grid(row=0, column=0, sticky="w")
p_marks_entry.grid(row=1, column=0, ipady=8, ipadx=50)

submit_button = Button(det_form_frame, text="Submit", font=("Roboto", 14, "bold"), bg=button_color, fg="white", bd=0, highlightthickness=0, cursor="hand2", command=lambda:(get_details()," select_files_gui()"))
submit_button.grid(row=2, column=1, pady=(50,0), ipadx=125, ipady=5, sticky="e")

back_button =  Button(det_form_frame, text="Back", font=("Roboto", 14, "bold"), bg="white", fg=button_color,bd =0, highlightthickness=0, relief="solid", highlightbackground="pink", cursor="hand2", command=close_detail_frame)

back_button.grid(row=2, column=0, pady=(50,0), ipadx=135, ipady=5, sticky="w")

submit_button.bind("<Enter>", lambda event: on_enter(event, btn_hover_color))
submit_button.bind("<Leave>", lambda event: on_leave(event, button_color))

back_button.bind("<Enter>", lambda event: on_enter(event, btn_hover_white))
back_button.bind("<Leave>", lambda event: on_leave(event, "white"))


###############################  CREATE ASSIGMENT DETAILS FORM ###############################

assignment_main_frame = Frame(root, bg="white", padx=15, pady=15)
# assignment_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

assignment_frame = Frame(assignment_main_frame, bg="white")
assignment_frame.pack(fill='both', expand=True)

img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\profile.png")
img= img.subsample(13)

assign_form_frame = Frame(assignment_frame, bg="white")
assign_form_frame.place(relx=.5, rely=.55, anchor="center")

assignment_title_frame = Frame(assign_form_frame, bg="white")
assignment_title_frame.grid(row=0, column=0, sticky="w", padx=(0,80))

subject_frame = Frame(assign_form_frame, bg="white")
subject_frame.grid(row=0, column=1, sticky="w")

t_marks_frame = Frame(assign_form_frame, bg="white")
t_marks_frame.grid(row=1, column=0,  padx=(0,80), pady=(50,0))

date_frame = Frame(assign_form_frame, bg="white")
date_frame.grid(row=1, column=1, sticky="w", pady=(50,0))

create_assign_heading = Label(assignment_frame, text="Create Assignments".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w")
create_assign_heading.pack(pady=(40,0))

assign_name = Label(assignment_title_frame, text="Title",  font=("Roboto", 14, "bold"), bg="white", fg=button_color, anchor="w")
assign_name_entry = Entry(assignment_title_frame, font=("Roboto", 14), bg="#fff", fg=label_color, bd=0, highlightthickness=1, highlightbackground=button_color, highlightcolor=button_color)
assign_name.grid(row=0, column=0, sticky="w")
assign_name_entry.grid(row=1, column=0, ipady=8, ipadx=50)

subject_name = Label(subject_frame, text="Subject",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
subject_name_entry = Entry(subject_frame, font=("Roboto", 14), bg="#fff", fg=label_color, bd=0, highlightthickness=1, highlightbackground=button_color, highlightcolor=button_color)
subject_name.grid(row=0, column=0, sticky="w")
subject_name_entry.grid(row=1, column=0, sticky="w", ipady=8, ipadx=50)

t_marks = Label(t_marks_frame, text="Total Marks",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
t_marks_entry = Entry(t_marks_frame, font=("Roboto", 14), bg="white", fg=label_color, bd=0, highlightthickness=1, highlightbackground=button_color, highlightcolor=button_color)
t_marks.grid(row=0, column=0, sticky="w")
t_marks_entry.grid(row=1, column=0,ipady=8, ipadx=50)

due_date = Label(date_frame, text="Due date",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
due_date_entry = DateEntry(date_frame, font=("Roboto", 14), bg="white", fg=button_color)
due_date.grid(row=0, column=0, sticky="w")

due_date_entry.grid(row=1, column=0, ipady=8, ipadx=85)
submit_button = Button(assign_form_frame, text="Done", font=("Roboto", 14, "bold"), bg=button_color, fg="white", bd=0, highlightthickness=0, cursor="hand2", command=lambda:(get_assignment_details(), close_assignment_detail_frame(), create_assignment_cards(), clear_assignment_details()))
submit_button.grid(row=2, column=1, pady=(50,0), ipadx=134, ipady=5, sticky="e")

back_button =  Button(assign_form_frame, text="Back", font=("Roboto", 14, "bold"), bg="white", fg=button_color,bd =0, highlightthickness=0, relief="solid", highlightbackground="pink", cursor="hand2", command=close_assignment_frame)
back_button.grid(row=2, column=0, pady=(50,0), ipadx=135, ipady=5, sticky="w")

submit_button.bind("<Enter>", lambda event: on_enter(event, btn_hover_color))
submit_button.bind("<Leave>", lambda event: on_leave(event, button_color))

back_button.bind("<Enter>", lambda event: on_enter(event, btn_hover_white))
back_button.bind("<Leave>", lambda event: on_leave(event, "white"))


###############################  ASSIGNMENT CREATED CARDS  ###############################

assignment_main_card_frame = Frame(root, bg="white", padx=15, pady=15)

assignment_card_frame = Frame(assignment_main_card_frame, bg="white", padx=20)
assignment_card_frame.pack(fill='both', expand=True)

img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\profile.png")
img= img.subsample(13)

assignment_header_frame = Frame(assignment_card_frame, bg="white")
assignment_header_frame.place(relx=.5, rely=0.1, anchor="center", width=1180, height=100)

assign_heading = Label(assignment_header_frame, text="Assignments".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w")
assign_heading.place(relx=0, rely=.5, anchor="w")

back_button =  Button(assignment_header_frame, text="Back", font=("Roboto", 14, "bold"), bg=button_color, fg="white",bd =0, highlightthickness=0, relief="solid",highlightbackground="pink", cursor="hand2", padx=25, pady=5, command=close_assignment_main_card_frame)
back_button.place(relx=1, rely=.5, anchor='e')

back_button.bind("<Enter>", lambda event: on_enter(event, btn_hover_color))
back_button.bind("<Leave>", lambda event: on_leave(event, button_color))


###############################  GUI FOR SHOWING THE PLAGIARISM PERCENTAGE  ###############################

plag_main_frame = Frame(root, bg="white")
# student_upload_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
# plag_main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

plag_sub_frame = Frame(plag_main_frame, bg="white")
plag_sub_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

sub_plag_frame = Frame(plag_sub_frame, bg="white", padx=0, pady=10)
sub_plag_frame.pack(anchor="center")

teach_plag_frame = Frame(plag_sub_frame, bg="pink", padx=0, pady=10)
teach_plag_frame.pack(anchor="center")

plag_label = Label(plag_sub_frame, text="Plagiarism Percentage",  font=("Roboto", 30, "bold"), bg="white", fg=button_color, pady=15)
plag_label.pack(anchor="center")

# Create the table
table = ttk.Treeview(root, columns=('Student name', 'Plagiarism found'))
# table.place(relx=.5, rely=.55, anchor="center")

# Define the headings for each column
table.heading('#0', text='Index'.upper())
table.heading('Student name', text='Student name'.upper())
table.heading('Plagiarism found', text='Plagiarism found'.upper())

# Set the column widths and alignments
table.column('Student name', width=400, anchor='center')
table.column('Plagiarism found', width=400, anchor='center')
table.column('#0', width=150, anchor='center')

# Apply the style to the table
style = ttk.Style()
style.configure('Treeview', background='white', foreground=button_color, rowheight=25, font=('roboto', 12))
style.configure('Treeview.Heading', background='white', foreground=button_color, font=('roboto', 14, 'bold'))
style.configure('Treeview.Heading', padding=(0, 25))

# Place the table using grid() method and set padding between cells
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)


###############################  STUDENT HOME PAGE  ###############################

student_home_frame = Frame(root, bg="white")
# student_home_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

student_frame = Frame(student_home_frame, bg="white")
student_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

student_home2_frame = Frame(student_frame, bg="white", padx=50)
student_home2_frame.place(relx=.5, rely=.5, anchor="center")

img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\profile.png")
img= img.subsample(13)

# Create a label with an image and text, and place it at the top left of the frame
user_id = Label(student_frame, text="get_user_name()", font=("Roboto", 14), bg='white', image=img, compound="left",padx=15, pady=10)
user_id.image = img
user_id.place(relx=0, rely=0, anchor='nw')

# Create a label with an image and text, and place it at the top left of the frame
user_id = Label(detail_frame, text="name", font=("Roboto", 14), bg='white', image=img, compound="left",padx=15, pady=10)
user_id.image = img
user_id.place(relx=0, rely=0, anchor='nw')

# Logout button
logout_button_frame = Frame(student_home_frame, bg="white")
logout_button_frame.place(relx=1, rely=0, anchor='ne')
create_btn(logout_button_frame, RIGHT, "Logout", lambda:("logout()"), button_color, "white", 14, 3, 25, btn_hover_color, button_color)

container_frame1 = Frame(student_home2_frame, bg="white", bd=0, relief="solid", highlightbackground=button_color, highlightthickness=1)
container_frame2 = Frame(student_home2_frame, bg="white", bd=0, relief="solid", highlightbackground=button_color, highlightthickness=1)

container_frame1.grid(row=0, column=1,sticky="nw",ipadx=140, ipady=110, pady=(50,0), padx=80)
container_frame2.grid(row=0, column=2, sticky="ne", ipadx=140, ipady=110, pady=(50,0), padx=80)

global show_assignment_img, plag_img, sub_assign_img, assign_img
show_assignment_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\assignment.png")
show_assignment_img = show_assignment_img.subsample(10)
show_assignment_logo_label = tk.Label(container_frame1, image=show_assignment_img, bg="white")
show_assignment_logo_label.place(relx=.5, rely=.45, anchor="s")
button_frame = Frame(container_frame1, bg="white")
button_frame.place(relx=.5, rely=.9, anchor='s')
create_btn(button_frame, 'bottom', "Show Assignments",lambda:(open_assignment_card_frame(), create_assignment_cards()), button_color, "white", 12, 7, 25, btn_hover_color, button_color)

show_marks_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\assignment.png")
show_marks_img = show_marks_img.subsample(10)
show_marks_logo_label = tk.Label(container_frame1, image=show_marks_img, bg="white")
show_marks_logo_label.place(relx=.5, rely=.45, anchor="s")
button_frame = Frame(container_frame2, bg="white")
button_frame.place(relx=.5, rely=.9, anchor='s')
create_btn(button_frame, 'bottom', "Show Marks",open_assignment_frame, button_color, "white", 12, 7, 25, btn_hover_color, button_color)


###############################  STUDENT FILE UPLOAD GUI  ###############################

student_upload_frame = Frame(root, bg="white")
# student_upload_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

student_frame = Frame(student_upload_frame, bg="white")
student_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\profile.png")
img= img.subsample(13)

# Create a label with an image and text, and place it at the top left of the frame
user_id = Label(student_frame, text="get_user_name()", font=("Roboto", 14), bg='white', image=img, compound="left",padx=15, pady=10)
user_id.image = img
user_id.place(relx=0, rely=0, anchor='nw')

# Create a label with an image and text, and place it at the top left of the frame
user_id = Label(detail_frame, text="name", font=("Roboto", 14), bg='white', image=img, compound="left",padx=15, pady=10)
user_id.image = img
user_id.place(relx=0, rely=0, anchor='nw')

# Logout button
back_button_frame = Frame(student_upload_frame, bg="white")
back_button_frame.place(relx=1, rely=0, anchor='ne')
create_btn(back_button_frame, RIGHT, "Back", open_student_home_frame, button_color, "white", 14, 3, 25, btn_hover_color, button_color)

st_upload_pdf_frame = Frame(student_frame, bg="white", padx=100, pady=100)
st_upload_pdf_frame.place(relx=.5, rely=.5, anchor="center")

st_label_frame = Frame(st_upload_pdf_frame, bg="white")
st_label_frame.grid(row=0, column=0)

st_label = Label(st_label_frame, text=f"FOR Subject", font=("Roboto", 18, "bold", "underline"), bg="white", fg=button_color)
st_label.grid(row=0, column=0, pady=(0,20))

st_sel_upl_btn_frame = Frame(st_upload_pdf_frame, bg="white")
st_sel_upl_btn_frame.grid(row=1, column=0)

create_btn(st_sel_upl_btn_frame, LEFT, "Select Files", select_files, button_color, "white", 14, 5, 40, btn_hover_color, button_color)
create_btn(st_sel_upl_btn_frame, RIGHT, "Upload Files", lambda:(upload_files(), "close_select_files_gui(), dynamic_label()"), "white", button_color, 14, 5, 40, btn_hover_white, "white")

st_label = Label(st_label_frame, text="Note: Pdf's name should be the name of the students", font=("Roboto", 12,), bg="white", fg=button_color)
st_label.grid(row=2, column=0, pady=(0,20))




root.mainloop()