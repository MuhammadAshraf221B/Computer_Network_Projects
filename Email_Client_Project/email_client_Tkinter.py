import smtplib
import imaplib
import email
from email.message import EmailMessage
import ssl
import socket
import time
import tkinter as tk
from tkinter import messagebox
from plyer import notification

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
def send_email(username, password, to_addr, subject, body, smtp_server, smtp_port):
    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    start = time.time()
    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(username, password)
                server.send_message(msg)

        latency = round(time.time() - start, 3)
        messagebox.showinfo("Success", f"Email sent successfully!\nLatency: {latency} s")
        send_notification("Email Sent Successfully")

    except Exception as e:
        messagebox.showerror("Error", f"Error sending email: {e}")
        send_notification("Email Sending Failed")

# ---------------- IMAP Receive ----------------
def read_latest_email(username, password, imap_server, imap_port):
    start = time.time()
    try:
        with imaplib.IMAP4_SSL(imap_server, imap_port) as imap:
            imap.login(username, password)
            imap.select("INBOX")

            typ, data = imap.search(None, "ALL")
            if typ != "OK" or not data or not data[0]:
                messagebox.showinfo("Info", "Inbox empty or search failed.")
                return

            latest_id = data[0].split()[-1]
            typ, msg_data = imap.fetch(latest_id, "(RFC822)")
            if typ != "OK":
                messagebox.showerror("Error", "Failed to fetch email.")
                return

            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get("Subject", "(no subject)")
            
            body_text = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                        charset = part.get_content_charset() or "utf-8"
                        body_text = part.get_payload(decode=True).decode(charset, errors="replace")
                        break
            else:
                charset = msg.get_content_charset() or "utf-8"
                body_text = msg.get_payload(decode=True).decode(charset, errors="replace")

            latency = round(time.time() - start, 3)

            # Push Notification
            notification.notify(
                title=f"New Email: {subject}",
                message=body_text,
                timeout=10
            )

            messagebox.showinfo("Success", f"Latest Email Received!\nSubject: {subject}\nLatency: {latency} s")
            send_notification("Email Received Successfully")

    except Exception as e:
        messagebox.showerror("Error", f"Error reading email: {e}")
        send_notification("Email Receiving Failed")

# ---------------- GUI Windows ----------------
def send_email_window():
    win = tk.Toplevel()
    win.title("Send Email (SMTP)")

    labels = ["SMTP Server", "Port", "Username", "Password", "To", "Subject", "Body"]
    entries = []

    for i, text in enumerate(labels[:-1]):
        tk.Label(win, text=text).grid(row=i, column=0)
        entry = tk.Entry(win, width=40, show="*" if text=="Password" else None)
        entry.grid(row=i, column=1)
        entries.append(entry)

    tk.Label(win, text="Body:").grid(row=6, column=0)
    text_body = tk.Text(win, height=10, width=40)
    text_body.grid(row=6, column=1)

    def send_btn():
        try:
            send_email(
                username=entries[2].get(),
                password=entries[3].get(),
                to_addr=entries[4].get(),
                subject=entries[5].get(),
                body=text_body.get("1.0", tk.END),
                smtp_server=entries[0].get(),
                smtp_port=int(entries[1].get())
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    tk.Button(win, text="Send", command=send_btn).grid(row=7, column=0, columnspan=2)

def read_email_window():
    win = tk.Toplevel()
    win.title("Read Latest Email (IMAP)")

    labels = ["IMAP Server", "Port", "Username", "Password"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text).grid(row=i, column=0)
        entry = tk.Entry(win, width=40, show="*" if text=="Password" else None)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def fetch_btn():
        try:
            read_latest_email(
                username=entries[2].get(),
                password=entries[3].get(),
                imap_server=entries[0].get(),
                imap_port=int(entries[1].get())
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    tk.Button(win, text="Fetch", command=fetch_btn).grid(row=4, column=0, columnspan=2)

def main_gui():
    root = tk.Tk()
    root.title("Simple Email Client")

    tk.Button(root, text="Send Email", width=30, command=send_email_window).pack(pady=10)
    tk.Button(root, text="Read Latest Email", width=30, command=read_email_window).pack(pady=10)
    tk.Button(root, text="Exit", width=30, command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
