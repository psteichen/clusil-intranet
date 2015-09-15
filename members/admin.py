from django.contrib import admin

from .models import Address, Organisation, Member, Role

admin.site.register(Address)
admin.site.register(Organisation)
admin.site.register(Member)
admin.site.register(Role)
