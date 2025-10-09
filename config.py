import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS')

SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60