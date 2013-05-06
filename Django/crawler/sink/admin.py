from sink.models import Analytic
from sink.models import Market, TargetPrice, Ticker
from django.contrib import admin


class TickersAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker')
    search_fields = ['name']

admin.site.register(Analytic)
admin.site.register(Market)
admin.site.register(TargetPrice)
admin.site.register(Ticker, TickersAdmin)
