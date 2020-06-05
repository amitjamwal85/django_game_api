from django.contrib import admin

from Webapp.models import Posts


@admin.register(Posts)
class AddS3FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'text', 'published_at', 'updated', 'status')