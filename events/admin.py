from django.contrib import admin

from .models import Event, Invitation, Partner, Distribution, Participant

admin.site.register(Event)
admin.site.register(Partner)
admin.site.register(Invitation)
admin.site.register(Distribution)
admin.site.register(Participant)
