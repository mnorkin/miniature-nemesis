from django import forms
from django.forms.widgets import HiddenInput


class FeatureAnalyticTickerCheckForm(forms.Form):
    """
    The feature analytic ticker check form
    """
    value = forms.CharField()
    feature_analytic_ticker = forms.IntegerField(
        widget=HiddenInput
    )
