import uuid
import boto3

from objects.models.aws_service import S3Object
from objects.requests.aws_service import DeleteImageRequest, UploadImageRequest


class AWSService:
    """
    Service for interacting with AWS.
    """

    def __init__(self) -> None:
        self.s3 = boto3.client("s3")

    def upload_file(self, param: UploadImageRequest) -> S3Object:
        """
        Upload a file to an S3 bucket.

        Parameters
        ----------
        file_path : str
            path to the file
        bucket : str
            bucket name
        object_name : str
            object name

        Returns
        -------
        S3Object
            s3 object
        """
        object_name = uuid.uuid4().hex
        self.s3.upload_file(param.file_path, param.bucket, object_name)

        return S3Object(object_name=object_name, bucket=param.bucket)

    def delete_file(self, param: DeleteImageRequest):
        """
        Delete a file from an S3 bucket.

        Parameters
        ----------
        bucket : str
            bucket name
        object_name : str
            object name
        """
        self.s3.delete_object(Bucket=param.bucket, Key=param.object_name)
