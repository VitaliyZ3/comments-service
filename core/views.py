import sys
from io import BytesIO
from PIL import Image

# django imports
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile
)
# drf imports
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework import permissions

# apps imports
from .service import CommentListPagination
from .models import (
    Comment,
    AttachedFile
)
from .serializers import (
    CommentCreateSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
    UserSerializer
)



class CommentCreate(generics.CreateAPIView):
    """
    View for creating comment object
    """
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentUpdate(generics.UpdateAPIView):
    """
    View for updating comment object
    """
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = "id"


class CommentDetail(generics.RetrieveAPIView):
    """
    View for view a list of child comments of the same parent
    """
    queryset = Comment.objects.prefetch_related('files', 'child')  # solving n+1 problem
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentDetailSerializer
    lookup_field = "id"


class CommentDelete(generics.DestroyAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    """
    View for creating user
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer


class CommentList(generics.ListAPIView):
    """
    View for list of comments objects,
    with sorting, pagination and ordering
    """
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentListSerializer
    pagination_class = CommentListPagination
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user_creator__username", "user_creator__email", "timestamp"]
    ordering_fields = ["user_creator__username", "user_creator__email", "timestamp"]

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get("ordering", None)

        if ordering == "username":
            queryset = queryset.order_by("user_creator__username")
        if ordering == "email":
            queryset = queryset.order_by("user_creator__email")
        return queryset

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class AddFile(APIView):
    """
    View for attaching file to comment object
    """
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        uploaded_file = request.FILES["file"]

        comment_id = request.POST.get("comment_id")
        comment = Comment.objects.get(id=comment_id)

        content_type = uploaded_file.content_type.split("/")
        file_extention = uploaded_file.name.split(".")[1]
        supported_image_extensions = ["jpg", "gif", "png", "jpeg"]

        if content_type[1] in supported_image_extensions and file_extention in supported_image_extensions:
            # block for images
            compressed_image = AddFile.image_compression(image=uploaded_file)
            return AddFile.save_file(
                comment=comment,
                image=uploaded_file,
                compressed_image=compressed_image,
            )

        elif content_type[0] == "text" and file_extention == "txt":
            # block for txt files
            if uploaded_file.size > 1000:
                return JsonResponse({
                    "data": "error",
                    "text": "File size bigger than 1 kb"
                })
            return AddFile.save_file(
                comment=comment,
                user=request.user,
                document=uploaded_file,
            )

        return JsonResponse({
            "data": "error",
            "text": "File type is not supported"
        })

    @staticmethod
    def calculate_size(size: tuple[int, int]) -> tuple[int, int]:
        width, height = size
        ratio = min(320 / width, 240 / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return new_width, new_height

    @staticmethod
    def image_compression(image: TemporaryUploadedFile) -> InMemoryUploadedFile:
        im = Image.open(image)
        output = BytesIO()
        new_size = AddFile.calculate_size(im.size)
        im = im.resize(new_size)
        image_format = image.content_type.split("/")[1].upper()
        im.save(output, format=image_format, quality=90)
        output.seek(0)

        return InMemoryUploadedFile(output, "ImageField", f"{image._name.split('.')[0]}.jpg", "image/jpeg",
                                    sys.getsizeof(output), None)

    @staticmethod
    def save_file(comment: Comment, document: str = "", image: str = "", compressed_image: str = ""):
        new_file = AttachedFile.objects.create(
            file_src=document,
            image_src=image,
            image_mini_src=compressed_image,
        )
        comment.files.add(new_file)
        return JsonResponse({"file_data": {"id": new_file.id, "title": f"{document}{image}"}})



