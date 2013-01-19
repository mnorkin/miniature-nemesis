from morbid.models import Feature, Unit, Analytic, Ticket, TargetPrice, FeatureAnalyticTicket
from django.contrib import admin

class FeatureAnalyticTicketAdmin(admin.ModelAdmin):
	list_display = ('analytic', 'ticket', 'feature', 'value')

class TargetPriceAdmin(admin.ModelAdmin):
	list_display = ('analytic', 'date', 'price', 'ticket')

class TicketAdmin(admin.ModelAdmin):
	list_display = ('name', 'long_name')

class FeatureAdmin(admin.ModelAdmin):
	list_display = ('name', 'unit', 'display_in_frontpage')

admin.site.register(Unit)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Analytic)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TargetPrice, TargetPriceAdmin)
admin.site.register(FeatureAnalyticTicket, FeatureAnalyticTicketAdmin)

