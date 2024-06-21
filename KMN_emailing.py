from email.message import EmailMessage
import ssl
import smtplib
import sys
import subprocess

#Automatically import the pip pandas library across different devices
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

#csv reading library
import pandas as reader


sender = "myemail@test.com"
pw = "password"
child = ""
subject = input("What is the subject: ")

#read the csv file of all emails iterating through each row
csv_file = "KMN_emails.csv"
information = reader.read_csv(csv_file)
for index, row in information.iterrows():
    #Iterate through each row and retrieve the "Email", and "Name" of the student and the email associated with the student
    email_recipient = row['Email']
    child = row['Name']

    body = f"""
Good Evening Parent of {child},

My name is xx and I'm trying to contact you directly through the inbox rather than junk
If you'd like to reach me my email is myemail@test.com. Thank you for your time.

Regards,
xx
"""
    #Formulate Email
    email = EmailMessage()
    email.set_content(body, subtype = "plain", charset = 'us-ascii')
    email['From'] = sender
    email['To'] = email_recipient
    email['Subject'] = subject


    #Layer of security
    context = ssl.create_default_context()
    #Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(sender, pw)
        smtp.sendmail(sender, email_recipient, email.as_string())