
import smtplib
gmail_user = 'postmaster@sandboxf641a49b349c471c91c3595bbb9e949f.mailgun.org'
gmail_password = '3f6bd1b2293e7172ebc3d9bdee1c48be-523596d9-31cf9343'
sent_from = 'chanwieng757@gmail.com'
to = ['dumtumkit@gmail.com']
message= 'test smtp test sent email'


try:
    smtp_server = smtplib.SMTP('smtp.mailgun.org',587)
    smtp_server.ehlo()
    smtp_server.login(gmail_user,gmail_password)
    smtp_server.sendmail(sent_from,to,message)
    smtp_server.close()
    print('Email sent successfully!')
except Exception as ex:
    print('Something went wrong',ex)
