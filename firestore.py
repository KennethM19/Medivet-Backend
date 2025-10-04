import json

import firebase_admin
from firebase_admin import credentials, firestore
import config

cred_dict = json.loads(config.FIREBASE_CREDENTIALS)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {})
db_firestore = firestore.client()