ERROR_CODES = {
    '001': 'An unspecified error has occurred during request processing.',
    '002': 'Image is not reachable or the URL is invalid.',
    '003': 'Invalid URL or required parameters not specified.'
}
ERROR_CODES_DEFAULT = ERROR_CODES['001']

LARGEST_SIZE_INPUT = 2500

TMP_FOLDER = '/tmp'

GCP_PROJECT = 'object-cut-engine'
GCP_STORAGE_JSON = './keys/google_cloud_storage_access.json'
GCP_STORAGE_BUCKET_NAME = 'object-cut-images'
