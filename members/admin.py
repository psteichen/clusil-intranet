from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
class MemberAdmin(ImportExportModelAdmin):
    pass

from import_export.admin import ImportExportActionModelAdmin
#class MemberAdmin(ImportExportActionModelAdmin):
#    pass

class AddressAdmin(admin.ModelAdmin):
  list_display = ('street', 'postal_code', 'town', 'gen_country',)

class OrgAdmin(admin.ModelAdmin):
  list_display = ('name',)

class MemberAdmin(admin.ModelAdmin):
  list_display = ('gen_name', 'nb_users',)


from .models import Address, Organisation, Member, Role, Renew
admin.site.register(Address, AddressAdmin)
admin.site.register(Organisation, OrgAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Role)
admin.site.register(Renew)


