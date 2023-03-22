'''
functions for upload/download to google cloud platform firebase storage. 
'''
from firebase_admin import credentials, initialize_app, storage
# from google.cloud import secretmanager
# import google_crc32c
import json
import logging
from pathlib import Path
import datetime


# bucket where stores private key
STORAGE_BUCKET_LONG = 'test1-de41b.appspot.com'
STORAGE_BUCKET_SHORT = 'test1-de41b'  # bucket where stores private key
SECRET_LOCATION = '/secrets/secret-key-firebase'
# PROJECT_SECRET_ID = '175712151730'
# SECRET_NAME = 'secret-key-firebase'
logger = logging.getLogger("app.main.gcp")


# def access_secret_version(project_id, secret_id, version_id='latest'):
#     """
#     Access the payload for the given secret version if one exists. The version
#     can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
#     """
#     # Create the Secret Manager client.
#     client = secretmanager.SecretManagerServiceClient()
#     # Build the resource name of the secret version.
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
#     # Access the secret version.
#     response = client.access_secret_version(request={"name": name})
#     # Verify payload checksum.
#     crc32c = google_crc32c.Checksum()
#     crc32c.update(response.payload.data)
#     if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
#         print("func <access_secret_version>: Data corruption detected.")
#         return response

#     payload = response.payload.data.decode("UTF-8")
#     # print("Plaintext: {}".format(payload))
#     print("<access_secret_version> successfull")
#     return payload


def upload_blob(source_file_name: str, destination_file_name: str, bucket_name=STORAGE_BUCKET_LONG):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)
    # # Opt : if you want to make public access from the URL
    # blob.make_public()
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
    # storage_client = storage.Client()
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        # This URL is valid for 1 hour
        expiration=datetime.timedelta(hours=1),
        # Allow GET requests using this URL.
        method="GET",
    )

    # print(f"The signed url for {blob.name} is {url}")
    return url
# import glob
# print(glob.glob("/*"))
# print(glob.glob("/secrets/*"))
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

# generate_signed_url(STORAGE_BUCKET_LONG,
#                     'd983c82f8f4f40df8be8c4b2c65d5786ab211214a0fa47c3ba969a1e2522998d81af234d61c643a38ca9df4d7cdb84d4307b7f9ec02b4157aaa06ea94af8f060.mpg')
