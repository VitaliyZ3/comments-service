from django.urls import path
from .consumers import (
    MainPageCommentConsumer,
    ChildCommentsConsumer
)


websocket_patterns = [
    path('ws/main-comments/', MainPageCommentConsumer.as_asgi()),
    path('ws/child-comments/<id>', ChildCommentsConsumer.as_asgi())
]
