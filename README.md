# KMN_emailing
Started in June 2024 and revisited in April 2025, This project started out as an emailing system for Kumon Learning that allowed users to send emails out to parents simultaneously rather than individually forming emails. In April of 2025, A third-party consumer requested some refinements and QOl updates to the project for their research lab to use and I took that opportunity to expand the program beyond a speciailized product for Kumon to a more generalized tool that anyone could use.

Requirements and Important Notes

To use the program you'll need:
An email
An app password for the designated email
A CSV file to read from

What is an app password?
First off, something that may immediately strike concern is giving your google password to a random program off the internet. This section will explain why there is no security risk for you and how this program will operate risk-free.
Sending emails over the internet typically uses the Simple Mail Transfer Protocol (SMTP), this program uses Google as its SMTP server. Google recently changed their security layers to be more stringent on what kind of third-party apps are able to access accounts. Because this program is in Python, it is not directly affiliated with Google and therefore a third-party app that needs to follow their security rules. Google created App Passwords to allow third-parties to do what they need to do while limiting their access to users' information. This means that my program cannot steal any information from you, the user. To create an app password, I recommend following this video guide starting at 1:10, it shows you everything you need to do to set up an app password for my program. https://www.youtube.com/watch?v=Sddnn6dpqk0&t=2s

Why do I need a CSV file?
The program reads from a Comma Separated Value (CSV) file, originally when I made this program for Kumon I intended the database to store neccessary information about each child and their associated parent but I was told that it didnt need to be that robust and was asked to just have it track the emails. In its current iteration it's very much the same and only requires the CSV file to have emails listed out. To have it properly work the first line of the CSV file needs to be "Email" afterwards you can list out all the emails you intend to send to each being on a new line refer to the sample .csv files for an example.
