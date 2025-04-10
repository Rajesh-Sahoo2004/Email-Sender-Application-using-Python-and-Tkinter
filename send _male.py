import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import smtplib
import re
import mimetypes
from email.message import EmailMessage

attachment_path = None

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def clean_text(text):
    return text.replace('\xa0', ' ').strip()

def browse_file():
    global attachment_path
    file_path = filedialog.askopenfilename()
    if file_path:
        attachment_path = file_path
        attachment_label.config(text=f"📎 {file_path.split('/')[-1]}")
    else:
        attachment_path = None
        attachment_label.config(text="No file attached")

def send_email():
    sender = from_entry.get()
    password = password_entry.get()
    recipients_raw = email_entry.get()
    message_content = clean_text(message_box.get("1.0", tk.END))

    if not sender or not password or not recipients_raw or not message_content:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    recipient_list = [email.strip() for email in recipients_raw.split(",") if email.strip()]
    if not all(is_valid_email(email) for email in recipient_list):
        messagebox.showerror("Invalid Email", "One or more recipient email addresses are invalid.")
        return

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Message from Tkinter App'
        msg['From'] = sender
        msg['To'] = ", ".join(recipient_list)
        msg.set_content(message_content, charset='utf-8')

        if attachment_path:
            mime_type, _ = mimetypes.guess_type(attachment_path)
            mime_type = mime_type or 'application/octet-stream'
            main_type, sub_type = mime_type.split('/', 1)

            with open(attachment_path, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype=main_type,
                    subtype=sub_type,
                    filename=attachment_path.split('/')[-1]
                )

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        messagebox.showinfo("Success", f"Email sent to:\n{msg['To']}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email:\n{str(e)}")

# UI setup
root = tk.Tk()
root.title("✉️ Beautiful Email Sender")
root.geometry("520x660")
root.configure(bg="#b3d9ff")

style = ttk.Style()
style.configure("TEntry", padding=5)
style.configure("TButton", font=("Segoe UI", 10, "bold"))

shadow_frame = tk.Frame(root, bg="#a6c9e2", width=480, height=620)
shadow_frame.place(x=20, y=20)

main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
main_frame.place(x=10, y=10, width=480, height=650)

label_font = ("Segoe UI", 11, "bold")
entry_font = ("Segoe UI", 10)
button_font = ("Segoe UI", 10, "bold")

header = tk.Label(main_frame, text="📨 Tkinter Email Sender", font=("Segoe UI", 16, "bold"), bg="white", fg="#0073e6")
header.pack(pady=15)

def label(master, text):
    return tk.Label(master, text=text, bg="white", font=label_font)

label(main_frame, "From Email:").pack(pady=(5, 0))
from_entry = ttk.Entry(main_frame, width=45)
from_entry.pack(pady=5)

label(main_frame, "Password (App Password):").pack(pady=(10, 0))
password_entry = ttk.Entry(main_frame, width=45, show="*")
password_entry.pack(pady=5)

label(main_frame, "Recipient Email(s):\n(Separate multiple emails with commas)").pack(pady=(10, 0))
email_entry = ttk.Entry(main_frame, width=45)
email_entry.pack(pady=5)

label(main_frame, "Message:").pack(pady=(10, 0))
message_box = tk.Text(main_frame, height=8, width=50, font=entry_font, wrap=tk.WORD, bd=1, relief="solid")
message_box.pack(pady=5)

attach_button = tk.Button(main_frame, text="📎 Attach File", command=browse_file, bg="#99ccff", fg="black", font=button_font)
attach_button.pack(pady=(10, 0))

attachment_label = tk.Label(main_frame, text="No file attached", bg="white", fg="gray", font=("Segoe UI", 9))
attachment_label.pack(pady=(3, 10))

# 👇 Send Button - BIGGER SIZE
send_button = tk.Button(main_frame, text="🚀 Send Email", command=send_email,
                        bg="#4da6ff", fg="white", font=("Segoe UI", 12, "bold"),
                        width=35, height=20)
send_button.pack(pady=20)

footer = tk.Label(main_frame, text="Designed by Rajesh Sahoo ❤️", bg="white", fg="#666666", font=("Segoe UI", 9))
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
