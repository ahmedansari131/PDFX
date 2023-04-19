import PyPDF2
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import os
from PIL import Image
from fpdf import FPDF
import fitz
import io
from PIL import Image
import difflib
import copy
import mysql.connector
from mysql.connector.errors import Error

allPDF = {}
exTxt = {}
numPdf = 0
login = False

# # Create a connection to the MySQL database
# try:
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="pcred",
#         port="3306"
#     )
#     print("Connection successful")

# except Error as e:
#     print(f"The error '{e}' occurred")
#     mydb = None

# if mydb is not None:
#     # Create a cursor to execute SQL queries
#     mycursor = mydb.cursor()
#     print("This is cursor")
# else:
#     print("Connection failed")

# # Create a function to handle the signup button click
# def signup():
#     # Get the username and password values from the form
#     username = input("Enter Username\n")
#     password = input("Enter Password\n")
#     c_password = input("Enter Confirm Password\n")

#     try:
#         # Execute an INSERT query to add the new user to the database
#         if(password == c_password):
#             mycursor.execute("INSERT INTO signup (username, password) VALUES (%s, %s)", (username, password))
#             print("Your account has been created\n")
#         else:
#             print("Confirm password does not match\n")

#         # Commit the changes to the database
#         mydb.commit()

#     except mysql.connector.Error as e:
#         print(f"The error '{e}' occurred")

# def login():
#     # Get the username and password values from the form
#     username = input("Enter Username\n")
#     password = input("Enter Password\n")

#     try:
#         # Execute a SELECT query to check if the username and password exist in the database
#         mycursor.execute("SELECT * FROM signup WHERE username='" + username + "' AND password='" + password + "'")

#         # Get the result of the query
#         result = mycursor.fetchone()

#         # If the result is not empty, the user is logged in
#         if result:
#            print("You are now loggedin!")
#            login = True
#         else:
#           print("Invalid username or password")

#     except mysql.connector.Error as e:
#         print(f"The error '{e}' occurred")

# print("Welcome to PDFX")
# user_choice = int(input("1. Login\n2. Signup\n"))

# match user_choice:
#     case 1:
#         login()
#     case 2:
#         signup()

# if(login):
numPdf = int(input("Enter the numbers of pdf you want to upload: "))
for i in range(numPdf):
    pdfPath = input(f"Enter the {i+1} path of the PDF: ")
    pdfPath = pdfPath.replace('''"''', "")
    file_name = os.path.basename(pdfPath)
    allPDF[file_name] = pdfPath

print("This is the first input from the user", allPDF)
for file_key in allPDF:
    if not os.path.isfile(allPDF[file_key]):
        print(f"{allPDF[file_key]} does not exist!")
    else:
        print(f"{allPDF[file_key]} exists!")


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

entireTxt = ''
imgTxt = readFrmImg(allPDF)
entireTxt = getTxt(allPDF, imgTxt)
# print(entireTxt)

for file1, txt1 in entireTxt.items():
    for file2, txt2 in entireTxt.items():
        if file1 < file2:
            print((file1))
            # print(txt1)
            # print(txt2)
            seq = difflib.SequenceMatcher(None, txt1, txt2)
            similarity_ratio = seq.ratio()
            matches = seq.get_matching_blocks()
            for match in matches:
                match_text = txt1[match.a:match.a+match.size]
                print("Match text is:", match_text)
            if similarity_ratio > 0.8:  # adjust the threshold as needed
                print(f"{file1} and {file2} have a high plagiarism: {round(similarity_ratio*100, 2)} %\n")
                print("Match text is:", match_text)
            else:
                print(f"{file1} and {file2} has plagiarism: {round(similarity_ratio*100, 2)} %\n")


# "C:\Users\ANSHARI\Downloads\Python project\43.pdf"
# "C:\Users\ANSHARI\Downloads\Python project\31.pdf"
# "C:\Users\ANSHARI\Downloads\Python project\34.pdf"



