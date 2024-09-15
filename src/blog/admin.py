from django.contrib import admin

from .models import Albom, BlogCategory, BlogPost, Comment, File_Album, Like

# Register your models here.


admin.site.register(Albom)
admin.site.register(File_Album)
admin.site.register(BlogCategory)
admin.site.register(Like)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_top", "category", "status")


admin.site.register(BlogPost, BlogPostAdmin)

# -------------------------------------------------------------


class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_reply", "date_created", "status")


admin.site.register(Comment, CommentAdmin)
