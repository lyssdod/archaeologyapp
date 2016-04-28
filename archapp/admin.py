from django.contrib import admin

from .models import Site, Filter, Property

class PropertyAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'oftype', 'instance', 'linked')
	list_editable = ('linked', 'oftype', 'instance')

"""    actions = ['link', ]

    def link(self, request, queryset):
        queryset.update(linked = True)
        self.message_user(request, 'Properties has been linked to their filters')

    link.short_description = 'Use as a sub-filter'
"""

class FilterAdmin(admin.ModelAdmin):
	pass
    #def get_queryset(self, request):
    #	return super(FilterAdmin, self).get_queryset(request).filter(linked = True).select_related('filter')


admin.site.register(Site)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Filter, FilterAdmin)
