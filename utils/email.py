import os
import random
import string

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from pydantic import SecretStr, EmailStr

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=SecretStr(os.getenv("MAIL_PASSWORD","")),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT", cast=int),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_TLS=os.getenv("MAIL_TLS", cast=bool),
    MAIL_SSL=os.getenv("MAIL_SSL", cast=bool),
    USE_CREDENTIALS=True,
)

def generate_verification_code(length=5):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

async def send_verification_email(email: EmailStr, code: str):
    subject = "Código de verificación - PetHealth"
    html = f"""
    <h2>¡Bienvenido a PetHealth!</h2>
    <p>Tu código de verificación es: <b>{code}</b></p>
    <p>Este código expira en 10 minutos.</p>
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=html,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)