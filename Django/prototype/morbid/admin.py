from morbid.models import Feature, Unit, Analytic, Ticker, TargetPrice, FeatureAnalyticTicker
from django.contrib import admin


class AnalyticAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_companies', 'last_target_price')


class FeatureAnalyticTickerAdmin(admin.ModelAdmin):
    list_display = ('analytic', 'ticker', 'feature', 'value')


class TargetPriceAdmin(admin.ModelAdmin):
    list_display = ('analytic', 'date', 'price', 'ticker')


class TickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'long_name', 'slug')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'display_in_frontpage')

admin.site.register(Unit)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Analytic, AnalyticAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(TargetPrice, TargetPriceAdmin)
admin.site.register(FeatureAnalyticTicker, FeatureAnalyticTickerAdmin)
