from django.contrib import admin
from .models import Post, Comment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published', 'status')
    list_editable = ('author', 'status')
    list_filter = ('author', 'status')
    search_fields = ('title',)
    ordering = ('-published', 'status')
    date_hierarchy = 'published'
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'created', 'active')
    list_filter = ('active', 'post')
    list_editable = ('active',)
    ordering = ('-created', 'active')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
