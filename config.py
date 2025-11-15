import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS')
BUCKET_NAME = os.getenv('BUCKET_NAME')

SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
ACCESS_TOKEN_EXPIRE_MINUTES = 60