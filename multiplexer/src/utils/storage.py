from google.cloud import storage
from google.oauth2 import service_account

from src import GCP_PROJECT, GCP_STORAGE_JSON, GCP_STORAGE_BUCKET_NAME


credentials = service_account.Credentials.from_service_account_file(GCP_STORAGE_JSON)
storage_client = storage.Client(project=GCP_PROJECT, credentials=credentials)
bucket = storage_client.get_bucket(GCP_STORAGE_BUCKET_NAME)


def upload_image(correlation_id, image_path):
    """
    Uploads an image into the GCP bucket publicly.
    :param correlation_id: Correlation ID for given a name to the remote file.
    :param image_path: Local image path.
    :return: GCP public URL pointing to the image.
    """
    blob = bucket.blob('{}.png'.format(correlation_id))
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url
