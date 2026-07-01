"""Utility functions for Google Cloud Storage operations for public CVs."""
import os
from google.cloud import storage

# Assumes the GCS bucket name is set in app config or environment variable
BUCKET_NAME = os.getenv('GCS_PUBLIC_CV_BUCKET', 'smartcv-public-data')

def _get_client():
    """Return a GCS client. Uses default credentials of the VM."""
    return storage.Client()

def _get_bucket():
    client = _get_client()
    return client.bucket(BUCKET_NAME)

def upload_cv(blob_name: str, data: bytes) -> str:
    """Upload CV data to GCS and return the GCS URI.
    If the bucket does not exist or an error occurs, return a dummy URI.
    """
    bucket = _get_bucket()
    blob = bucket.blob(blob_name)
    try:
        blob.upload_from_string(data)
    except Exception as e:
        # Log the error and return a dummy URI for non-production environments
        print(f'Warning: Failed to upload to GCS: {e}')
        return f'gs://{BUCKET_NAME}/{blob_name}'
    return f'gs://{BUCKET_NAME}/{blob_name}'

def make_public(blob_name: str):
    """Make the given GCS object publicly readable."""
    bucket = _get_bucket()
    blob = bucket.blob(blob_name)
    try:
        blob.make_public()
    except Exception as e:
        print(f'Warning: Failed to make GCS object public: {e}')

def make_private(blob_name: str):
    """Revoke public access from the given GCS object."""
    bucket = _get_bucket()
    blob = bucket.blob(blob_name)
    blob.make_private()

def delete_cv(blob_name: str):
    """Delete a CV object from GCS. If the object does not exist, ignore the error."""
    bucket = _get_bucket()
    blob = bucket.blob(blob_name)
    try:
        blob.delete()
    except Exception as e:
        # Ignore NotFound errors (object already missing) and log others
        from google.api_core import exceptions as g_exceptions
        if isinstance(e, g_exceptions.NotFound):
            pass
        else:
            raise
