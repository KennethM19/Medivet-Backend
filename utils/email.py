import os
import random
import string

from decouple import config
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from pydantic import SecretStr, EmailStr

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME"),
    MAIL_PASSWORD=SecretStr(os.getenv("MAIL_PASSWORD","")),
    MAIL_FROM=config("MAIL_FROM"),
    MAIL_PORT=config("MAIL_PORT", cast=int),
    MAIL_SERVER=config("MAIL_SERVER"),
    MAIL_TLS=config("MAIL_TLS", cast=bool),
    MAIL_SSL=config("MAIL_SSL", cast=bool),
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