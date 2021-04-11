import json
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "s.skornadev@gmail.com"
password = "crawler_real"
receiver_email = "s.skorna@gmail.com"
admin_email = "s.skorna@gmail.com"
base_cwd = "C:/Users/sskor/Documents/real_estate_crawler"
port = 465  # For SSL
# Create a secure SSL context
context = ssl.create_default_context()

def send_email_admin(msg):
    message = f"""
    Subject: Erorr in bazos crawler
    {msg}
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, admin_email, message)

data_new = {}
data_new['bazos'] = []

# Check that the dataset from today is not empty otherwise send email to admin

try:
    print(data_new['bazos'][0])
except TypeError as error:
    send_email_admin(msg=f'TypeError: {error}')
    sys.exit()
except KeyError as error:
    send_email_admin(msg=f'KeyError:{error} Named list not found in json')
    sys.exit()
except IndexError as error:
    send_email_admin(msg=f'IndexError:{error} on index 0 in data["bazos"]')
    sys.exit()