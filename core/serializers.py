from rest_framework import serializers
from .models import (
    Comment,
    User
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "user_creator", "text", "files", "parent", "main_parent")


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentDetailSerializer(serializers.ModelSerializer):
    child = RecursiveSerializer(many=True)

    class Meta:
        model = Comment
        fields = "__all__"


class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
