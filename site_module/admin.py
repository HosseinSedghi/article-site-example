from django.contrib import admin

from site_module.models import SiteSetting, Links, LinkBoxes

# Register your models here.


class LinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'box']

admin.site.register(SiteSetting)
admin.site.register(Links, LinksAdmin)
admin.site.register(LinkBoxes)