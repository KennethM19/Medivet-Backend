import uuid
from urllib.parse import urlparse, unquote

from google.cloud import storage

import config

client = storage.Client.from_service_account_json(config.FIREBASE_CREDENTIALS)
bucket = client.bucket(config.BUCKET_NAME)

def upload_user_image_to_firebase(contents: bytes, filename: str) -> str:
    blob = bucket.blob(f"user_photos/{uuid.uuid4()}_{filename}")
    blob.upload_from_string(contents, content_type="image/jpeg")
    return blob.public_url

def upload_pet_image_to_firebase(contents: bytes, filename: str) -> str:
    blob = bucket.blob(f"pet_photos/{uuid.uuid4()}_{filename}")
    blob.upload_from_string(contents, content_type="image/jpeg")
    return blob.public_url

def delete_photo_from_firebase(public_url: str):
    parsed_url = urlparse(public_url)
    path = unquote(parsed_url.path)
    parts = path.split("/", 2)
    blob_name = parts[2] if len(parts) > 2 else path.lstrip("/")

    blob = bucket.blob(blob_name)
    blob.delete()