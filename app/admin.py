from django.contrib import admin
from app.models import Coment, Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [ "title", "slug", "author", "publish", "status" ]
    list_filter = [ "author", "publish", "status", "created" ]
    search_fields = [ "body", "title" ]
    prepopulated_fields = { "slug": ("title", ) }
    raw_id_fields = [ "author" ]
    date_hierarchy = "publish"
    ordering = [ "status", "publish" ]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Coment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'email', 'post', 'created', 'active' ]
    list_filter = [ 'active', 'created', 'updated' ]
    search_fields = [ 'name', 'email', 'body' ]


