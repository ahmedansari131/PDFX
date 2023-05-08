import copy
import difflib
import math
import os
import random
from re import X
import tkinter as tk
from tkinter import TOP, VERTICAL, Y, Canvas, Image, Text, Tk, filedialog, messagebox, Frame, Label, Entry, Button, LEFT, RIGHT, BOTH, END
from tkinter import ttk
from tkinter.font import Font
from db_connect import *
import pytesseract
import PyPDF2
import ftplib



###############################  COLORS VARIABLE  ###############################
bg_color = "#f2f2f3"
label_color = "#1B1212"
button_color = "#003151"
btn_hover_color = "#004d80"
btn_hover_white = "#C6E6FB"
btn_color = "#003151"
success = "#3bb54a"
error = "#ff3333"

global user_who
user_who = ""
global code_entered
code_entered = ""
allPDF = {}
assign_details = {}
# plag = {}
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
sh_assign = False
path_list = []
# plagiarism = []
# mark = []
# comp_plag = {}
# is_joined_sec = False
global is_created_sec
is_created_sec = False
joined_team_name = []
teamname = ""

# FTP server settings
server_address = '127.0.0.1'
username = 'pdfx'
password = 'Mohammad#131#'

root = tk.Tk()
root.iconbitmap(r"C:\Users\ANSHARI\Downloads\Python project\pdfx1-02.ico")
root.title("PDFX")
# root.geometry("1980x1080")
root.resizable(False, False)

# Centering the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (1500/2))
y_cordinate = int((screen_height/2) - (810/2))
root.geometry("{}x{}+{}+{}".format(1500, 810, x_cordinate, y_cordinate))

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

def open_login_frame():
    main_frame.pack_forget()
    signup_frame.place_forget()
    login_frame.place(relx=.5, rely=.5, anchor="center")
    # dialog_frame.place_forget()

def close_login_frame():
    login_frame.place_forget()

def open_signup_frame():
    main_frame.pack_forget()
    login_frame.place_forget()
    signup_frame.place(relx=.5, rely=.5, anchor="center")
    # dialog_frame.place_forget()

def clear_signup_form():
    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    c_pass_entry.delete(0, tk.END)

def clear_create_team_form():
    team_name.delete(0, tk.END)
    team_subject_name.delete(0, tk.END)
    team_teacher_name.delete(0, tk.END)

def clear_login_form():
    login_user_entry.delete(0, tk.END)
    login_pass_entry.delete(0, tk.END)

def open_create_team_modal():
    modal_frame.place(relx=.5, rely=.5, anchor="center", width=1000, height=600)

def open_home_frame():
    home_main_frame.pack(fill=BOTH, expand=True)

def open_options_panel(event, team_card_name_label):
    global clicked_team_name, no_assignment_label, user_who
    home2_frame.place(relx=0, rely=.5, anchor="w")
    create_team_btn.grid_forget()
    create_join_btn.grid_forget()
    my_team_cards_frame.place_forget()
    joined_team_cards_frame.place_forget()
    left_frame.grid(row=0, column=0, sticky="n",pady=100, padx=(40,60))
    right_frame.grid(row=0, column=1, sticky="w")
    create_back_btn.grid_forget()
    global is_created_sec
    is_created_sec = True
    team_detail_frame = event.widget
    team_card_name = [w for w in team_detail_frame.winfo_children() if w.winfo_name() == "team_card_name"][0]
    clicked_team_name = team_card_name.cget("text")
    team_card_name_label.config(text=clicked_team_name)
    print(clicked_team_name)
    join_welcome_label.place_forget()
    welcome_label.config(text=f"Welcome to {clicked_team_name} team", anchor="e")
    assignment_label.grid(row=0, column=0, sticky="nsew", pady=(0,40), ipadx=30, ipady=8)
    plagiarism_label.grid(row=2, column=0, sticky="nsew", ipadx=30, ipady=8)
    back_btn.place(relx=.83, rely=.04)
    show_assignment_btn.place_forget()
    create_assignment_btn.place_forget()
    select_file_btn.place_forget()
    upload_file_btn.place_forget()
    create_assign_heading.place_forget()
    assignment_frame.place_forget()
    assign_heading.place_forget()
    try:
        for frame in uploaded_work_frames:
            frame.destroy()  # or frame.pack_forget()
        no_assignment_label.place_forget()
    except:
        print("error occured")
    update_assignment_cards()
    welcome_label.place(relx=.5, rely=.56, anchor="center")
    welcome.place(relx=.5, rely=.42, anchor="center")
    assignment_card_frame.place_forget()
    work_heading.place_forget()
    team_code_label.grid(row=0, column=1, padx=(15,50))
    try:
        query = (f"SELECT code FROM create_teams WHERE teamname = '{clicked_team_name}' and username = '{user_who}'")
        mycursor.execute(query)
        print("This is query",query)
        # Get the result of the query
        result = mycursor.fetchone()
        teamcode = list(result)
        print("This is details corresponding to the code", teamcode[0])
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    team_code_label.config(text=f'Code: {teamcode[0]}')
    max_marks_frame.place_forget()

def close_create_join_btn():
    my_teams_btn.place_forget()
    joined_teams_btn.place_forget()

def open_joined_team_card():
    global user_who
    join_user_label.config(text=user_who)
    join_user_label.grid(row=0, column=0, padx=(15,50))
    joined_team_cards_frame.place(x=0, y=0, width=screen_width, height=screen_height)

def back_joined_team():
    joined_team_cards_frame.place(x=0, y=0, width=screen_width, height=screen_height)
    create_back_btn.grid(row=0, column=1, padx=(15,50))
    user_label.grid(row=0, column=0, padx=(15,50))

def open_my_team_card():
    global user_who
    my_team_cards_frame.place(x=0, y=0, height=screen_height, width=screen_width)
    create_back_btn.grid(row=0, column=1, padx=(15,50))
    user_label.config(text=user_who)
    user_label.grid(row=0, column=0, padx=(15,50))
    team_code_label.grid_forget()
    clear_table(table)
    table.place_forget()

def close_joined_team_card():
    joined_team_cards_frame.place_forget()

def close_my_team_card():
    my_team_cards_frame.place_forget()

def show_back_btn():
    create_back_btn.grid(row=0, column=1, padx=(15,50))
    user_label.grid(row=0, column=0, padx=(15,50))
    create_join_btn.grid_forget()
    create_team_btn.grid_forget()

def hide_back_btn():
    user_label.grid_forget()
    create_back_btn.grid_forget()
    create_team_btn.grid(row=0, column=0)
    create_join_btn.grid(row=0, column=1, padx=(15,50))
    my_teams_btn.place(relx=.4, rely=.5, anchor="center")
    joined_teams_btn.place(relx=.6, rely=.5, anchor="center")
    my_team_cards_frame.place_forget()
    joined_team_cards_frame.place_forget()
    not_joined_home_label.place_forget()
    not_created_home_label.place_forget()
    create_logout_btn.grid(row=0, column=2, padx=(20,80))
    join_user_label.grid_forget()

def logout():
    global team_detail_frame, team_card_frame, my_team_cards_frame
    home_main_frame.pack_forget()
    main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
    for frame in my_team_cards_frame.winfo_children():
        frame.destroy()
    joined_team_cards_frame.pack_forget()
    for frame in joined_team_cards_frame.winfo_children():
        frame.destroy()
    joined_team_cards_frame.pack_forget()

def close_logout_btn():
    create_logout_btn.grid_forget()


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

def close_team_modal():
    modal_frame.place_forget()

def open_join_team_modal():
    join_modal_frame.place(relx=.5, rely=.5, anchor="center", width=500, height=300)
    print("Open it")

def close_join_modal():
    join_modal_frame.place_forget()

def open_join_options_panel(event, team_card_name_label):
    global clicked_team_name
    join_home2_frame.place(relx=0, rely=.5, anchor="w")
    join_show_assign_label.grid(row=0, column=0, sticky="nsew", pady=(0,40), ipadx=40, ipady=8, padx=40)
    # join_marks_label.grid(row=2, column=0, sticky="nsew", ipadx=30, ipady=8, padx=40)
    join_back_btn.place(relx=.83, rely=.04)
    assignment_label.grid_forget()
    plagiarism_label.grid_forget()
    welcome_label.place_forget()
    welcome.place_forget()
    back_btn.place_forget()
    create_back_btn.grid_forget()
    close_joined_team_card()
    team_detail_frame = event.widget
    team_card_name = [w for w in team_detail_frame.winfo_children() if w.winfo_name() == "team_card_name"][0]
    clicked_team_name = team_card_name.cget("text")
    team_card_name_label.config(text=clicked_team_name)
    print(clicked_team_name)
    join_welcome_label.config(text=f"Welcome to {clicked_team_name} team", anchor="e")
    join_show_assignment_btn.place_forget()
    join_assign_heading.place_forget()
    join_assignment_card_frame.place_forget()
    join_welcome_label.place(relx=.5, rely=.5, anchor="center")
    no_join_assignment_label.place_forget()
    join_uploaded_work.place_forget()
    join_work_heading.place_forget()
    join_select_file_btn.place_forget()
    join_upload_file_btn.place_forget()

###############################  CREATING THE TEAM  ###############################
def create_team():
    global t_name
    t_name = team_name.get()
    sub_name = team_subject_name.get()
    te_name = team_teacher_name.get()
    desc = "Description"
    # user_name = "username"
    team_code = int(round(random.uniform(10000, 50000), 0))
    global db_name
    db_name = "create_teams"

    if t_name == "":
        dialog_box("Enter the team name", close_dialog_box, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif sub_name == "":
        dialog_box("Enter the subject name", close_dialog_box, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif te_name == "":
        dialog_box("Enter the professor name", close_dialog_box, error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    try:
        if t_name != None and sub_name != None and te_name != None:

            mycursor.execute("INSERT INTO {} (username, teamname, subname, profname, description, code) VALUES (%s, %s, %s, %s, %s, %s)".format(db_name), (user_who, t_name, sub_name, te_name, desc, team_code))
            mydb.commit()

            dialog_box(f"Your team has been created\nTeam code is {team_code}", lambda:(close_dialog_box()) , success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
            clear_create_team_form()
        else:
            messagebox.showerror("Some other error")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

###############################  JOINING THE TEAM  ###############################
def join_team():
     db_name = "create_teams"
     code_entered = code_show()
     try:
        # Execute a SELECT query to check if the username and password exist in the database
        query = (f"SELECT username, teamname, subname, profname, description, code FROM {db_name} WHERE code = '{code_entered}'")
        mycursor.execute(query)
        print("This is query",query)
        # Get the result of the query
        result = mycursor.fetchone()
        print("This is details corresponding to the code", result)
        dialog_box("You have joined the team", close_dialog_box, success, "white", "white", r"C:\Users\ANSHARI\Downloads\Python project\check.png")
     except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

     def create_joining_team_card():
        res = []
        res.append(result)
        print("This is list of tuples",res)

        # Inserting data of joined team corresponding to the username (loggedin)
        try:
            mycursor.execute("INSERT INTO {} (username, teamname, subname, code) VALUES (%s, %s, %s, %s)".format("team_joined"), (user_who, res[0][1], res[0][2], res[0][5]))
            # Commit the changes to the database
            mydb.commit()
        
        except mysql.connector.Error as e:
            print(f"The error '{e}' occurred")
     create_joining_team_card()


def fetch_all_teams_joined():
    global joined_team_names, team_card_name
    try:
        display_teams_query = (f"SELECT teamname, subname FROM team_joined WHERE username = '{user_who}'")
        print(display_teams_query)
        mycursor.execute(display_teams_query)
        # Get the result of the query
        display_joined_teams_result = mycursor.fetchall()
        print("Joined teams", display_joined_teams_result)
        print(len(display_joined_teams_result))
        joined_team_cards_frame.config(bg=button_color)

        if display_joined_teams_result:
            not_joined_home_label.place_forget()
            row_index = 0
            for i in range(0,len(display_joined_teams_result)):
                    # global join_team_card_frame
                    if i % 4 == 0 and i != 0:
                        row_index += 1
                    join_team_card_frame = Frame(joined_team_cards_frame, bg="white", width=240, height=240)
                    join_team_card_frame.grid(row=row_index, column=i%4, pady=(160 if row_index == 0 else 90,0), padx=63, sticky="nsew")
                    team_card = Frame(join_team_card_frame, bg="white", width=250, height=250, highlightthickness=3, highlightcolor="white", relief="groove", highlightbackground="#40bbec",  cursor="hand2")
                    team_card.pack()

                    team_detail_frame = Frame(team_card, bg="white", width=240, height=240)
                    team_detail_frame.place(relx=.5, rely=.5, anchor="center")

                    team_card_name = Label(team_detail_frame, bg="white", text=display_joined_teams_result[i][0], font=("roboto", 20, "bold"), fg=button_color, name="team_card_name")
                    team_card_name.place(relx=.5, rely=.44, anchor="center")

                    team_card_subname = Label(team_detail_frame, bg="white", text=display_joined_teams_result[i][1], font=("roboto", 15), fg=button_color)
                    team_card_subname.place(relx=.5, rely=.63, anchor="center")

                    joined_team_name.append(display_joined_teams_result[i][0])
                    team_detail_frame.bind("<Button>", lambda event, name=team_card_name: open_join_options_panel(event, name))
        else:
            not_joined_home_label.place(relx=.5, rely=.48, anchor="center")
        
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")



###############################  FETCH THE CREATED TEAM DETAIL CORRESPONDING TO USERNAME  ###############################
def fetch_teams():
    global team_card_name, team_card_subname, team_detail_frame, team_card_frame
    db_name = "create_teams"
    try:
        # Execute a SELECT query to check if the username and password exist in the database
        query = (f"SELECT teamname, subname FROM {db_name} WHERE username = '{user_who}'")
        mycursor.execute(query)
        print("This is query",query)
        # Get the result of the query
        display_teams_result = mycursor.fetchall()
        print("This is details corresponding to username", display_teams_result)

        # If the result is not empty, the user is logged in


        if display_teams_result:
            my_team_cards_frame.place(x=0, y=0, height=screen_height, width=screen_width)
            my_team_cards_frame.config(bg=button_color)
            row_index = 0
            for i in range(len(display_teams_result)):
                global team_card_frame
                if i % 4 == 0 and i != 0:
                    row_index += 1
                team_card_frame = Frame(my_team_cards_frame, bg=button_color, width=240, height=240)
                team_card_frame.grid(row=row_index, column=i%4, pady=(160 if row_index == 0 else 90,0), padx=63, sticky="nsew")
                
                team_card = Frame(team_card_frame, bg="white", width=250, height=250, highlightthickness=3, highlightcolor="white", relief="groove", highlightbackground="#40bbec", cursor="hand2")
                team_card.pack()

                team_detail_frame = Frame(team_card, bg="white", width=240, height=240)
                team_detail_frame.place(relx=.5, rely=.5, anchor="center")

                team_card_name = Label(team_detail_frame, bg="white", text=display_teams_result[i][0], font=("roboto", 20, "bold"), fg=button_color, name="team_card_name")
                team_card_name.place(relx=.5, rely=.44, anchor="center")

                team_card_subname = Label(team_detail_frame, bg="white", text=display_teams_result[i][1], font=("roboto", 15), fg=button_color)
                team_card_subname.place(relx=.5, rely=.63, anchor="center")

                team_detail_frame.bind("<Button>", lambda event, name=team_card_name: open_options_panel(event, name))
        else:
            not_created_home_label.place(relx=.5, rely=.48, anchor="center")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

###############################  sIGNUP LOGIC  ###############################
def signup_form(db_name):
    global name
    name = user_entry.get()
    password = pass_entry.get()
    confirm_password = c_pass_entry.get()

    if name == "":
        dialog_box("Enter your name", lambda:(open_signup_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif password == "":
        dialog_box("Enter the password", lambda:(open_signup_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif len(password) < 8:
        dialog_box("Password must be at least 8 characters", lambda:(open_signup_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
    elif password != confirm_password:
        dialog_box("Password do not match", lambda:(open_signup_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    try:
        if password == confirm_password and name != None and password != None and confirm_password != None:
            # Execute an INSERT query to add the new user to the database
            # print(db_name)
            mycursor.execute("INSERT INTO {} (username, password) VALUES (%s, %s)".format(db_name), (name, password))
            # Commit the changes to the database
            mydb.commit()

            dialog_box("Registered successfully!", lambda:(close_dialog_box(), open_login_frame()) , success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
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
    # print("User name is",name)
    # print(password)
    try:
        # Execute a SELECT query to check if the username and password exist in the database
        query = ("SELECT * FROM {} WHERE username = %s AND password = %s".format(db_name))
        mycursor.execute(query, (name, password))

        # Get the result of the query
        result = mycursor.fetchone()
        # print(result)

        # If the result is not empty, the user is logged in
        if result:
            dialog_box("You are loggedin!", lambda:(close_dialog_box(), clear_login_form(), open_home_frame()), success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
            global te_loggedin
            te_loggedin = True
            global user_who
            user_who =name

        elif len(name) == 0:
            dialog_box("Enter the details", lambda:(open_login_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
        elif len(password) == 0:
            dialog_box("Enter the details", lambda:(open_login_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")
        else:
            dialog_box("Incorrect Credentials", lambda:(open_login_frame(), close_dialog_box()), error, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\close.png")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")


def fetch_team_detail():
    try:
        team_dict = {}
        # Execute a SELECT query to check if the username and password exist in the database
        db_name = "create_teams"
        query = (f"SELECT * FROM {db_name} where username = '{user_who}' ")
        mycursor.execute(query) 

        # Get the result of the query
        result = mycursor.fetchall()
        # print(result)

        team_dict["team name"] = result[0][1]
        # print(team_dict)  
        joined_team_cards_frame.config(bg="white")

        my_team_cards_frame.config(bg="white")

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    except:
        # If the result is not empty, the user is logged in
        if result:
            print("Result is true")
            # middle_home_label.place_forget()
            # user_id.place_forget()
        else:
            joined_team_cards_frame.config(bg="white")
            print("No teams joined or created")
            # middle_home_label.place(relx=.5, rely=.55, anchor="center")
            # user_id.place(relx=.5, rely=.44, anchor="center")


###############################  SELECT FILE LOGIC  ###############################
def select_files():
    if te_loggedin:
         file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
         path_list.extend(file_paths)
         for path in file_paths:
            print("Selected file:", path)
            pdf_name = os.path.basename(path)
            pdf_name = os.path.splitext(pdf_name)[0]
            allPDF[pdf_name] = path
            print(allPDF)
            print(pdf_name)
    else:
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        pdf_name = os.path.basename(file_path)
        pdf_name = os.path.splitext(pdf_name)[0]
        allPDF[pdf_name] = file_path
        print(allPDF)


###############################  UPLOADING PDF LOGIC  ###############################
def upload_files():
    if len(path_list) == 0:
        print("No files selected!")
        return

    print("Uploading files...")
    for path in path_list:
        print("File path:", path)

    path_list.clear()
    print("Upload complete!")
    calc_plag()
    print("This is file path", allPDF.values())
 
    if len(allPDF.values()) == 0:
        print("No files selected!")
        return
        
    allPDF.clear()
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
    # print("This is entire text",entireTxt)
    return entireTxt

def get_max_marks():
    global marks
    marks = max_marks_entry.get()
    return marks

############################### CALCULATING THE PLAGIARISM  ###############################
def calc_plag():
    global user_who, marks
    plag = {}
    entireTxt = entire_text()
    for file1, txt1 in entireTxt.items():
        for file2, txt2 in entireTxt.items():
            if file1 < file2:
                seq = difflib.SequenceMatcher(None, txt1, txt2)
                similarity_ratio = seq.ratio()

                plag[file1, file2] = round(similarity_ratio*100, 2)

                if similarity_ratio > 0.8:  # adjust the threshold as needed
                    print(f"{file1} and {file2} have a high plagiarism: {round(similarity_ratio*100, 2)} %\n")
                else:
                    print(f"{file1} and {file2} has plagiarism: {round(similarity_ratio*100, 2)} %\n")

    plag_values = plag.values()
    global plag_values_list 
    plag_values_list = list(plag_values)
    print("This is plag",plag)

    def dynamic_label():
        max_marks = 0
        plagiarism = []
        mark = []
        comp_plag = {}
        pdf_list = list(allPDF)
        print("this pdf list", pdf_list)
        length_of_pdf = len(pdf_list)

        for first_key, value in plag.items():
              first_char = first_key[0]
              sec_char = first_key[1]

              if first_char in comp_plag:
                print("I am comp plag", comp_plag)
                comp_plag[first_char].append(value)
                if sec_char in comp_plag:
                    comp_plag[sec_char].append(value)
                else:
                    comp_plag[sec_char] = [value]
                print("Value appended", comp_plag)
              else:
                comp_plag[first_char] = [value]
                if sec_char in comp_plag:
                    comp_plag[sec_char].append(value)
                else:
                    comp_plag[sec_char] = [value]

        print("This is new dictionary", comp_plag)
        i = 0
        for key, value in comp_plag.items():
            greatest_value = max(value)
            print(f"The greatest value in the list {key} is {greatest_value}.")
            plagiarism.append(greatest_value)
        print("Plagiarism Found", plagiarism)
        table.place(relx=.475, rely=.5, anchor="center", height=500)
        max_marks = int(get_max_marks())
        print("I am max marks", type(max_marks))
        for i in range(0, length_of_pdf):
            if 0.0 <= plagiarism[i] <= 21.0:
                marks = int(max_marks)
            elif 21.0 <= plagiarism[i] <= 41.0:
                marks = int(max_marks * 0.75)
                # print(marks)
            elif 41.0 <= plagiarism[i] <= 61.0:
                marks = int(max_marks * 0.5)
                # print(marks)
            elif 61.0 <= plagiarism[i] <= 81.0:
                marks = int(max_marks * 0.25)
                # print(marks)
            elif 81.0 <= plagiarism[i] <= 101.0:
                marks = int(max_marks * 0.1)
            mark.append(marks)
            print("Marks are:", mark)
        for i, key in enumerate(allPDF.keys()):
            print(key)

            try:
                table.insert(parent='', index='end', iid=i, text=f"{i+1}.", values=(f"{key} {plagiarism[i]} {mark[i]}/{max_marks}"))
                mycursor.execute(f"INSERT INTO assignment_marks (teamname, username, pdf_name, plagiarism, marks, total_marks) VALUES (%s, %s, %s, %s, %s, %s)", (clicked_team_name, user_who, key, plagiarism[i], mark[i], max_marks))
                print("Data inserted")
                mydb.commit()
                print("This is i", i)
            except:
                table.insert(parent='', index='end', iid=i, text=f"{i+1}.", values=(f"{key} {plagiarism[i]} {mark[i]}/{max_marks}"))
                mycursor.execute(f"INSERT INTO assignment_marks (teamname, username, pdf_name, plagiarism, marks, total_marks) VALUES (%s, %s, %s, %s, %s, %s)", (clicked_team_name, user_who, key, plagiarism[i], mark[i-1], max_marks))
                print("This is except i", i)
                print("Except")
        comp_plag.clear()
    dynamic_label()

def clear_table(table):
    # Delete all existing rows in the table
    table.delete(*table.get_children())
    print("cleared")

###############################  SELECT FILE LOGIC  ###############################
def join_select_files():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        print("Selected file:", file_path)
        pdf_name = os.path.basename(file_path)
        pdf_name = os.path.splitext(pdf_name)[0]
        allPDF[pdf_name] = file_path
        print(allPDF)

###############################  JOINED UPLOADING PDF LOGIC  ###############################
def joined_upload_files():
    global file_path, clicked_team_name, clicked_assign_name
    if len(file_path) == 0:
        print("No files selected!")
        return
    print("Uploading files...")

    # Connect to the FTP server
    ftp = ftplib.FTP(server_address)
    ftp.login(username, password)

    with open(file_path, 'rb') as file:
        filename = os.path.basename(file_path)
        ftp.storbinary('STOR ' + filename, file)
        print("File uploaded:", filename)
        file_path_on_server = file_path             
        try:
            # file_abs_path = os.path.abspath(file_path)
            # Execute an INSERT query to add the new user to the database  
            mycursor.execute(f"INSERT INTO submitted_assignments (teamname, assign_name, username, filename, filepath) VALUES (%s, %s, %s, %s, %s)", (clicked_team_name, clicked_assign_name, user_who, filename, file_path_on_server))
            # Commit the changes to the database
            mydb.commit()
        except mysql.connector.Error as e:
             print(f"The error '{e}' occurred")

    # Close the FTP connection
    ftp.quit()

    path_list.clear()
    print("Upload complete!")
    # print("This is file path", allPDF.values())

    if len(allPDF.values()) == 0:
        print("No files selected!")
        return

    allPDF.clear()
    dialog_box("Files are uploaded", close_dialog_box, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
    print("Executed")

###############################  MAIN FRAME  ###############################
main_frame = tk.Frame(root, bg="white")
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

main_title = Label(title_frame, text="Login or signup to proceed with the app", font=("Roboto", 15), bg="white", fg=label_color)
main_title.pack(pady=10)

button_frame = Frame(title_frame, bg="white")
button_frame.pack()

create_btn(button_frame, LEFT, "Login", lambda: (open_login_frame()), button_color, "white", 12, 7, 30, btn_hover_color, button_color)
create_btn(button_frame, RIGHT, "Signup", lambda: (open_signup_frame()), button_color, "white", 12, 7, 30, btn_hover_color, button_color)


# Create the login frame
login_frame = Frame(root, bg="white", padx=50, pady=40)

# small_title_label = Label(login_frame, text= "Teacher sign in", font=("Roboto", 12, "underline"), bg="white", fg="#003d66", anchor="w")
# small_title_label.pack(pady=(0, 20))

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

create_btn(login_button_frame, RIGHT, "Login", lambda:(validate_login("te_signup"), close_login_frame(),  fetch_team_detail()),button_color, "white", 14, 5, 40, btn_hover_color, button_color)
create_btn(login_button_frame, LEFT, "Signup", open_signup_frame, "white", button_color, 14, 5, 40, "#FAF9F6", "white")



###############################  SIGNUP FRAME  ###############################
signup_frame = Frame(root, bg="white", padx=50, pady=40)

# small_title_label = Label(signup_frame, text= "Teacher registration", font=("Roboto", 12, "underline"), bg="white", fg="#003d66", anchor="w")
# small_title_label.pack(pady=(0, 20))

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

create_btn(button_frame, LEFT, "Signup", lambda:signup_form("te_signup"), button_color, "white", 14, 5, 40, btn_hover_color, button_color)
create_btn(button_frame, LEFT, "Login", open_login_frame, "white", button_color, 14, 5, 40, "#FAF9F6", "white")



###############################  HOME MAIN FRAME  ###############################
home_main_frame = tk.Frame(root, bg="white")
# home_main_frame.pack(fill=BOTH, expand=True)

home_sub_frame = Frame(home_main_frame, bg="white", width=screen_width, height=screen_height)
home_sub_frame.place(x=0,y=0)

my_team_cards_frame = Frame(home_sub_frame, bg=button_color, width=screen_width, height=screen_height)
my_team_cards_frame.place(x=0, y=0, width=screen_width, height=screen_height)

joined_team_cards_frame = Frame(home_sub_frame, bg=button_color, width=screen_width, height=screen_height)
joined_team_cards_frame.place(x=0, y=0, width=screen_width, height=screen_height)

home_menu_frame = Frame(home_sub_frame, bg=button_color, height=70, width=screen_width)
home_menu_frame.place(x=0, y=0, width=screen_width)

logo_label = Label(home_menu_frame, text="PDFX", font=("Roboto", 30, "bold"), bg=button_color, fg="white")
logo_label.place(relx=.1, rely=.5, anchor="center")

global white_logo
white_logo = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\white-logo.png")
white_logo = white_logo.subsample(5)
white_logo_label = Label(home_menu_frame, image= white_logo, bg=button_color)
white_logo_label.place(relx=.05, rely=.5, anchor="center")

button_frame = Frame(home_menu_frame, bg=button_color, width=300, height=50)
button_frame.place(relx=.84, rely=.5, anchor="center")

create_team_btn = Button(button_frame, text="Create team", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2",command=lambda:(open_create_team_modal()))
create_team_btn.grid(row=0, column=0)

create_join_btn = Button(button_frame, text="Join team", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2",command=open_join_team_modal)
create_join_btn.grid(row=0, column=1, padx=(15,10))

create_back_btn = Button(button_frame, text="Back", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2",command=hide_back_btn)

create_logout_btn = Button(button_frame, text="Logout", padx=25, pady=5, bg=button_color, fg="white", bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 14, "bold"), cursor="hand2",command=logout)
create_logout_btn.grid(row=0, column=2, padx=(20,80))

# global user_img
user_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\user (3).png")
user_img= user_img.subsample(15)
user_label = Label(button_frame, text="username", fg="white", bg=button_color, font=("roboto", 14, "bold"), compound=LEFT, image=user_img, padx=15)
user_label.image = user_img

team_code_label = Label(button_frame, text="team code", fg=button_color, bg="white", font=("roboto", 14), padx=15, pady=5)

not_created_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\add-friend.png")
not_created_img= not_created_img.subsample(7)
not_created_home_label = Label(home_sub_frame, text="You have not created any team yet", font=("Roboto", 28, "bold"), bg=button_color, fg="white", image=not_created_img, compound=TOP, pady=20)
not_created_home_label.image = not_created_img


not_joined_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\meeting.png")
not_joined_img= not_joined_img.subsample(7)
not_joined_home_label = Label(home_sub_frame, text="You have not joined any team yet", font=("Roboto", 28, "bold"),bg=button_color, fg="white", image=not_joined_img, compound=TOP, pady=20)
not_created_home_label.image = not_joined_img


my_team_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\myteam (1).png")
my_team_img= my_team_img.subsample(8)

joined_team_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\joinedteam.png")
joined_team_img= joined_team_img.subsample(8)

my_teams_btn = Button(home_sub_frame, text="My teams", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 20, "bold"), cursor="hand2", compound=LEFT, image=my_team_img, command=lambda:(close_create_join_btn(), fetch_teams(), show_back_btn(), close_joined_team_card(), open_my_team_card(), close_logout_btn()))
my_teams_btn.place(relx=.4, rely=.5, anchor="center")

joined_teams_btn = Button(home_sub_frame, text="Joined teams", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 20, "bold"), cursor="hand2", compound=LEFT, image=joined_team_img, command=lambda:(fetch_all_teams_joined(), close_create_join_btn(), show_back_btn(), close_my_team_card(), open_joined_team_card(), close_logout_btn()))
joined_teams_btn.place(relx=.6, rely=.5, anchor="center")

global home2_frame
home2_frame = Frame(home_sub_frame, bg=button_color, width=screen_width, height=screen_height-140)
join_home2_frame = Frame(home_sub_frame, bg=button_color, width=screen_width, height=screen_height-140)
# home2_frame.place(relx=.5, rely=.5, anchor="center")

join_user_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\user (3).png")
join_user_img= join_user_img.subsample(15)
join_user_label = Label(button_frame, text="user_who", fg="white", bg=button_color, font=("roboto", 14, "bold"), compound=LEFT, image=join_user_img, padx=15)
join_user_label.image = join_user_img

join_left_frame = Frame(join_home2_frame, bg=button_color, height=screen_height-140)
join_left_frame.grid(row=0, column=0, sticky="n",pady=100)

left_frame = Frame(home2_frame, bg=button_color, height=screen_height-140)
left_frame.grid(row=0, column=0, sticky="n",pady=100)

join_right_frame = Frame(join_home2_frame, bg="white", width=screen_width-255, height=screen_height-140)
join_right_frame.grid(row=0, column=1, sticky="w")

right_frame = Frame(home2_frame, bg="white", width=screen_width-255, height=screen_height-140)
right_frame.grid(row=0, column=1, sticky="w")
# uploaded_work = Frame(right_frame, bg=button_color, padx=30, pady=15)


assignment_label = Label(left_frame, text="Assignments", font=("Roboto", 15), bg="white", fg=button_color, anchor="center", cursor="hand2")
assignment_label.grid(row=0, column=0, sticky="nsew", pady=(0,40), ipadx=30, ipady=8)
assignment_label.bind("<Button-1>", lambda event: (assign_label_clicked()))

plagiarism_label = Label(left_frame, text="Plagiarism", font=("Roboto", 15), bg="white", fg=button_color, anchor="center", cursor="hand2")
plagiarism_label.grid(row=2, column=0, sticky="nsew", ipadx=30, ipady=8)

welcome_label = Label(right_frame, text=f"Welcome to the team name", font=("Roboto", 25, "bold"), bg="white", fg=button_color)
welcome_label.place(relx=.5, rely=.56, anchor="center")
welcome_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\partners.png")
welcome_img= welcome_img.subsample(5)
welcome = Label(right_frame,  font=("Roboto", 14), bg="white", fg="white", image=welcome_img, compound="left", padx=20, cursor="hand2")
welcome.image = welcome_img
welcome.place(relx=.5, rely=.42, anchor="center")

back_btn = Button(right_frame, text="Back", padx=25, pady=5, bg=button_color, fg="white", bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 14, "bold"), cursor="hand2", command=lambda:(left_frame.grid_forget(), right_frame.grid_forget(), home2_frame.place_forget(), open_my_team_card(), my_teams_btn.place_forget(), joined_teams_btn.place_forget()))
back_btn.place(relx=.83, rely=.04)

special_back_btn = Button(right_frame, text="Back", padx=25, pady=5, bg="pink", fg="white", bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 14, "bold"), cursor="hand2", command=lambda:())

show_assignment_btn = Button(right_frame, text="Show assignments", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 15, "underline"), cursor="hand2", command=lambda:(open_assignment_cards()))

plus_icon = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\create.png")
plus_icon= plus_icon.subsample(10)

create_assignment_btn = Button(right_frame, text="Create assignments", padx=25, pady=10, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 23, "bold"),image=plus_icon, compound=LEFT, cursor="hand2", command=lambda:(open_assign_detail_form()))

select_icon = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\tap.png")
select_icon= select_icon.subsample(10)
select_file_btn = Button(right_frame, text="Select files", padx=25, pady=10, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 23, "bold"),image=select_icon, compound=LEFT, cursor="hand2", command=lambda:(select_files()))

upload_icon = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\uplaod.png")
upload_icon= upload_icon.subsample(12)
upload_file_btn = Button(right_frame, text="Upload files", padx=25, pady=10, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 23, "bold"),image=upload_icon, compound=LEFT, cursor="hand2", command=lambda:(upload_files(), select_file_btn.place_forget(), upload_file_btn.place_forget()))

max_marks_frame = Frame(right_frame, bg=button_color, padx=90, pady=30)

max_marks_label = Label(max_marks_frame, bg=button_color, fg="white", text="Enter the total marks", anchor="center", font=("roboto", 14))
max_marks_label.grid(row=0, column=0, sticky="nsew")

max_marks_entry = Entry(max_marks_frame, bg=button_color, fg="white", bd=0, highlightbackground="white", highlightthickness=1, font=("roboto", 12))
max_marks_entry.grid(row=1, column=0, sticky="nsew", ipady=5)

max_marks_btn = Button(max_marks_frame, bg="white", fg=button_color, padx=18, pady=3, text="Next",font=("roboto", 12, "bold"), cursor="hand2", command= lambda:(get_max_marks(), max_marks_frame.place_forget()))
max_marks_btn.grid(row=2, column=0, sticky="nsew", pady=(20,0))

###############################  JOIN OPTIONS SECTION ###############################
join_uploaded_work = Frame(join_right_frame, bg=button_color, padx=30, pady=15)
join_uploaded_file = Frame(join_uploaded_work, highlightbackground="white", highlightthickness=1, bg=button_color)
uploaded_work = Frame(right_frame, bg=button_color, padx=30, pady=15)
uploaded_file = Frame(uploaded_work, highlightbackground="white", highlightthickness=1, bg=button_color)
    
join_show_assign_label = Label(join_left_frame, text="Assignments", font=("Roboto", 15), bg="white", fg=button_color, anchor="center", cursor="hand2")
join_show_assign_label.bind("<Button-1>", lambda event: join_assign_label_clicked())

join_marks_label = Label(join_left_frame, text="Marks", font=("Roboto", 15), bg="white", fg=button_color, anchor="center", cursor="hand2")

join_back_btn = Button(join_right_frame, text="Back", padx=25, pady=5, bg=button_color, fg="white", bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 14, "bold"), cursor="hand2", command=lambda:(join_home2_frame.place_forget(), back_joined_team(), update_join_assignment_cards()))

join_welcome_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\partners.png")
join_welcome_img= join_welcome_img.subsample(7)
# join_welcome = Label(join_right_frame,  font=("Roboto", 14), bg="white", fg="white", image=join_welcome_img, compound="left", padx=20, cursor="hand2")
join_welcome_label = Label(join_right_frame, text=f"Welcome to the team", font=("Roboto", 25, "bold"), bg="white", fg=button_color, image=join_welcome_img, compound=TOP, pady=20)
join_welcome_label.image = join_welcome_img
join_welcome_label.place(relx=.5, rely=.5, anchor="center")

join_show_icon = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\visual.png")
join_show_icon= join_show_icon.subsample(9)
join_show_assignment_btn = Button(join_right_frame, text="Show assignments", padx=25, pady=20, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 23, "bold"),image=join_show_icon, compound=TOP, cursor="hand2", command=lambda:(open_join_assignment_cards(), create_join_assignment_cards()))

join_select_icon = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\tap.png")
join_select_icon= join_select_icon.subsample(10)
join_select_file_btn = Button(join_right_frame, text="Select files", padx=25, pady=10, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 23, "bold"),image=join_select_icon, compound=LEFT, cursor="hand2", command=lambda:(join_select_files()))

join_upload_icon = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\uplaod.png")
join_upload_icon= join_upload_icon.subsample(12)
join_upload_file_btn = Button(join_right_frame, text="Upload files", padx=25, pady=10, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 23, "bold"),image=join_upload_icon, compound=LEFT, cursor="hand2", command=lambda:(joined_upload_files(), select_file_btn.place_forget(), upload_file_btn.place_forget()))


###############################  CREATE ASSIGMENT DETAILS FORM ###############################

assignment_frame = Frame(right_frame, bg="white")
# assignment_frame.place(relx=.5, rely=5, anchor="center")

assign_form_frame = Frame(assignment_frame, bg="white")
assign_form_frame.place(relx=.5, rely=.55, anchor="center")

assignment_icon_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\online-survey.png")
assignment_icon_img= assignment_icon_img.subsample(8)

create_assign_heading = Label(assignment_frame, text="Create Assignment".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w", compound="left", image=assignment_icon_img, padx=20)
create_assign_heading.grid(row=0, column=0, sticky="nsew", pady=(0,80))

assign_name = Label(assignment_frame, text="Title",  font=("Roboto", 14, "bold"), bg="white", fg=button_color, anchor="w")
assign_name_entry = Entry(assignment_frame, font=("Roboto", 14), bg="#fff", fg=label_color, bd=0, highlightthickness=1, highlightbackground=button_color, highlightcolor=button_color)
assign_name.grid(row=2, column=0, sticky="w")
assign_name_entry.grid(row=3, column=0, ipady=8, ipadx=50, sticky="w")

subject_name = Label(assignment_frame, text="Subject",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
subject_name_entry = Entry(assignment_frame, font=("Roboto", 14), bg="#fff", fg=label_color, bd=0, highlightthickness=1, highlightbackground=button_color, highlightcolor=button_color)
subject_name.grid(row=2, column=1, sticky="w")
subject_name_entry.grid(row=3, column=1, sticky="w", ipady=8, ipadx=50)

t_marks = Label(assignment_frame, text="Total Marks",  font=("Roboto", 14, "bold"), bg="white", fg=button_color)
t_marks_entry = Entry(assignment_frame, font=("Roboto", 14), bg="white", fg=label_color, bd=0, highlightthickness=1, highlightbackground=button_color, highlightcolor=button_color)
t_marks.grid(row=4, column=0, sticky="w", pady=(40,0))
t_marks_entry.grid(row=5, column=0,ipady=8, ipadx=50,sticky="w")

submit_button = Button(assignment_frame, text="Next", font=("Roboto", 14, "bold"), bg=button_color, fg="white", bd=0, highlightthickness=0, cursor="hand2", command=lambda:(get_assignment_details(), "close_assignment_detail_frame(), create_assignment_cards(), clear_assignment_details()"))
submit_button.grid(row=6, column=1, ipadx=50, ipady=5, pady=(50,0), sticky="e")

submit_button.bind("<Enter>", lambda event: on_enter(event, btn_hover_color))
submit_button.bind("<Leave>", lambda event: on_leave(event, button_color))

plagiarism_label.bind("<Button-1>", lambda event: plag_label_clicked())

assignment_card_frame = Frame(right_frame, bg="white", height=650, width=screen_width-255,pady=40)
assign_card = Frame(assignment_card_frame, bg=button_color, padx=30, pady=15)

join_assignment_card_frame = Frame(join_right_frame, bg="white", height=650, width=screen_width-255,pady=40)
# assignment_card_frame.place(relx=.5, rely=.5, anchor="center")

assign_heading = Label(right_frame, text="Assignments".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w", padx=20)
join_assign_heading = Label(join_right_frame, text="Assignments".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w", padx=20)
join_work_heading = Label(join_right_frame, text="My work".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w", padx=20)
work_heading = Label(right_frame, text="Submitted assignments".upper(),  font=("Roboto", 25, "bold"), bg="white", fg=button_color, anchor="w", padx=20)

def open_assign_detail_form():
    assignment_frame.place(relx=.5, rely=.5, anchor="center")
    create_assignment_btn.place_forget()

def open_assignment_cards():
    create_assignment_btn.place_forget()
    assignment_card_frame.place(relx=.5, rely=.6, anchor="center")
    assign_heading.place(relx=0.035, rely=.08, anchor="w")
    create_assignment_cards()
    show_assignment_btn.place_forget()

def open_join_assignment_cards():
    join_assignment_card_frame.place(relx=.5, rely=.6, anchor="center")
    join_assign_heading.place(relx=0.035, rely=.08, anchor="w")
    join_show_assignment_btn.place_forget()

def join_upload_sec(event, join_assignment_label):
    global clicked_assign_name, clicked_team_name
    join_assignment_card_frame.place_forget()
    join_assign_heading.place_forget()
    join_select_file_btn.place(relx=.35, rely=.5, anchor="center")
    join_upload_file_btn.place(relx=.65, rely=.5, anchor="center")
    join_assign_card = event.widget
    clicked_assign_name = join_assignment_label.cget("text")
    join_assignment_label.config(text=clicked_assign_name)
    print(clicked_assign_name)
    try:
        print("This is assignment name: ",clicked_assign_name)
        query = (f"SELECT filename, filepath FROM submitted_assignments where assign_name = '{clicked_assign_name}' and teamname = '{clicked_team_name}' and username = '{user_who}'")
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(result)
        uploaded_file_path = result[0][1]
        def open_uploaded_pdf():
             os.startfile(uploaded_file_path, 'open')

        print(result)
        if result:
            print("Assignment already uploaded")
            join_upload_file_btn.place_forget()
            join_select_file_btn.place_forget()
            join_work_heading.place(relx=0.035, rely=.08, anchor="w")
            # join_uploaded_work = Frame(join_right_frame, bg=button_color, padx=30, pady=15)
            join_uploaded_work.place(relx=.05, rely=.2, width=1099, height=120)
            join_uploaded_file.place(relx=.5, rely=.5, anchor="center", width=1070, height=87)

            join_uploaded_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\pdf.png")
            join_uploaded_img = join_uploaded_img.subsample(16)
            join_uploaded_work_btn = Button(join_uploaded_file, text=result[0][0],  font=("Roboto", 15, "bold"), bg=button_color, fg="white", image=join_uploaded_img, compound=LEFT, cursor="hand2", padx=20, anchor="w", bd=0, highlightthickness=0, command=open_uploaded_pdf)
            join_uploaded_work_btn.image = join_uploaded_img
            join_uploaded_work_btn.place(relx=0, rely=.5, anchor="w", width=1068, height=84)
        else:
            print("Please upload assignment")
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

def assign_label_clicked():
    global uploaded_work_frames, no_assignment_label
    welcome.place_forget()
    welcome_label.place_forget()
    create_assignment_btn.place(relx=.5, rely=.5, anchor="center")
    show_assignment_btn.place(relx=.6, rely=.04)
    select_file_btn.place_forget()
    upload_file_btn.place_forget()
    assignment_frame.place_forget()
    assignment_card_frame.place_forget()
    assign_heading.place_forget()
    try:
        for frame in uploaded_work_frames:
            frame.destroy()  # or frame.pack_forget()
    except:
        print("error occured")
    work_heading.place_forget()
    special_back_btn.place_forget()
    back_btn.place(relx=.83, rely=.04)
    try:
        no_assignment_label.place_forget()
    except:
        print("error occured")
    table.place_forget()
    max_marks_frame.place_forget()

def join_assign_label_clicked():
    global join_uploaded_work, uploaded_work_frames, no_join_assignment_label
    join_welcome_label.place_forget()
    join_welcome_label.place_forget()
    join_show_assignment_btn.place(relx=.5, rely=.5, anchor="center")
    join_select_file_btn.place_forget()
    join_upload_file_btn.place_forget()
    assignment_frame.place_forget()
    join_assignment_card_frame.place_forget()
    join_assign_heading.place_forget()
    join_work_heading.place_forget()
    join_uploaded_work.place_forget()
    join_uploaded_file.place_forget()
    join_welcome_label.place_forget()
    try:
        no_join_assignment_label.place_forget()
    except:
        print("Error in join_assign_label_clicked")

def plag_label_clicked():
    global uploaded_work_frames, no_assignment_label
    welcome.place_forget()
    welcome_label.place_forget()
    select_file_btn.place(relx=.35, rely=.5, anchor="center")
    upload_file_btn.place(relx=.65, rely=.5, anchor="center")
    create_assignment_btn.place_forget()
    show_assignment_btn.place_forget()
    table.place_forget()
    assignment_frame.place_forget()
    assignment_card_frame.place_forget()
    assign_heading.place_forget()
    try:
        for frame in uploaded_work_frames:
            frame.destroy()  # or frame.pack_forget()
    except:
        print("I am in except")
    work_heading.place_forget()
    special_back_btn.place_forget()
    back_btn.place(relx=.83, rely=.04)
    try:
        no_assignment_label.place_forget()
    except:
        print("Except 2")
    clear_table(table)
    table.place_forget()
    max_marks_frame.place(relx=.5, rely=.5, anchor="center")

def get_assignment_details():
    global count_of_assignment, clicked_team_name  # declare the variable as global
    assign_title = assign_name_entry.get()
    subject = subject_name_entry.get()
    assign_total_marks = t_marks_entry.get()
    # assign_due_date = due_date_entry.get()

    teamname = clicked_team_name
    create_assign["assignment title"] = assign_title
    create_assign["subject"] = subject
    create_assign["marks"] = assign_total_marks
    # create_assign["due date"] = assign_due_date

    print(create_assign)
    print("This is before increment",count_of_assignment)

    if subject == "" and assign_title == "" and assign_total_marks == "":
        print("This is none")
        dialog_box("Enter the details", lambda:(close_dialog_box()), error, bg_color, "white", r"C:\Users\ANSHARI\Downloads\Python project\close.png")
        assignment_frame.place(relx=.5, rely=5, anchor="center")
    else:
        try:
            # Execute an INSERT query to add the new user to the database
            assign_table_name = "assignments"   
            mycursor.execute(f"INSERT INTO {assign_table_name} (teamname, assign_name, sub_name, total_marks) VALUES (%s, %s, %s, %s)", (teamname, create_assign['assignment title'], create_assign["subject"], create_assign["marks"]))
            # Commit the changes to the database
            mydb.commit()

            dialog_box("Assignment created successfullly!", close_dialog_box, success, bg_color, label_color, r"C:\Users\ANSHARI\Downloads\Python project\check.png")
            clear_assign_form()
        except mysql.connector.Error as e:
             print(f"The error '{e}' occurred")

        count_of_assignment = count_of_assignment + 1
        print("After increment",count_of_assignment)

        return create_assign
    
def clear_assign_form():
    assign_name_entry.delete(0, tk.END)
    subject_name_entry.delete(0, tk.END)
    t_marks_entry.delete(0, tk.END)
    # due_date_entry.delete(0, tk.END)

def create_assignment_cards():
    global uploaded_work_frames, no_assignment_label
    uploaded_work_frames = []
    global count_of_assignment, assign_card, clicked_uploaded_assign_name
    assignments = "assignments"
        
    def submitted_assignment(event, join_assignment_label):
        try:
            global clicked_uploaded_assign_name, uploaded_work
            clicked_uploaded_assign_name = join_assignment_label.cget("text")
            join_assignment_label.config(text=clicked_uploaded_assign_name)

            for widget in assignment_card_frame.winfo_children():
                    widget.destroy()
            query = (f"SELECT * FROM submitted_assignments where teamname = '{clicked_team_name}' and assign_name = '{clicked_uploaded_assign_name}'")
            mycursor.execute(query)
            submitted_result = mycursor.fetchall()
 
            if submitted_result:
                print("This is result you can see", submitted_result)
                work_heading.place(relx=0.035, rely=.08, anchor="w")
                uploaded_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\pdf.png")
                uploaded_img = uploaded_img.subsample(14)
                download_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\Asset 23ldpi.png")
                download_img = download_img.subsample(50)

                for i, result in enumerate(submitted_result, start=1):
                    print(result)
                    uploaded_work = Frame(right_frame, bg=button_color, padx=30, pady=15)
                    uploaded_work.place(relx=.05, rely=.2*i, width=1099, height=120)
                    uploaded_work_frames.append(uploaded_work)

                    uploaded_file = Frame(uploaded_work, highlightbackground="white", highlightthickness=1, bg=button_color)
                    uploaded_file.place(relx=.5, rely=.5, anchor="center", width=1070, height=87)

                    uploaded_work_frame = Frame(uploaded_file, bg=button_color,  padx=20, bd=0, highlightthickness=0)
                    uploaded_work_frame.place(relx=0, rely=.5, anchor="w", width=1068, height=84)

                    uploaded_work_student_name = Label(uploaded_work_frame, text=f"{result[3]}", bg=button_color, fg="white", font=("roboto", 15, "bold"), anchor="w", image=uploaded_img, compound=LEFT, pady=20, padx=10)
                    uploaded_work_student_name.grid(row=0, column=0, sticky="w")
                    uploaded_work_student_name.image = uploaded_img
                    
                    download_img_lable = Label(uploaded_work_frame, image=download_img, bg=button_color, cursor="hand2", anchor="e")
                    download_img_lable.grid(row=0, column=1, sticky="e", padx=(0, 15))
                    download_img_lable.image = download_img
                    uploaded_work_frame.columnconfigure(0, weight=1)
                    uploaded_work_frame.columnconfigure(1, weight=0)
                    download_img_lable.bind("<Button-1>", lambda event, filepath=result[3]: download_uploaded_file(filepath))

                def download_uploaded_file(filepath):
                    print(filepath)
                    local_folder_path = r"C:\Users\ANSHARI\Downloads\Python project\Downloaded PDFs"
                    if not os.path.exists(local_folder_path):
                        os.makedirs(local_folder_path)
                    ftp = ftplib.FTP(server_address)
                    ftp.login(username, password)
                    with open(os.path.join(local_folder_path, filepath), "wb") as f:
                        print("Path is", os.path.join(local_folder_path, filepath))
                        ftp.retrbinary(f"RETR {filepath}", f.write)
                        dialog_box("Downloaded successfully!", close_dialog_box, success, "white", "white", r"C:\Users\ANSHARI\Downloads\Python project\check.png")
                    ftp.quit()

                def close_uploaded_assign_section():
                    global create_assignment_btn
                    for frame in uploaded_work_frames:
                        frame.destroy()  # or frame.pack_forget()
                    work_heading.place_forget()
                    show_assignment_btn.place(relx=.6, rely=.04)
                    assign_heading.place_forget()
                    special_back_btn.place_forget()
                    back_btn.place(relx=.83, rely=.04)

        except mysql.connector.Error as e:
            print(f"The error '{e}' occurred")

    try:
        query = (f"SELECT * FROM {assignments} where teamname = '{clicked_team_name}'")
        mycursor.execute(query)
        result = mycursor.fetchall()
        print("This is result",result)
        print(result)
        
        if result:
            for i,results in enumerate(result):
                print(results)
                assign_card = Frame(assignment_card_frame, bg=button_color, padx=30, pady=15)
                assign_card.place(relx=.05, rely=.28*i, width=1099)
                    
                created_assignment_label = Label(assign_card, text=f'{result[i][1]}',  font=("Roboto", 16, "bold", "underline"), bg=button_color, fg="white", anchor="w", cursor="hand2")
                created_assignment_label.grid(row=1, column=0, sticky="w", pady=(0,10))
                created_assignment_label.bind("<Button-1>", lambda event, label=created_assignment_label: submitted_assignment(event, label))
                assignment_subject_label = Label(assign_card, text=f"Subject: "+f'{result[i][2]}',  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
                assignment_subject_label.grid(row=2, column=0, sticky="w")

                assignment_marks_label = Label(assign_card, text=f'Marks: {result[i][3]}',  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
                assignment_marks_label.grid(row=3, column=0, sticky="w")
        else:
            assign_heading.place_forget()
            no_assignment_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\sad.png")
            no_assignment_img = no_assignment_img.subsample(7)
            no_assignment_label = Label(right_frame, bg="white", text="No assginments found", font=("roboto", 25, "bold"), fg= button_color, image=no_assignment_img, compound=TOP, pady=20)
            no_assignment_label.place(relx=.5, rely=.5, anchor="center")
            no_assignment_label.image = no_assignment_img
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")



def my_team_uploaded_file(event, assignment_label):
     global clicked_assign_name, clicked_team_name
     join_assign_card = event.widget
     clicked_assign_name = assignment_label.cget("text")
     assignment_label.config(text=clicked_assign_name)
     print("Hello")
     try:
        print("This is assignment name: ",clicked_assign_name)
        query = (f"SELECT filename, filepath, assign_name FROM submitted_assignments where assign_name = '{clicked_assign_name}' and teamname = '{clicked_team_name}'")
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(result)
        uploaded_file_path = result[0][1]
        def open_uploaded_pdf():
             os.startfile(uploaded_file_path, 'open')

        print(result)
        if result:
            print("Assignment already uploaded")
            assignment_card_frame.place_forget()
            join_work_heading.place(relx=0.035, rely=.08, anchor="w")
            # join_uploaded_work = Frame(join_right_frame, bg=button_color, padx=30, pady=15)
            join_uploaded_work.place(relx=.05, rely=.2, width=1099, height=120)
            join_uploaded_file.place(relx=.5, rely=.5, anchor="center", width=1070, height=87)

            join_uploaded_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\pdf.png")
            join_uploaded_img = join_uploaded_img.subsample(16)
            join_uploaded_work_btn = Button(join_uploaded_file, text=result[0][0],  font=("Roboto", 15, "bold"), bg=button_color, fg="white", image=join_uploaded_img, compound=LEFT, cursor="hand2", padx=20, anchor="w", bd=0, highlightthickness=0, command=open_uploaded_pdf)
            join_uploaded_work_btn.image = join_uploaded_img
            join_uploaded_work_btn.place(relx=0, rely=.5, anchor="w", width=1068, height=84)

        else:
            print("Please upload assignment")
     except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

def create_join_assignment_cards():
    global count_of_assignment, clicked_team_name, no_join_assignment_label
    try:
        query = (f"SELECT assign_name, sub_name, total_marks FROM assignments where teamname = '{clicked_team_name}'")
        mycursor.execute(query)
        print(query)
        result = mycursor.fetchall()
        print("This is result",result)
        print(result)
        if result:
            for i,results in enumerate(result):
                join_assign_card = Frame(join_assignment_card_frame, bg=button_color, padx=30, pady=15)
                join_assign_card.place(relx=.05, rely=.28*i, width=1099)
                    
                join_assignment_label = Label(join_assign_card, text=f'{result[i][0]}',  font=("Roboto", 16, "bold", "underline"), bg=button_color, fg="white", anchor="w", cursor="hand2", name="assignment-label")
                join_assignment_label.grid(row=1, column=0, sticky="w", pady=(0,10))

                assignment_subject_label = Label(join_assign_card, text=f"Subject: "+f'{result[i][1]}',  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
                assignment_subject_label.grid(row=2, column=0, sticky="w")

                assignment_marks_label = Label(join_assign_card, text=f'Marks: {result[i][2]}',  font=("Roboto", 12), bg=button_color, fg="white", anchor="w")
                assignment_marks_label.grid(row=3, column=0, sticky="w")
                
                join_assignment_label.bind("<Button-1>", lambda event, label=join_assignment_label: join_upload_sec(event, label))
        else:
            join_assign_heading.place_forget()
            no_join_assignment_label.place(relx=.5, rely=.5, anchor="center")
            no_join_assignment_label.image = no_join_assignment_img

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")

def update_join_assignment_cards():
    # Clear the current cards
    for widget in join_assignment_card_frame.winfo_children():
        widget.destroy()

def update_assignment_cards():
    # Clear the current cards
    for widget in assignment_card_frame.winfo_children():
        widget.destroy()



###############################  TEAMS CARD ###############################
modal_frame = Frame(root, padx=50, pady=20, bg=button_color)

modal_title = Label(modal_frame, text="Create your team", font=("Roboto", 27, "bold"), bg=button_color, fg="white", anchor="w")
modal_title.place(y=10)

modal_sub_title = Label(modal_frame, text="Collaborate closely with a group of people inside your organization based on project, initiative, \nor common interest.", font=("Roboto", 12), bg=button_color, fg="white", anchor="w", justify=LEFT)
modal_sub_title.place(rely=.19, anchor="w")

team_name = Label(modal_frame, text="Team name", bg=button_color, fg="white", font=("Roboto", 14))
team_name.place(rely=0.34)

team_name = Entry(modal_frame, font=("Roboto", 14), bg=button_color, fg="white", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", insertbackground="white", width=27)
team_name.place(relx=.2, rely=.34, height=33)

team_subject_name = Label(modal_frame, text="Subject", bg=button_color, fg="white", font=("Roboto", 14))
team_subject_name.place(rely=0.46)

team_subject_name = Entry(modal_frame, font=("Roboto", 14), bg=button_color, fg="white", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", insertbackground="white", width=27)
team_subject_name.place(relx=.2, rely=.46, height=33)

team_teacher_name = Label(modal_frame, text="Professor", bg=button_color, fg="white", font=("Roboto", 14))
team_teacher_name.place(rely=0.58)

team_teacher_name = Entry(modal_frame, font=("Roboto", 14), bg=button_color, fg="white", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", insertbackground="white", width=27)
team_teacher_name.place(relx=.2, rely=.58, height=33)

team_text_area = Label(modal_frame, text="Description", bg=button_color, fg="white", font=("Roboto", 14))
team_text_area.place(rely=.7)

team_text_area = Label(modal_frame, text="(Optional)", bg=button_color, fg="white", font=("Roboto", 9))
team_text_area.place(rely=.75)

team_text_area = Text(modal_frame, width=27, height=5, bg=button_color, fg="white", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", insertbackground="white", font=("Roboto", 14), padx=15, pady=10)
placeholder_text = "Let people know about your team"

# Add placeholder text
team_text_area.insert("1.0", placeholder_text)
team_text_area.tag_configure("placeholder", foreground="grey", font=("roboto",10))
team_text_area.place(relx=.2, rely=.7)

button_frame = Frame(modal_frame, bg=button_color, width=300, height=50)
button_frame.place(relx=.7, rely=.9)

cancel_btn = Button(button_frame, text="Cancel", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2",command=lambda:(close_team_modal()))
cancel_btn.place(relx=.2, rely=.5, anchor="w")

next_btn = Button(button_frame, text="Next", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2", command=lambda:(create_team(), fetch_team_detail()))
next_btn.place(relx=.65, rely=.5, anchor="w")

# Bind events to remove and add placeholder text
def on_focus_in(event):
    if team_text_area.get("1.0", "end-1c") == placeholder_text:
        team_text_area.delete("1.0", "end-1c")
        team_text_area.tag_configure("placeholder", foreground="black")

def on_focus_out(event):
    if not team_text_area.get("1.0", "end-1c"):
        team_text_area.insert("1.0", placeholder_text)
        team_text_area.tag_configure("placeholder", foreground="grey")

team_text_area.bind("<FocusIn>", on_focus_in)
team_text_area.bind("<FocusOut>", on_focus_out)

# Bind the mouse click event to a function that closes the modal frame
main_frame.bind("<Button-1>", lambda event: modal_frame.destroy())


###############################  MODAL FRAME FOR JOINING THE TEAM  ###############################

join_modal_frame = Frame(root, padx=50, pady=20, bg=button_color)

join_modal_title = Label(join_modal_frame, text="Join the team", font=("Roboto", 27, "bold"), bg=button_color, fg="white", anchor="w")
join_modal_title.place(y=10)

join_team_name = Label(join_modal_frame, text="Enter the code", bg=button_color, fg="white", font=("Roboto", 14))
join_team_name.place(rely=0.34)

join_team_code = Entry(join_modal_frame, font=("Roboto", 14), bg=button_color, fg="white", bd=0, highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc", insertbackground="white", width=34)
join_team_code.place(relx=.01, rely=.48, height=33)

def code_show():
    code_entered = join_team_code.get()
    print("This is code", code_entered)
    return code_entered

join_button_frame = Frame(join_modal_frame, bg=button_color, width=300, height=50)
join_button_frame.place(relx=.25, rely=.8)

join_cancel_btn = Button(join_button_frame, text="Cancel", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2",command=lambda:(close_join_modal()))
join_cancel_btn.place(relx=.2, rely=.5, anchor="w")

join_next_btn = Button(join_button_frame, text="Next", padx=25, pady=5, bg="white", fg=button_color, bd=0, highlightbackground=button_color, highlightthickness=0,font=("roboto", 12, "bold"), cursor="hand2", command=lambda:("run_for_n_seconds(create_team, 5)", join_team()))
join_next_btn.place(relx=.65, rely=.5, anchor="w")

no_join_assignment_img = tk.PhotoImage(file=r"C:\Users\ANSHARI\Downloads\Python project\sad.png")
no_join_assignment_img = no_join_assignment_img.subsample(7)
no_join_assignment_label = Label(join_right_frame, bg="white", text="No assginments found", font=("roboto", 25, "bold"), fg= button_color, image=no_join_assignment_img, compound=TOP, pady=20)

###############################  OPTIONS FOR JOINED TEAMS  ###############################





# Create the table
table = ttk.Treeview(right_frame, columns=('Student name', 'Plagiarism found', 'Marks'))
# table.place(relx=.5, rely=.55, anchor="center")

# Define the headings for each column
table.heading('#0', text='Index'.upper())
table.heading('Student name', text='Student name'.upper())
table.heading('Plagiarism found', text='Plagiarism found'.upper())
table.heading('Marks', text='Marks'.upper())

# Set the column widths and alignments
table.column('Student name', width=400, anchor='center')
table.column('Plagiarism found', width=400, anchor='center')
table.column('Marks', width=250, anchor='center')
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

root.mainloop()
