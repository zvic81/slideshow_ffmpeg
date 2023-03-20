'''
functions for upload/download to google cloud platform firebase storage. For authentification to access firebase use private key secret-key-firebase
in secret manager.
for acces my pc to secret manager:
gcloud auth application-default login
'''
from firebase_admin import credentials, initialize_app, storage
from google.cloud import secretmanager
import google_crc32c
import json
import logging
from pathlib import Path

# bucket where stores private key
STORAGE_BUCKET_LONG = 'test1-de41b.appspot.com'
STORAGE_BUCKET_SHORT = 'test1-de41b'  # bucket where stores private key
PROJECT_SECRET_ID = '175712151730'
SECRET_NAME = 'secret-key-firebase'
logger = logging.getLogger("app.main.gcp")


def access_secret_version(project_id, secret_id, version_id='latest'):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    # Verify payload checksum.
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("func <access_secret_version>: Data corruption detected.")
        return response

    payload = response.payload.data.decode("UTF-8")
    # print("Plaintext: {}".format(payload))
    print("<access_secret_version> successfull")
    return payload


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


secret_locations = '/secrets/key_firebase'
with open(secret_locations) as f:
    SECRET = f.readlines()
try:
    print('SECRET READ ::: ', SECRET)
except Exception as e:
    print("ERROR ", e)


# dic = json.loads(access_secret_version(PROJECT_SECRET_ID, SECRET_NAME))
# print(dic)
# cred = credentials.Certificate(dic)
# initialize_app(cred, {'storageBucket': STORAGE_BUCKET_LONG})
print(f'initialize_app succesfull for {STORAGE_BUCKET_LONG}')
# upload_blob('cloudbuild.yaml', 'cloudbuild.yaml')
# download_blob('cloudbuild.yaml', 'cloudbuild_download.yaml')
