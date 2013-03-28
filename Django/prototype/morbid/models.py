from django.db import models    # Model description
from django.conf import settings    # Settings
from django.contrib.auth import models as auth_models    # Authentication
from django.contrib.auth.models import User    # User manager
from django.contrib.auth.management import create_superuser    # Superuser manager
from django.db.models import signals    # Signal handling
import string    # String lib for alphabet

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)


class Unit(models.Model):
    """
    The units of the feature
    """
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __unicode__(self):
        """
        The object return name
        """
        return self.name


class Feature(models.Model):
    """
    The feature of the measure
    """
    name = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit)
    display_in_frontpage = models.BooleanField()
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        """
        The object return name
        """
        return self.name


class Analytic(models.Model):
    """
    Analysing analytic
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def get_absolute_url(self):
        """
        Generating absolute url to reach analytic
        """
        return "/analytic/%s/" % self.slug

    def natural_key(self):
        """
        Required for serialization
        @return: C{string}
        """
        return self.name

    def last_target_price(self, _ticker=None):
        """
        Returning last target price
        """
        if _ticker:
            target_price = TargetPrice
            try:
                target_price = TargetPrice.objects.filter(
                    ticker=_ticker,
                    analytic=self).order_by('-date')[0]
                return target_price
            except target_price.DoesNotExist:
                return None
        else:
            return None

    def __unicode__(self):
        """
        The object return name
        """
        return self.name


class Ticker(models.Model):
    """
    The Ticker (or more precise to call it a company) name
    """
    name = models.CharField(max_length=200)
    long_name = models.CharField(max_length=200)
    last_stock_price = models.FloatField()
    consensus_min = models.FloatField()
    consensus_avg = models.FloatField()
    consensus_max = models.FloatField()
    slug = models.SlugField()

    def get_absolute_url(self):
        """
        Generating absolute url
        """
        return "/ticker/%s/" % self.slug

    def natural_key(self):
        """
        The natural return key -- not index (pk), but the name (short name)
        of the Ticker

        @return: string
        """
        return self.name

    def __unicode__(self):
        """
        The object return name
        """
        return self.long_name + " (" + self.name + ")"


class TargetPriceNumberAnalyticTicker(models.Model):
    """
    Number of target prices to the ticker, given by the specific analytic
    """
    analytic = models.ForeignKey(Analytic)
    ticker = models.ForeignKey(Ticker)
    number = models.IntegerField()

    def __unicode__(self):
        """
        Unicode return
        """
        return str(self.number)


class Volatility(models.Model):
    """
    Volatility measure
    """
    analytic = models.ForeignKey(Analytic)
    ticker = models.ForeignKey(Ticker)
    number = models.IntegerField()
    total = models.IntegerField()

    def __unicode__(self):
        """
        Unicode return
        """
        return str(self.number) + '/' + str(self.total)


class FeatureAnalyticTicker(models.Model):
    """
    The place where analytic, Ticker and feature meets
    """
    value = models.FloatField()
    feature = models.ForeignKey(Feature)
    analytic = models.ForeignKey(Analytic)
    ticker = models.ForeignKey(Ticker)

    def hash(self):
        """
        Unique identification of feature for Analytic-Ticker relation
        """
        all_letters = string.lowercase
        id_hash = "".join([all_letters[int(letter)] for letter in str(self.id)])
        return self.feature.slug + self.analytic.slug + self.ticker.slug + id_hash

    def __unicode__(self):
        """
        The object return name

        @return: string
        """
        return str(self.value) + " " + str(self.feature) + " " + str(self.analytic)


class TargetPriceManager(models.Manager):
    """
    Custom Target Price Manager
    """
    def with_count(self):
        """
        Return the target prices with more than repeatable number defined
        """
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT ticker_id FROM morbid_targetprice GROUP BY ticker_id HAVING COUNT(ticker_id) > 1")
        results_list = []
        for row in cursor.fetchall():
            results_list.append(row[0])

        return self.filter(ticker_id__in=results_list)


class TargetPrice(models.Model):
    """
    The list of all the target prices to show to people
    """
    date = models.DateField()
    price = models.FloatField()
    change = models.FloatField()
    ticker = models.ForeignKey(Ticker)
    analytic = models.ForeignKey(Analytic)

    objects = TargetPriceManager()

    def hash(self):
        """
        Unique identification of particular targe price
        """
        all_letters = string.lowercase
        id_hash = "".join([all_letters[int(letter)] for letter in str(self.date).replace("-", "")])
        price_hash = "".join([all_letters[int(letter)] for letter in str(self.price).replace(".", "")])
        return price_hash + self.analytic.slug + self.ticker.slug + id_hash

    def __unicode__(self):
        """
        Returns unicode object name
        """
        return str(self.price) + " " + str(self.ticker)


class ApiKey(models.Model):
    """
    ApiKey things
    """
    user = models.ForeignKey(User, related_name='keys', unique=True)
    key = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.key = User.objects.make_random_password(length=255)

        while ApiKey.objects.filter(key__exact=self.key).count():
            self.key = User.objects.make_random_password(length=255)

        super(ApiKey, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key


def create_testuser(app, created_models, verbosity, **kwargs):
    """
    Create fast user automatically
    """
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
