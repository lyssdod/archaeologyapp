from django.contrib import admin
from django.db.models import Count
from .models import Site, Filter, Property

class PropertyAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'oftype', 'instance', 'linked')
	list_editable = ('linked', 'oftype', 'instance')
	list_filter = ('instance', 'linked', 'oftype')

class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'prop_count', 'linked_count')

    def get_queryset(self, request):
        return super(FilterAdmin, self).get_queryset(request).annotate(num_props = Count('property'))#.filter(property__linked = True)

    def prop_count(self, obj):
        return obj.num_props

    def linked_count(self, obj):
        return 'Not Implemented Yet'
        #return Filter.objects.filter(property__linked = True).annotate(Count('property'))

    prop_count.short_description = 'Subfilters'
    prop_count.admin_order_field = 'num_props'

#class FilterAdmin(admin.ModelAdmin):
#	list_display = ('name', 'get_size')

#	def get_size(self, obj):
#		return Property.
    #def get_queryset(self, request):
    #	return super(FilterAdmin, self).get_queryset(request).filter(linked = True).select_related('filter')


admin.site.register(Site)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Filter, FilterAdmin)
