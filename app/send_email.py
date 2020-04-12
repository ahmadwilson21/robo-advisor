
# adapted from https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/packages/sendgrid.md

import os
#import pprint

from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.

def sendEmail(toEmail, prompt,email_subject):
    """
    Sends an email to a specified email address using the Sendgrid API
    This code was taken from a template

    Params: 
        toEmail(string) the email that you want to send the message to
        prompt(string) the message that you want to send
        email_subject(string) the subject for the email
    
    Example: sendEmail("me@123.com", "Reminder, this is an example email")

    Returns: 202 (if email was sent successfully)
    
    """

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
    MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

    # AUTHENTICATE

    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    # COMPILE REQUEST PARAMETERS (PREPARE THE EMAIL)



    from_email = Email(MY_EMAIL_ADDRESS)
    to_email = Email(toEmail)
    subject = email_subject
    message_text = prompt
    content = Content("text/plain", message_text)
    mail = Mail(from_email, subject, to_email, content)

    # ISSUE REQUEST (SEND EMAIL)

    response = sg.client.mail.send.post(request_body=mail.get())

    

    # Response Error Checking
    if (response.status_code == 202):
        print("Email sent successfully")
    else:
        print(f"Email not sent correctly. Email: {to_email} or {from_email} may not be real emails")

    return response.status_code
    

