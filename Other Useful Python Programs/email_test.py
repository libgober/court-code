#test sending an email in python

import smtplib

sender = 'libgober@gmail.com'
receivers = 'blibgober@g.harvard.edu'

message = """From: Alan Stuart <r3k790@gmail.com>
To: Brian <blibgober@g.harvard.edu>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login("r3k790","Aa571423")
server.sendmail(sender, receivers, message)     
server.quit()    
print "Successfully sent email"