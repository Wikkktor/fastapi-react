import os
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi import BackgroundTasks
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        self.conf: ConnectionConfig = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=os.getenv("MAIL_PORT"),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER="./templates/email/",
        )
        self.fast_mail: FastMail = FastMail(self.conf)

    def send_email(
        self,
        subject: str,
        recipients: list[str],
        template_name: str,
        background_tasks: BackgroundTasks,
        template_body: dict = None,
    ) -> True:
        """
        Send an email using FastAPI Mail.
        """
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body=template_body,
            subtype="html",
        )
        background_tasks.add_task(
            self.fast_mail.send_message, message, template_name=template_name
        )
        return True

    def send_test_email(self, email: str, background_tasks: BackgroundTasks) -> True:
        """
        Send a test email to the specified recipient.
        """
        return self.send_email(
            subject="Test email",
            recipients=[email],
            template_name="blank.html",
            background_tasks=background_tasks,
        )
