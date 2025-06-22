import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from dotenv import load_dotenv
from openrouter_client import OpenRouterClient

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
IMAP_SERVER = os.getenv('IMAP_SERVER')
SMTP_SERVER = os.getenv('SMTP_SERVER')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Initialize OpenRouter client
ai_client = OpenRouterClient(OPENROUTER_API_KEY)

def fetch_latest_email():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('inbox')
        typ, data = mail.search(None, 'UNSEEN')
        mail_ids = data[0].split()
        if not mail_ids:
            return None, None
        latest_id = mail_ids[-1]
        typ, msg_data = mail.fetch(latest_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg['subject']
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        return subject, body

def send_email(subject, body, to_addr):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_addr
    with smtplib.SMTP_SSL(SMTP_SERVER) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_addr, msg.as_string())

def main():
    subject, body = fetch_latest_email()
    if not body:
        print("No new emails.")
        return
    print(f"Fetched email: {subject}\n{body}")
    ai_reply = ai_client.ask(f"Reply to this email: {body}")
    print("AI-generated reply:", ai_reply)
    # Example: send reply to the same sender (customize as needed)
    # send_email(f"Re: {subject}", ai_reply, sender_email)

if __name__ == "__main__":
    main()
