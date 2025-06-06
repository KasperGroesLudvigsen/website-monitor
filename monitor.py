import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests

URL = "https://example.com"
STATE_PATH = "state/last_hash.txt"

def fetch_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def hash_content(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def load_previous_hash():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r") as f:
            return f.read().strip()
    return None

def save_current_hash(content_hash):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        f.write(content_hash)

def send_email(subject, body):
    sender = os.environ["GMAIL_USER"]
    receivers = os.environ["EMAIL_RECEIVERS"].split(",")
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())

def main():
    content = fetch_page_text(URL)
    current_hash = hash_content(content)
    previous_hash = load_previous_hash()

    if previous_hash != current_hash:
        print("Change detected.")
        send_email(
            "Web page changed!",
            f"The content of {URL} has changed."
        )
        save_current_hash(current_hash)
    else:
        print("No change detected.")

if __name__ == "__main__":
    main()
