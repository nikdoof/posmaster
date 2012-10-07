from django.contrib import admin
from poscore.models.objects import Tower, InSpaceObject, Fuel
from poscore.models.api import APIKey

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['keyid', 'vcode', 'active']
admin.site.register(APIKey, APIKeyAdmin)

class FuelInlineAdmin(admin.TabularInline):
    model = Fuel
    list_display = ['resource', 'level', 'updated_datetime']
 
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False 

class TowerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']
    list_filter = ['state']
    readonly_fields = ['id', 'type', 'owner', 'system', 'x', 'y', 'z', 'state', 'moon']

    inlines = [
        FuelInlineAdmin,
    ]
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Tower, TowerAdmin)

class InSpaceObjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'system']
    list_filter = ['type__name']

admin.site.register(InSpaceObject, InSpaceObjectAdmin)