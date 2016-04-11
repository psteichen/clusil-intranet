from django.contrib import admin

from .models import Meeting_Attendance, Event_Attendance, MtoM, EtoM

admin.site.register(Meeting_Attendance)
admin.site.register(MtoM)
admin.site.register(Event_Attendance)
admin.site.register(EtoM)
