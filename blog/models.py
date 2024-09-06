from django.conf import settings
from django.db import models
from django.utils import timezone as tz

class Post(models.Model):

    
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PULBISHED = "PB", "Published"
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            related_name = "blog_posts")
    body = models.TextField()
    publish = models.DateField(default=tz.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    status = models.CharField(
            max_length = 2,
            choices = Status,
            default = Status.DRAFT)
    
    class Meta:
        ordering = [ "-publish" ]
        indexes = [
                    models.Index(fields=["-publish"]),
                ]

    def __str__(self):
        return f"{self.title}"
