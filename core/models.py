from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from .service import UUIDFileStorage
import bleach


class Comment(models.Model):
    """
    This class represents a comment.
    """
    user_creator = models.ForeignKey(User, related_name="comment", db_index=True, null=False,
                                     on_delete=models.DO_NOTHING)
    text = models.TextField("Comment text")
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False, db_index=True)
    files = models.ManyToManyField("AttachedFile", blank=True, related_name="comment", verbose_name="Attached files")
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, related_name="child", verbose_name="Parent comment"
    )
    main_parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Main Parent comment"
    )

    def __str__(self):
        return self.text

    @property
    def cleaned_text(self):
        allowed_tags = ['a', 'code', 'i', 'strong']
        return bleach.clean(self.text, tags=allowed_tags)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['user_creator'])
        ]
        ordering = ["-id"]


class AttachedFile(models.Model):
    """
    This class represents a attached file.
    """
    name = models.CharField(max_length=150, blank=True, verbose_name="File name")
    image_src = models.FileField(storage=UUIDFileStorage(), max_length=156, blank=True, verbose_name="Image")
    image_mini_src = models.FileField(storage=UUIDFileStorage(is_miniature=True), max_length=156, blank=True,
                                      verbose_name="")
    file_src = models.FileField(storage=UUIDFileStorage(is_document=True), max_length=156, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.image_src != "":
            self.name = self.image_src
        super().save(*args, **kwargs)

    def check_file(self):
        if self.file_src.name.split(".")[-1] != "pdf":
            return True
        return False

    class Meta:
        verbose_name = "Files attached to comment"


# function to submit a task to celery for future sending to websocket
@receiver(post_save, sender=Comment)
def send_event_to_comment(sender, instance, **kwargs):
    from . import tasks
    is_child = instance.main_parent is not None

    group_id = 0 if instance.main_parent is None else instance.main_parent.id

    if kwargs['created']:
        event_type = "CREATED"
    else:
        event_type = "UPDATED"

    tasks.send_created_comment.delay(group_id, instance.id, is_child, event_type)

