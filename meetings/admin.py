from django.contrib import admin

from .models import Meeting, Invitation

admin.site.register(Meeting)
admin.site.register(Invitation)
