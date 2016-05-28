from django.contrib import admin

from .models import Event, Invitation

admin.site.register(Event)
admin.site.register(Invitation)
