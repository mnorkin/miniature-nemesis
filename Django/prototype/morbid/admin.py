from morbid.models import Feature
from morbid.models import Unit
from morbid.models import Analytic
from morbid.models import Ticker
from morbid.models import TargetPrice
from morbid.models import FeatureAnalyticTicker
from morbid.models import FeatureAnalyticTickerCheck
from morbid.models import Volatility
from morbid.models import TargetPriceAnalyticTicker
from django.contrib import admin


class VolatilityAdmin(admin.ModelAdmin):
    list_display = ('analytic', 'ticker', 'total', 'number')


class AnalyticAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_target_price')

class FeatureAnalyticTickerCheckAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'analytic', 'feature_name', 'value', 'feature_value')

    def feature_value(self, obj):
        return "%s" % ( obj.feature_analytic_ticker.value )

    def feature_name(self, obj):
        return "%s" % ( obj.feature_analytic_ticker.feature.name )

    def ticker(self, obj):
        return "%s" % ( obj.feature_analytic_ticker.ticker.name )

    def analytic(self, obj):
        return "%s" % ( obj.feature_analytic_ticker.analytic.name )

class FeatureAnalyticTickerAdmin(admin.ModelAdmin):
    list_display = ('analytic', 'ticker', 'feature', 'value')


class TargetPriceAdmin(admin.ModelAdmin):
    list_display = ('analytic', 'date', 'price', 'ticker')
    search_fields = ['ticker__name']


class TickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'long_name', 'slug')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'display_in_frontpage', 'position')
    ordering = ['position']


class TargetPriceAnalyticTickerAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'analytic', 'date')
    ordering = ['date']

admin.site.register(Unit)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Volatility, VolatilityAdmin)
admin.site.register(Analytic, AnalyticAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(TargetPrice, TargetPriceAdmin)
admin.site.register(FeatureAnalyticTicker, FeatureAnalyticTickerAdmin)
admin.site.register(FeatureAnalyticTickerCheck, FeatureAnalyticTickerCheckAdmin)
admin.site.register(TargetPriceAnalyticTicker, TargetPriceAnalyticTickerAdmin)
