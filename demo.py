import ftplib

# Open a connection to the FileZilla server
ftp = ftplib.FTP('127.0.0.1', 'pdfx', 'Mohammad#131#')

# Change to the directory where you want to upload the file
# ftp.cwd("PDF")

# Open the file you want to upload
with open(r"C:\Users\ANSHARI\Downloads\Python project\31.pdf", 'rb') as file:
    # Upload the file to the FTP server
    ftp.storbinary('STOR 31.pdf', file)

# Close the FTP connection
ftp.quit()
