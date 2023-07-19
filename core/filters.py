from django_filters import rest_framework as filters
from .models import Comment


class CommentFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('user_creator__username', 'username'),
            ('user_creator__email', 'email'),
            ('timestamp', 'timestamp'),
        ),
    )

    class Meta:
        model = Comment
        fields = []
