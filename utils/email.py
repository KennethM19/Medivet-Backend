import os
import random
import string

from dotenv import load_dotenv
from pydantic import EmailStr
from sendgrid import Mail, SendGridAPIClient

load_dotenv()

SENDGRID_API_KEY = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

def generate_verification_code(length=5):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

async def send_verification_email(email: EmailStr, code: str):
    message = Mail(
        from_email=MAIL_FROM,
        to_emails=email,
        subject="Código de verificación - MediVet",
        html_content=f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h2>Bienvenido a MediVet 🐾</h2>
                <p>Gracias por registrarte. Tu código de verificación es:</p>
                <h3 style="color: #0066CC;">{code}</h3>
                <p>Por favor, ingrésalo en la aplicación para continuar.</p>
                <p style="font-size: 12px; color: #999;">Este código expira en 10 minutos.</p>
            </div>
            """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print(f"✅ Correo enviado correctamente a {email}")
    except Exception as e:
        print(f"❌ Error al enviar correo a {email}: {e}")