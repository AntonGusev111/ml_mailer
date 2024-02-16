import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import re
from config import mail_pass, mail_address, imap_server, smtp_server
import quopri


async def checkMail() -> list:
    try:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(mail_address, mail_pass)
        imap.select("INBOX")
        mail_num = imap.search(None, "UNSEEN")[1][0]
        if len(mail_num) > 0:
            msg = imap.fetch(((mail_num.decode()).split())[-1], '(RFC822)')
            msg_obj = email.message_from_bytes(msg[1][0][1])
            data_from_mail = []
            for part in msg_obj.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    data_from_mail.append(clean_body(get_body(part)))
            imap.logout()
            incomings = str(msg_obj['From']).split(' ')
            data_from_mail.append(incomings[1].replace('<', '').replace('>', ''))
            data_from_mail[0] = clean_body(data_from_mail[0])
            return data_from_mail
    except Exception as e:
        pass


def get_body(part):
    if part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] in ("binary", "8bit", "7bit", None):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:
        return part.get_payload()


def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None


def clean_body(text=str) -> str:
    reg = re.compile('[^а-яА-я a-zA-Z 0-9 / . \n]')
    return (reg.sub('', text))


def mail_send(letter_obj: dict) -> None:
    smtp_ser = smtplib.SMTP(smtp_server)
    smtp_ser.starttls()
    smtp_ser.login(mail_address, mail_pass)
    msg = MIMEMultipart()
    msg["From"] = mail_address
    msg["To"] = letter_obj[1]
    msg["Subject"] = "ответ на письмо"
    text = letter_obj[0]
    msg.attach(MIMEText(text, "plain"))
    smtp_ser.sendmail(mail_address, letter_obj[1], msg.as_string())
