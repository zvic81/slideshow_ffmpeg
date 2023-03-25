'''
functions for upload/download to google cloud platform firebase storage.
'''
from firebase_admin import credentials, initialize_app, storage
import json
import logging
from pathlib import Path
import datetime

# bucket where stores private key
STORAGE_BUCKET_LONG = 'test1-de41b.appspot.com'
SECRET_LOCATION = '/secrets/secret-key-firebase'

logger = logging.getLogger("app.main.gcp")


def upload_blob(source_file_name: str, destination_file_name: str, bucket_name=STORAGE_BUCKET_LONG):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)
    logger.info("upload_blob %s", blob.public_url)
    return 0


def download_blob(source_blob_name: str, destination_file_name: str, bucket_name=STORAGE_BUCKET_LONG):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    logger.info('download_blob %s succesfull to %s',
                source_blob_name, destination_file_name)
    return 0


def generate_signed_url(blob_name, bucket_name=STORAGE_BUCKET_LONG):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        # This URL is valid for 1 hour
        expiration=datetime.timedelta(hours=1),
        # Allow GET requests using this URL.
        method="GET",
    )
    return url

dic = []
try:
    with open(SECRET_LOCATION) as f:
        dic = json.loads(f.read())
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
except:  # handle other exceptions such as attribute errors
    print("Unexpected error:", sys.exc_info()[0])
# print(dic)
if dic:
    cred = credentials.Certificate(dic)
    initialize_app(cred, {'storageBucket': STORAGE_BUCKET_LONG})
    print(f'Initialize_app succesfull for {STORAGE_BUCKET_LONG}')
else:
    print(f'Initialize_app ERROR for {STORAGE_BUCKET_LONG}')
