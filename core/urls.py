from django.urls import path
from .views import (
    CommentCreate,
    CommentList,
    CommentDetail,
    CommentUpdate,
    UserCreate,
    CommentDelete,
    AddFile
)

urlpatterns = [
    path("comment-update/<id>", CommentUpdate.as_view(), name="update_comment"),
    path("comment-detail/<id>", CommentDetail.as_view(), name="comment_detail"),
    path("comment-delete/<id>", CommentDelete.as_view(), name="comment_delete"),
    path("comment-create/", CommentCreate.as_view(), name="create_comment"),
    path("comments-list/", CommentList.as_view(), name="comments-list"),
    path("user-create/", UserCreate.as_view(), name="user_create"),
    path("add-file/", AddFile.as_view(), name="add_file")
]