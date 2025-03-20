import imaplib
import email
import re
import logging
import requests
import webbrowser
import sys
import subprocess
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GmailAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.mail = None

    def connect_to_gmail(self):
        """Connects to Gmail via IMAP."""
        try:
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
            self.mail.login(self.email, self.password)
            self.mail.select("inbox")
            logging.info("✅ Connected to Gmail successfully!")
        except Exception as e:
            logging.error(f"❌ Error connecting to Gmail: {e}")

    def fetch_email_with_subject(self, subject_keyword):
        """Searches for an unread email that starts with the given subject keyword."""
        try:
            status, messages = self.mail.search(None, "UNSEEN")
            email_ids = messages[0].split()
            if not email_ids:
                logging.info("📭 No new emails found.")
                return None, None

            for email_id in reversed(email_ids):
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        if subject and subject.startswith(subject_keyword):
                            logging.info(f"📌 Matching Email Found! Subject: {subject}")
                            self.mail.store(email_id, "+FLAGS", "\\Seen")
                            email_body = ""

                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    content_disposition = str(part.get("Content-Disposition"))
                                    if content_type == "text/plain" and "attachment" not in content_disposition:
                                        email_body += part.get_payload(decode=True).decode(errors="ignore") + "\n\n"
                            else:
                                email_body = msg.get_payload(decode=True).decode(errors="ignore")

                            logging.info("📩 Email Content:")
                            logging.info(email_body.strip())

                            links = re.findall(r"https?://[^\s]+", email_body)
                            if links:
                                logging.info(f"🔗 Extracted Link: {links[0]}")
                                return email_body, links[0]
                            else:
                                logging.warning("⚠ No link found in the email!")
                                return email_body, None

            logging.info("📭 No matching email found.")
            return None, None
        except Exception as e:
            logging.error(f"❌ Error fetching email: {e}")
            return None, None

    def generate_second_url(self, first_url):
        """Generates the second URL based on the extracted link."""
        parsed_url = urlparse(first_url)
        query_params = parse_qs(parsed_url.query)
        cid = query_params.get('cid', [''])[0]
        accept_key = query_params.get('acceptKey', [''])[0]

        base_url = 'https://ulg-ssa.lspware.com/Atrium/MyLanguageBankServlet'
        new_query_params = {
            'action': 'acceptDeclineJob',
            'cid': cid,
            'id': accept_key
        }
        encoded_query = urlencode(new_query_params)
        new_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            '/Atrium/MyLanguageBankServlet',
            '',
            encoded_query,
            ''
        ))
        return new_url

    def hit_generated_url(self, url):
        """Sends a GET request to the generated URL and opens it in a web browser."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info(f"✅ Successfully accessed: {url}")
                webbrowser.open(url)
            else:
                logging.error(f"❌ Failed to access {url}, Status Code: {response.status_code}")
        except Exception as e:
            logging.error(f"❌ Error hitting the generated URL: {e}")

    def close_connection(self):
        """Closes the email connection."""
        if self.mail:
            self.mail.logout()
            logging.info("📴 Gmail connection closed.")

def main():
    parser = argparse.ArgumentParser(description="Automate Gmail tasks")
    parser.add_argument("--email", required=True, help="Your Gmail address")
    parser.add_argument("--password", required=True, help="Your Gmail app password")
    parser.add_argument("--subject", required=True, help="Keyword to search in email subject")
    args = parser.parse_args()

    gmail_bot = GmailAutomation(args.email, args.password)
    gmail_bot.connect_to_gmail()
    email_body, link = gmail_bot.fetch_email_with_subject(args.subject)

    if not link:
        logging.info("❌ No mail found with the subject. Stopping execution.")
        gmail_bot.close_connection()
        sys.exit()

    second_url = gmail_bot.generate_second_url(link)
    logging.info(f"🔗 Generated Second URL: {second_url}")
    gmail_bot.hit_generated_url(second_url)
    gmail_bot.close_connection()

if __name__ == "__main__":
    main()
