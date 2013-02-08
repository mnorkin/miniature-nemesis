from morbid.models import Feature, Unit, Analytic, Ticker, TargetPrice, FeatureAnalyticTicker
from django.contrib import admin

class FeatureAnalyticTickerAdmin(admin.ModelAdmin):
	list_display = ('analytic', 'ticker', 'feature', 'value')

class TargetPriceAdmin(admin.ModelAdmin):
	list_display = ('analytic', 'date', 'price', 'ticker')

class TickerAdmin(admin.ModelAdmin):
	list_display = ('name', 'long_name')

class FeatureAdmin(admin.ModelAdmin):
	list_display = ('name', 'unit', 'display_in_frontpage')

admin.site.register(Unit)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Analytic)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(TargetPrice, TargetPriceAdmin)
admin.site.register(FeatureAnalyticTicker, FeatureAnalyticTickerAdmin)