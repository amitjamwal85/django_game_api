from django.contrib import admin

from User.models import UserProfile, Post, Comments
from import_export.admin import ImportExportModelAdmin

admin.site.register( UserProfile )


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):

    search_fields = ('user_id',)
    list_filter = ['post_title', 'post_text']
    # readonly_fields = [
    #     'name', 'address'
    # ]

    def comments(self):
        comments = Comments.objects.all()
        for comment in comments:
            if self.id == comment.post.id:
                return comment.comment

    list_display = ('id', 'post_title', 'post_text', 'user_id', comments)
#
#
# @admin.register(Comments)
# class CommentsAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'comment', 'post_id')
#     search_fields = ('post_id',)
#     list_filter = ['post_id']




# class Commentsline(admin.StackedInline):
#     model = Comments
#     extra = 0
#     list_display = ('id', 'comment', 'post_id')
#
#
# class PostCommentAdmin(admin.ModelAdmin):
#     inlines = [
#         Commentsline
#     ]
#     model = Post
#     list_display = ('id', 'post_title', 'post_text', 'user_id')
#     list_per_page = 20
#
#
# admin.site.register(Post, PostCommentAdmin)


