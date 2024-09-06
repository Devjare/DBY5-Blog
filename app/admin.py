from django.contrib import admin
from blog.models import Post

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
