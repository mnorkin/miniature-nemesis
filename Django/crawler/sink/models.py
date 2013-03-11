from django.db import models


class Ticker(models.Model):
    """
    Ticker model
    """
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=200)


class TargetPrice(models.Model):
    """
    Target Price model
    """
    analytic = models.CharField(max_length=200)
    market = models.CharField(max_length=200)
    ticker = models.ForeignKey(Ticker)
    date = models.DateField()


class TickerChange(models.Model):
    """
    Ticker change model
    """
    pass
