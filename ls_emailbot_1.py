# email bot for LS by 4EPEHK0B

import smtplib, ssl
import sys

print('...')
print('sending invitation email to: '+str(sys.argv[len(sys.argv) - 2])+'/n from: '+str(sys.argv[len(sys.argv) - 1]))
print('...')

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "ls.emailbot@gmail.com"  # Enter your address
receiver_email = sys.argv[len(sys.argv) - 2]  # Enter receiver address          ls.emailbot@gmail.com
password = "ypwqzdsnqenxhtuy"

message = """\
Subject: Automatic reply

Hi everyone,
Your message has been receved.

Our team will make it's best to ansver as soon as posible!
If you still have some questions please write them as the responces to thic message. Otherwice it will take longer for us to reply to you.

A join request was requested by telegram user with telegram ID: """+str(sys.argv[len(sys.argv) - 1])+"""
If you hanen't sent the request, just ignore it.

Best wishes
LowsSkills"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)