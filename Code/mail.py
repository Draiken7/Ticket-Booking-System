import smtplib
import smtplib
import datetime
import json
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from jinja2 import Template
import configs.mailConfig as mailConfig


# Setting Configs
SMPTP_SERVER_HOST = mailConfig.SMPTP_SERVER_HOST
SMPTP_SERVER_PORT = mailConfig.SMPTP_SERVER_PORT
SENDER_ADDRESS = mailConfig.SENDER_ADDRESS
SENDER_PASSWORD = mailConfig.SENDER_PASSWORD


jobs = {
    "html_templates" : [
        "./templates/theaterReport.html",
        "./templates/reminder.html", 
        "./templates/monthly.html"
    ],
    "subject": [
        "Theater Report",
        "Reminder",
        "Monthly Summary"
    ]
}

# Basic send mail fucntion!
def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Email attachments are sent as base64 encoded
        encoders.encode_base64(part)
        # From: https://www.ietf.org/rfc/rfc2183.txt
        # Bodyparts can be designated `attachment' to indicate that they are
        # separate from the main body of the mail message, and that their
        # display should not be automatic, but contingent upon some further
        # action of the user.
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_file}",
        )
        # Add the attchment to msg
        msg.attach(part)

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    # s.starttls()
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


def format_message(template_file, data={}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data)


def send_notifsReports(data, temp=0, file=None):
        
    message = format_message(jobs["html_templates"][temp], data=data)
    # this can be a seaprate task
    send_email(
        to_address=data["user"]["email"],
        subject=jobs["subject"][temp],
        message=message,
        content="html",
        attachment_file=file,
    )   