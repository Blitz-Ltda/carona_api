from app.shared.config import settings
from email.mime.text import MIMEText
import smtplib
import ssl

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD

    def send_email(self, to_address: str, subject: str, body: str) -> bool:
        msg = MIMEText(body, 'html', 'utf-8')
        msg['From'] = self.username
        msg['To'] = to_address
        msg['Subject'] = subject

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.sendmail(self.username, to_address, msg.as_string())
            print(f"E-mail enviado para {to_address}")
            return True
        except Exception as e:
            print(f"Falha ao enviar e-mail: {e}")
            return False
