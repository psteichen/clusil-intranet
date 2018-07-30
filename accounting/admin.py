from django.contrib import admin

from .models import Fee

class FeeAdmin(admin.ModelAdmin):
  list_display = ('get_member', 'year', 'paid', 'paid_date',)

admin.site.register(Fee, FeeAdmin)
