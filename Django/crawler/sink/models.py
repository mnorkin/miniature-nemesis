from django.db import models
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)


class Ticker(models.Model):
    """
    Ticker model
    """
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=200)
    market = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Market(models.Model):
    """
    Market
    """
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Analytic(models.Model):
    """
    Analytic
    """
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class TargetPrice(models.Model):
    """
    Target Price model
    """
    action = models.CharField(max_length=200)
    analytic = models.ForeignKey(Analytic)
    rating = models.CharField(max_length=200)
    price0 = models.FloatField()
    price1 = models.FloatField()
    ticker = models.ForeignKey(Ticker)
    date = models.DateField()

    def __unicode__(self):
        return self.ticker.name


class Stock(models.Model):
    """
    The stock guy
    """
    ticker = models.ForeignKey(Ticker)
    date = models.DateField()
    price_open = models.FloatField()
    price_high = models.FloatField()
    price_low = models.FloatField()
    price_close = models.FloatField()


class TickerChange(models.Model):
    """
    Ticker change model
    """
    pass


def create_testuser(app, created_models, verbosity, **kwargs):
    """Create fast user automatically"""
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username='test')
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating test user -- login: test, password: test'
        print '*' * 80
        assert auth_models.User.objects.create_superuser('test', 'x@x.com', 'test')
    else:
        print 'Test user already exists'

signals.post_syncdb.connect(
    create_testuser,
    sender=auth_models,
    dispatch_uid='common.models.create_testuser'
)
