from datetime import datetime
from os import path

from django.core.files.storage import FileSystemStorage
from uuid import uuid4

from rest_framework.pagination import PageNumberPagination


class UUIDFileStorage(FileSystemStorage):
    """
    Class for creating path for uploaded file
    """
    def __init__(self, is_miniature=False, is_document=False, *args, **kwargs):
        self.is_miniature = is_miniature
        self.is_document = is_document
        super().__init__(*args, **kwargs)

    def get_available_name(self, name, max_length=None):
        _, ext = path.splitext(name)
        date = datetime.today().strftime("%Y/%m/%d/")
        if self.is_miniature:
            file_path = "miniature/" + date + uuid4().hex + ext
            return file_path
        elif self.is_document:
            file_path = "document/" + date + uuid4().hex + ext
            return file_path
        else:
            return date + uuid4().hex + ext


class CommentListPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 25
