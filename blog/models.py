from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone as tz

class PublishedManager(models.Manager):

    def get_queryset(self):
        return (
                super().get_queryset().filter(status=Post.Status.PULBISHED)
                )



class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PULBISHED = "PB", "Published"
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(
            max_length=250,
            unique_for_date="publish")
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
    
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = [ "-publish" ]
        indexes = [
                    models.Index(fields=["-publish"]),
                ]

    def __str__(self):
        return f"{self.title}"

    
    def get_absolute_url(self):
        print(f"Returning absolute url...")
        return reverse(
                'blog:post_detail',
                args=[
                    self.publish.year,
                    self.publish.month,
                    self.publish.day,
                    self.slug
                    ]
                )



class Coment(models.Model):
    post = models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            related_name="comments"
            )

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = [ 'created' ]
        indexes = [
                models.Index(fields=['created'])
                ]