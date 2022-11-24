from datetime import date
import imaplib
import email
from email.header import decode_header
from sqlite3 import Time
import webbrowser
import os

#ข้อมูลบัญชี
username = "dumtumkit@gmail.com"
password = "biwliwvnfgocfkgi"
imap_server = "imap.gmail.com"

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)# เครียรข้อความสำหรับสร้างโฟลเดอร์
imap = imaplib.IMAP4_SSL(imap_server)# สร้างคลาส IMAP4 ด้วย SSL
# ตรวจสอบสิทธิ์
imap.login(username, password)
status, messages = imap.select("INBOX")
N = 4# จำนวนอีเมลที่จะเรียก จากใหม่สุด
messages = int(messages[0])
for i in range(messages, messages-N, -1):
    # ดึงข้อความอีเมลโดย ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # แยกวิเคราะห์อีเมลไบต์ลงในวัตถุข้อความ
            msg = email.message_from_bytes(response[1])
            # ถอดรหัสหัวเรื่องอีเมล
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # ถ้าเป็นไบต์ ให้ถอดรหัสเป็น str
                subject = subject.decode(encoding)
            # ถอดรหัสผู้ส่งอีเมล
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            #เวลาที่ส่งมา
            Time, encoding = decode_header(msg.get("date"))[0]
            if isinstance(Time, bytes):
                Time = Time.decode(encoding)
                
            print("Subject: ", subject)
            print("From: ", From)
            print("Time: ",Time)
            # หากข้อความอีเมลเป็นแบบหลายส่วน
            if msg.is_multipart():
                # ทำซ้ำในส่วนอีเมล
                for part in msg.walk():
                    # แยกประเภทเนื้อหาของอีเมล
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # รับเนื้อหาอีเมล
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        print(body)
                    # elif "attachment" in content_disposition:
                    #     # ดาวน์โหลดไฟล์แนบ
                    #     filename = part.get_filename()
                    #     if filename:
                    #         folder_name = clean(subject)
                    #         if not os.path.isdir(folder_name):
                    #             # สร้างโฟลเดอร์สำหรับอีเมลนี้ (ตั้งชื่อตามหัวเรื่อง)
                    #             os.mkdir(folder_name)
                    #         filepath = os.path.join(folder_name, filename)
                    #         # ดาวน์โหลดไฟล์แนบและบันทึก
                    #         open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                # แยกประเภทเนื้อหาของอีเมล
                content_type = msg.get_content_type()
                # รับเนื้อหาอีเมล
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # พิมพ์เฉพาะส่วนข้อความอีเมล
                    print(body)
            # if content_type == "text/html":
            #     # ถ้าเป็น HTML ให้สร้างไฟล์ HTML ใหม่และเปิดในเบราว์เซอร์
            #     folder_name = clean(subject)
            #     if not os.path.isdir(folder_name):
            #         # สร้างโฟลเดอร์สำหรับอีเมลนี้ (ตั้งชื่อตามหัวเรื่อง)
            #         os.mkdir(folder_name)
            #     filename = "index.html"
            #     filepath = os.path.join(folder_name, filename)
            #     # เขียนไฟล์
            #     open(filepath, "w").write(body)
            #     # เปิดในเบราว์เซอร์เริ่มต้น
            #     webbrowser.open(filepath)
            print("="*100)
# ปิดการเชื่อมต่อและออกจากระบบ
imap.close()
imap.logout()