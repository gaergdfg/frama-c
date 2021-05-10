from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Directory)
admin.site.register(File)
admin.site.register(SectionCategory)
admin.site.register(Status)
admin.site.register(StatusData)
admin.site.register(FileSection)
