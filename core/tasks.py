from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from .serializers import CommentCreateSerializer
from .models import Comment


# function to send a comment creation/update notification to ws connection
@shared_task
def send_created_comment(group_id: int, comment_id: int, is_child: bool, event_type: str):
    layer = get_channel_layer()
    if is_child:
        group_name = f"child_comments_{group_id}"
    else:
        group_name = f"main_comments"
    comment = Comment.objects.get(id=comment_id)
    serializer = CommentCreateSerializer(comment)
    async_to_sync(layer.group_send)(
        group=group_name,
        message={
            "type": "send_comment",
            "message": serializer.data,
            "event_type": event_type
        }
    )
    return True
