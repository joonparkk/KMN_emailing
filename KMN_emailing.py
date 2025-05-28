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
import html
import os
#Automatically import the pip pandas library across different devices
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

#csv reading library
import pandas as reader
attachment_path = ""

#read the csv file of all emails iterating through each row
csv_file = ""

def compile_list(email_list):
    recipients = []
    for index, row in email_list.iterrows():
        #Iterate through each row and retrieve the "Email", and "Name" of the student and the email associated with the student
        if reader.isnull(row['Email']) == True:
            continue
        recipients.append(row['Email'])
    send_emails(recipients)

def send_emails(recipients):
    sender = emailtxt.get("1.0", "end-1c")
    pw = passwordtxt.get("1.0", "end-1c")
    subject = subjecttxt.get("1.0", 'end-1c')
        #Formulate Email
    email = MIMEMultipart()
    email['From'] = sender
    email['Bcc'] = ', '.join(recipients)
    email['Subject'] = subject
    email.attach(MIMEText(get_html_body(), 'html'))
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
        filename = os.path.basename(attachment_path)
        attachment_package.add_header('Content-Disposition', f'attachment; filename="{filename}"')

def get_text():
    information = reader.read_csv(csv_file)
    compile_list(information)

def get_html_body():
    content = ""
    index = "1.0"
    try:
        while True:
            next_index = inputtxt.index(f"{index} +1c")
            if next_index == index:
                break

            char = inputtxt.get(index, next_index)
            escaped_char = html.escape(char)

            if char == "\n":
                content += "<br>"
            else:
                tags = inputtxt.tag_names(index)
                if "bold" in tags:
                    content += f"<b>{escaped_char}</b>"
                elif "italic" in tags:
                    content += f"<i>{escaped_char}</i>"
                elif "underline" in tags:
                    content += f"<u>{escaped_char}</u>"
                else:
                    content += escaped_char

            index = next_index
    except Exception as e:
        print("Error in get_html_body:", e)

    return f"<html><body>{content}</body></html>"

def toggle_bold():
    toggle_text("bold")

def toggle_italics():
    toggle_text("italic")

def toggle_underline():
    toggle_text("underline")

def toggle_text(tag):
    try:
        start = inputtxt.index("sel.first")
        end = inputtxt.index("sel.last")

        # Check if the selected text has the tag
        if tag in inputtxt.tag_names("sel.first"):
            inputtxt.tag_remove(tag, start, end)
        else:
            inputtxt.tag_add(tag, start, end)
    except TclError:
        pass  # No text is selected

def choose_csv():
    global csv_file
    csv_file = filedialog.askopenfilename(title= "Select CSV File", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    fileLabel.configure(text=csv_file)
    


    
myWindow = Tk()
myWindow.geometry("700x800")

csvLabel = Label(myWindow, text="Choose CSV file:")
fileLabel = Label(myWindow, text="No File Chosen")
bodyLabel = Label(myWindow, text="Enter Body:")
subjectLabel = Label(myWindow, text= "Enter Subject:")
attachmentLabel = Label(myWindow, text = "Attachment:")
progressLabel = Label(myWindow, text = "Progress: Emails not sent yet")

email_pw_frame = Frame(myWindow)
email_pw_frame.pack(pady=(15,15))

emailLabel = Label(email_pw_frame, text ="Your Email:")
passwordLabel =Label(email_pw_frame, text="Your App Password:")

emailtxt = Text(email_pw_frame, height = 1, width = 40)
passwordtxt = Text(email_pw_frame, height = 1, width = 25)
subjecttxt = Text(myWindow, height = 2, width = 50, bg = "light blue")
inputtxt = Text(myWindow, height = 10, width = 50, bg = "light yellow")
base_font = tkFont.nametofont(inputtxt.cget("font"))

bold_font = base_font.copy()
bold_font.configure(weight="bold")

italic_font = base_font.copy()
italic_font.configure(slant="italic")

underline_font = base_font.copy()
underline_font.configure(underline=1)

inputtxt.tag_configure("bold",      font=bold_font)
inputtxt.tag_configure("italic",    font=italic_font)
inputtxt.tag_configure("underline", font=underline_font)

csvButton = Button(myWindow, text= "Add CSV File:", command=lambda:choose_csv(), height=1, width=15)
quitButton = Button(myWindow, text="Quit", command=myWindow.destroy, height= 1, width=10)
sendButton = Button(myWindow, text = "Send", command= lambda:get_text(), height=1, width= 10)
attachmentButton = Button(myWindow, text = "Add Attachment", command = lambda:open_file(), height=1, width=15)

emailLabel.pack()
emailtxt.pack()

passwordLabel.pack()
passwordtxt.pack()

fileLabel.pack()
csvButton.pack(pady=(0,20))

subjectLabel.pack()
subjecttxt.pack()

bodyLabel.pack(pady= (60,0))
inputtxt.pack()

attachmentLabel.pack(pady=(30,0))
attachmentButton.pack()

font_btn_frame = Frame(myWindow)
font_btn_frame.pack(pady=(30,15))

boldButton = Button(font_btn_frame, text="Bold", command=toggle_bold, height=1, width=10)
italicsButton = Button(font_btn_frame, text="Italics", command=toggle_italics, height=1, width=10)
underlineButton = Button(font_btn_frame, text="Underline", command=toggle_underline, height=1, width=10)

boldButton.pack(side="left", padx=5)
italicsButton.pack(side="left", padx=5)
underlineButton.pack(side="left", padx=5)


sendButton.pack(pady=(15,0))
progressLabel.pack()

quitButton.pack(pady=(40,0))
inputtxt.focus_set()

myWindow.mainloop()