from django.contrib import admin

from ESearch.models import Publisher
from .models import PostSearch

admin.site.register(PostSearch)


@admin.register(Publisher)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state_province', 'country', 'website')
    search_fields = ('name',)
    list_filter = ['country', 'website']
    readonly_fields = [
        'name', 'address'
    ]
    # filter_horizontal = ('country', 'website',)

