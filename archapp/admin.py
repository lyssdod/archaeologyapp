from django.contrib import admin
from django.db.models import Sum, Count, Case, When, IntegerField
from .models import Site, Filter, Property

class PropertyAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'oftype', 'instance', 'linked')
	list_editable = ('linked', 'oftype', 'instance')
	list_filter = ('instance', 'linked', 'oftype')

class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_count', 'prop_count')

    def get_queryset(self, request):
        return super(FilterAdmin, self).get_queryset(request).annotate(
            num_props = Count(Case(When(property__linked = False, then = 1), output_field = IntegerField())),
            num_linkd = Count(Case(When(property__linked = True, then = 1), output_field = IntegerField()))
            )

    def prop_count(self, obj):
        return obj.num_props

    def link_count(self, obj):
        return obj.num_linkd

    prop_count.short_description = 'Used by'
    prop_count.admin_order_field = 'num_links'

    link_count.short_description = 'Subfilters'
    link_count.admin_order_field = 'num_props'


admin.site.register(Site)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Filter, FilterAdmin)
