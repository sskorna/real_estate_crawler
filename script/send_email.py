import json
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "s.skornadev@gmail.com"
password = "crawler_real"
# password = input("Type your password and press enter: ")
receiver_emails = ["s.skorna@gmail.com", "jano.skorna@gmail.com"]
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

with open(f"{base_cwd}/data/new/bazos.json") as f:
    data_new = json.load(f)
 
with open(f"{base_cwd}/data/yesterday/bazos.json") as f:
    data_yesterday = json.load(f)

# Check that the dataset from today is not empty otherwise send email to admin

try:
    print(data_new['bazos'][0])
except TypeError as error:
    send_email_admin(msg=f'TypeError: {error} No data found!')
    sys.exit()
except KeyError as error:
    send_email_admin(msg=f'KeyError:{error}Named list not found in json')
    sys.exit()
except IndexError as error:
    send_email_admin(msg=f'IndexError:{error} on index 0 in data["bazos"]')
    sys.exit()

# Find new posts
posts_to_send = []
for idx, post in enumerate(data_new['bazos']):
    if post['id'] not in [post_old['id'] for post_old in data_yesterday['bazos']]:
        # print(idx)
        # print(post)
        posts_to_send.append(post)


# Send Email if new posts
if (len(posts_to_send) == 0):
    sys.exit()

# Create a secure SSL context
context = ssl.create_default_context()

message = MIMEMultipart("alternative")
message["Subject"] = "Nové Inzeráty"
message["From"] = sender_email
message["To"] = ', '.join(receiver_emails)

message_body = ""
for post in posts_to_send:
    message_body = f"""
        {message_body}
        <p style="margin-left: 40px">
        <a href={post['url']}>{post['header']}</a><br>
        s cenou {post['detail']['price']}, 
        zverejnený od '{post['detail']['name']}', 
        už ho videlo {post['detail']['seen']}<br>
        </p>
    """ 

html = f"""
<html>
  <body>
    <p>Dobrý deň, pán Škorňa,<br>
       Hlásim nové inzeráty:<br>
    </p>
    {message_body}
    <p>S pozdravom<br>
        Šimonov robot
    </p>
  </body>
</html>
"""
part2 = MIMEText(html, "html")
message.attach(part2)
# print(message.as_string()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("s.skornadev@gmail.com", password)
    server.sendmail(sender_email, receiver_emails, message.as_string())