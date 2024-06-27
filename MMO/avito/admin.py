from django.contrib import admin
from django.utils.safestring import mark_safe

from avito.models import Post, Message

# admin.site.register(Post)
# admin.site.register(Message)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'category', 'text', 'photo','post_photo', 'author']
    readonly_fields = ['post_photo']
    list_display = ['id','title', 'category','create_date', 'text', 'post_photo']
    list_display_links = ['title', 'text']
    ordering = ['-create_date', 'title']
    list_editable = ['category']

    @admin.display(description='Фото')
    def post_photo(selfself, post: Post):
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' width=50>")
        return 'Без фото'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','author', 'post','status', 'text', 'create_date']
    list_display_links = ['id','author', 'post']
    ordering = ['-create_date', 'text']
# admin.site.register(Post,PostAdmin)