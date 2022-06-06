import os
from abc import ABC, abstractmethod

from minio import Minio


class FileStorage(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def save_file(self, filepath: str, destination: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def download_file(self, directory: str, key: str, destination: str):
        raise NotImplementedError()

    @abstractmethod
    def fetch_file_content(self, directory: str, key: str) -> bytes:
        raise NotImplementedError()


class MinioStorage(FileStorage):

    def __init__(self, client: Minio):
        super().__init__()

        self.client = client

    def save_file(self, filepath: str, destination: str) -> str:
        splits = destination.split(os.sep)

        bucket = splits[0]

        self._ensure_bucket(bucket)

        filename = os.path.basename(filepath)

        destination = "/".join(splits[1:]) if len(splits) > 1 else ''

        res = self.client.fput_object(
            bucket, destination + "/" + filename, filepath,
        )

        return res.object_name

    def _ensure_bucket(self, bucket: str):
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    def download_file(self, directory: str, key: str, destination: str) -> str:
        splits = directory.split(os.sep)

        bucket = splits[0]

        data = self.client.get_object(bucket, key).data

        with open(destination, 'wb') as f:
            f.write(data)

    def fetch_file_content(self, directory: str, key: str) -> bytes:
        splits = directory.split(os.sep)

        bucket = splits[0]

        return self.client.get_object(bucket, key).data
