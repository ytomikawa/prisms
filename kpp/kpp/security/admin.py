from django.contrib import admin

from .models import SecurityCode, Security, SecurityMargin, SecurityPrice

class SecurityAdmin(admin.ModelAdmin):
    pass


admin.site.register(SecurityCode)
admin.site.register(Security, SecurityAdmin)
admin.site.register(SecurityMargin)
admin.site.register(SecurityPrice)

