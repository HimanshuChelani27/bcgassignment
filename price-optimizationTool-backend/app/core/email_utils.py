import smtplib, ssl
from email.message import EmailMessage

def send_verification_email(sender_email, receiver_email, app_password, verification_link, name):
    subject = "Verify Your Email"
    body = f"""Hi {name},

Himanshu this side 👋

I saw you trying to sneak into my PRICE OPTIMIZATION TOOL — love the enthusiasm! 😄  
But hey, we’ve got standards (and spam filters), so you'll need to do this one tiny thing first.

Click this magical link to verify your email and unlock the doors to data-powered greatness:  
{verification_link} 🪄✨

See you on the other side!
"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(sender_email, app_password)
        server.send_message(msg)
