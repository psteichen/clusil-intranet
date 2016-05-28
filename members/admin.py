from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
class MemberAdmin(ImportExportModelAdmin):
    pass

from import_export.admin import ImportExportActionModelAdmin
#class MemberAdmin(ImportExportActionModelAdmin):
#    pass

from .models import Address, Organisation, Member, Role
admin.site.register(Address)
admin.site.register(Organisation)
admin.site.register(Member)
admin.site.register(Role)


