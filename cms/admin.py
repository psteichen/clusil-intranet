from django.contrib import admin
from cms.models import LdapGroup, LdapUser

class LdapGroupAdmin(admin.ModelAdmin):
    exclude = ['dn']
    list_display = ['name', 'members']
    search_fields = ['name', 'members']


class LdapUserAdmin(admin.ModelAdmin):
    exclude = ['dn']
    list_display = ['username', 'first_name', 'last_name', 'email' ,'password']
    search_fields = ['first_name', 'last_name', 'username']

admin.site.register(LdapGroup, LdapGroupAdmin)
admin.site.register(LdapUser, LdapUserAdmin)
