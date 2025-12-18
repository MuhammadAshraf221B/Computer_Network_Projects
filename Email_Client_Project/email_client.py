import smtplib
import imaplib
import email
from email.message import EmailMessage
import getpass
import ssl
import socket   
import time     

# ---------------- TCP Notification ----------------
def send_notification(message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect(("127.0.0.1", 9999))                        
        s.send(message.encode())                                
        s.close()                                              
    except Exception as e:
        print("Notification error:", e)

# ---------------- SMTP Send ----------------
def send_email():
    print("=== Send Email (SMTP) ===")
    smtp_server = input("SMTP server: ").strip()
    smtp_port = int(input("SMTP port (465 for SSL, 587 for TLS) [587]: ") or 587)  
    username = input("SMTP username: ").strip()
    password = getpass.getpass("SMTP password: ")

    to_addr = input("Receiver email: ").strip()
    subject = input("Subject: ").strip()
    body = input("Body: ").strip()

    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    start = time.time()  

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(
                smtp_server, smtp_port, context=ssl.create_default_context()
            ) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(username, password)
                server.send_message(msg)

        print("Email sent successfully!")
        print("SMTP Latency:", round(time.time() - start, 3), "seconds") 
        send_notification("Email Sent Successfully")                       

    except Exception as e:
        print("Error sending email:", e)
        send_notification("Email Sending Failed")                          

# ---------------- IMAP Receive ----------------
def read_latest_email():
    print("=== Read Latest Email (IMAP) ===")
    imap_server = input("IMAP server: ").strip()
    imap_port = int(input("IMAP port [993]: ") or 993)
    username = input("IMAP username: ").strip()
    password = getpass.getpass("IMAP password: ")

    start = time.time() 

    try:
        with imaplib.IMAP4_SSL(imap_server, imap_port) as imap:
            imap.login(username, password)
            imap.select("INBOX")

            typ, data = imap.search(None, "ALL")
            if typ != "OK" or not data or not data[0]:
                print("Inbox empty or search failed.")
                return

            latest_id = data[0].split()[-1]
            typ, msg_data = imap.fetch(latest_id, "(RFC822)")
            if typ != "OK":
                print("Failed to fetch email.")
                return

            msg = email.message_from_bytes(msg_data[0][1])
            print(f"Subject: {msg.get('Subject', '(no subject)')}")

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                        charset = part.get_content_charset() or "utf-8"
                        print("Body:\n", part.get_payload(decode=True).decode(charset, errors="replace"))
                        break
            else:
                charset = msg.get_content_charset() or "utf-8"
                print("Body:\n", msg.get_payload(decode=True).decode(charset, errors="replace"))

            print("IMAP Latency:", round(time.time() - start, 3), "seconds")  
            send_notification("Email Received Successfully")                    

    except Exception as e:
        print("Error reading email:", e)
        send_notification("Email Receiving Failed")                          

# ---------------- Main ----------------
def main():
    while True:
        print("\nSimple Email Client")
        print("1. Send Email (SMTP)")
        print("2. Read Latest Email (IMAP)")
        print("3. Exit")
        choice = input("Choose an option [1-3]: ").strip()
        if choice == "1":
            send_email()
        elif choice == "2":
            read_latest_email()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
