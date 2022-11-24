import imaplib
import email

imap_server = "imap.gmail.com"
email_address = "dumtumkit@gmail.com"
password = "biwliwvnfgocfkgi"

imap = imaplib.IMAP4_SSL(imap_server) 
imap.login(email_address,password) 

imap.select("inbox") 
_,msgnums = imap.search(None, "ALL")
for msgnum in msgnums[0].split():
    _,data = imap.fetch(msgnum,"(RFC822)")#RFC822
    message = email.message_from_bytes(data[0][1]) 

    print(f"Message Number :{msgnum}")
    print(f"From :{message.get('From')}") 
    print(f"To :{message.get('To')}")  
    print(f"BCC :{message.get('BCC')}") 
    print(f"Data :{message.get('Date')}")  
    print(f"Subject :{message.get('Subject')}") 

    print("content :")
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            print(part.as_string)
            print("\n")
imap.close()