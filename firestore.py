import firebase_admin
from firebase_admin import credentials, firestore
import config

cred = credentials.Certificate(config.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {})
db_firestore = firestore.client()