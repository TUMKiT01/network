import imaplib
from datetime import date
import email
from email.header import decode_header
from sqlite3 import Time
#ข้อมูลบัญชี
username = "dumtumkit@gmail.com"
password = "biwliwvnfgocfkgi"
imap_server = "imap.gmail.com"

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

            else:
                # แยกประเภทเนื้อหาของอีเมล
                content_type = msg.get_content_type()
                # รับเนื้อหาอีเมล
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # พิมพ์เฉพาะส่วนข้อความอีเมล
                    print(body)

            print("="*100)
# ปิดการเชื่อมต่อและออกจากระบบ
imap.close()
imap.logout()