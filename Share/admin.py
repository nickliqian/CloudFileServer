from django.contrib import admin
from Share.models import Upload


class UploadAdmin(admin.ModelAdmin):
    list_display = ("DownloadDocount", "code",  "Datatime", "path", "name", "Filesize", "PCIP")


admin.site.register(Upload, UploadAdmin)
