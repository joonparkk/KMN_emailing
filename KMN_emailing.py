import ssl
import smtplib
import sys
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *
from tkinter import filedialog

#Automatically import the pip pandas library across different devices
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

#csv reading library
import pandas as reader
    
sender = "myemail@test.com"
pw = "password"
child = ""
subject = ""
attachment_path = ""
body = ""

#read the csv file of all emails iterating through each row
csv_file = "mycsv.csv"
information = reader.read_csv(csv_file)

def send_emails(email_list):
    for index, row in email_list.iterrows():
        #Iterate through each row and retrieve the "Email", and "Name" of the student and the email associated with the student
        if reader.isnull(row['Email']) == True:
            continue
        email_recipient = row['Email']

        #Formulate Email
        email = MIMEMultipart()
        email['From'] = sender
        email['To'] = email_recipient
        email['Subject'] = subject
        email.attach(MIMEText(body, 'plain'))
        if attachment_path != "":
            attachment = open(attachment_path, 'rb')
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename= " + attachment_path)
            email.attach(attachment_package)


        #Layer of security
        context = ssl.create_default_context()
        #Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls(context = context)
            smtp.login(sender, pw)
            smtp.sendmail(sender, email_recipient, email.as_string())
    progressLabel.configure(text= "Progress: Emails have been sent!")

def open_file():
    global attachment_path 
    attachment_path = filedialog.askopenfilename()
    attachmentLabel.configure(text= "Attachment: {}".format(attachment_path))

def get_text():
    global body
    global subject
    body = inputtxt.get("1.0", 'end-1c')
    subject = subjecttxt.get("1.0", 'end-1c')
    send_emails(information)


myWindow = Tk()
myWindow.geometry("700x700")
bodyLabel = Label(myWindow, text="Enter Body:")
subjectLabel = Label(myWindow, text= "Enter Subject:")
attachmentLabel = Label(myWindow, text = "Attachment:")
progressLabel = Label(myWindow, text = "Progress: Emails not sent yet")

subjecttxt = Text(myWindow, height = 2, width = 50, bg = "light blue")
inputtxt = Text(myWindow, height = 10, width = 50, bg = "light yellow")
quitButton = Button(myWindow, text="Quit", command=myWindow.destroy, height= 1, width=10)
sendButton = Button(myWindow, text = "Send", command= lambda:get_text(), height=1, width= 10)
attachmentButton = Button(myWindow, text = "Add Attachment", command = lambda:open_file(), height=1, width=15)


subjectLabel.pack()
subjecttxt.pack()

bodyLabel.pack(pady= (60,0))
inputtxt.pack()

attachmentLabel.pack(pady=(60,0))
attachmentButton.pack()

sendButton.pack(pady=(60,0))
progressLabel.pack()

quitButton.pack(pady=(60,0))
inputtxt.focus_set()

myWindow.mainloop()