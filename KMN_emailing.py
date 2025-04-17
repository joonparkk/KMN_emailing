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
import tkinter.font as tkFont

#Automatically import the pip pandas library across different devices
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

#csv reading library
import pandas as reader
    
sender = ""
pw = ""
child = ""
subject = ""
attachment_path = ""
body = ""

#read the csv file of all emails iterating through each row
csv_file = "KMN_emails.csv"
information = reader.read_csv(csv_file)

def compile_list(email_list):
    recipients = []
    for index, row in email_list.iterrows():
        #Iterate through each row and retrieve the "Email", and "Name" of the student and the email associated with the student
        if reader.isnull(row['Email']) == True:
            continue
        recipients.append(row['Email'])
    send_emails(recipients)

def send_emails(recipients):
        #Formulate Email
    email = MIMEMultipart()
    email['From'] = sender
    email['Bcc'] = ', '.join(recipients)
    email['Subject'] = subject
    email.attach(MIMEText(body, 'plain'))
    if attachment_path != "":
        email.attach(attachment_package)
        #Layer of security
    context = ssl.create_default_context()
        #Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls(context = context)
        smtp.login(sender, pw)
        smtp.sendmail(sender, recipients, email.as_string())
    progressLabel.configure(text= "Progress: Emails have been sent!")

def open_file():
    global attachment_path 
    attachment_path = filedialog.askopenfilename()
    attachmentLabel.configure(text= "Attachment: {}".format(attachment_path))
    get_path(attachment_path)

def get_path(attachment_path):
    global attachment_package
    with open(attachment_path, 'rb') as attachment:
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + attachment_path)

def get_text():
    global body
    global subject
    body = inputtxt.get("1.0", 'end-1c')
    subject = subjecttxt.get("1.0", 'end-1c')
    compile_list(information)

def toggle_bold():
    try:
        start = inputtxt.index("sel.first")
        end = inputtxt.index("sel.last")

        # Check if the selected text has the "bold" tag
        if "bold" in inputtxt.tag_names("sel.first"):
            inputtxt.tag_remove("bold", start, end)
        else:
            inputtxt.tag_add("bold", start, end)
    except TclError:
        pass  # No text is selected


    
myWindow = Tk()
myWindow.geometry("700x700")
bodyLabel = Label(myWindow, text="Enter Body:")
subjectLabel = Label(myWindow, text= "Enter Subject:")
attachmentLabel = Label(myWindow, text = "Attachment:")
progressLabel = Label(myWindow, text = "Progress: Emails not sent yet")

subjecttxt = Text(myWindow, height = 2, width = 50, bg = "light blue")
inputtxt = Text(myWindow, height = 10, width = 50, bg = "light yellow")
bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
inputtxt.tag_configure("bold", font=bold_font)

quitButton = Button(myWindow, text="Quit", command=myWindow.destroy, height= 1, width=10)
sendButton = Button(myWindow, text = "Send", command= lambda:get_text(), height=1, width= 10)
attachmentButton = Button(myWindow, text = "Add Attachment", command = lambda:open_file(), height=1, width=15)

boldButton = Button(myWindow, text="Bold", command=toggle_bold, height=1, width=10)


subjectLabel.pack()
subjecttxt.pack()

bodyLabel.pack(pady= (60,0))
inputtxt.pack()

attachmentLabel.pack(pady=(60,0))
attachmentButton.pack()

boldButton.pack(pady=(30,0))

sendButton.pack(pady=(30,0))
progressLabel.pack()

quitButton.pack(pady=(60,0))
inputtxt.focus_set()

myWindow.mainloop()