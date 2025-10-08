import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS')