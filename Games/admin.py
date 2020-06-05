from django.contrib import admin
from Games.models import Games, AddS3File
from django.utils.safestring import mark_safe

admin.site.register(Games)


@admin.register(AddS3File)
class AddS3FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'audio_file_player')
    readonly_fields = [
        'file', 'audio_file_player'
    ]

    def audio_file_player(self, obj):
        player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (
            obj.file.url)
        return mark_safe( player_string )

    audio_file_player.short_description = 'Player'