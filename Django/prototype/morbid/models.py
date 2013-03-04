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
    """ The units of the feature """

    name = models.CharField(max_length=200)
    """Name of the unit of measure
    @type: C{str}"""
    value = models.CharField(max_length=200)
    """The value (sign) of the measure (days, percent)
    @type: C{str}"""

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
    """Name of the measure
    @type: C{str}"""
    unit = models.ForeignKey(Unit)
    """The units of the measure
    @type: L{Unit}"""
    display_in_frontpage = models.BooleanField()
    """Boolean to display in frontpage
    @type: C{boolean}"""
    description = models.TextField()
    """Description of the feature
    @type: C{text}"""
    slug = models.SlugField(max_length=200, unique=True)
    """Slug of the feature
    @type: C{str}"""

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
    """Name of analytic
    @type: C{str}"""
    number_of_companies = models.IntegerField()
    """Number of tp analytic released
    @type: C{integer}"""
    number_of_tp = models.IntegerField()
    """Number of target prices released by analytic
         @type: C{integer}"""
    volatility_positive = models.IntegerField()
    """Measure of uncertainty, total number of target prices
         @type: C{integer}"""
    volatility_negative = models.IntegerField()
    """Measure of uncertainty, total number of target prices, failed to keep the 250 days
         @type: C{integer}"""
    last_target_price = models.FloatField()
    """Last target price analytic released
         @type: C{float}"""

    slug = models.SlugField()
    """Slug to reach the page of analytic
        @type: C{str}"""

    def get_absolute_url(self):
        return "/analytic/%s/" % self.slug

    def natural_key(self):
        """
        Required for serialization
        @return: C{string}
        """
        return self.name

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
    """Name of the Ticker (AAPL, GOOG)
         @type: C{str}"""
    long_name = models.CharField(max_length=200)
    """Full name of the Ticker (Apple Inc, Google Inc)
         @type: C{str}"""
    last_stock_price = models.FloatField()
    """Last stock price of the Ticker (live update maybe)
         @type: C{float}"""
    number_of_analytics = models.IntegerField()
    """Number of analytics analyzing the Ticker
         @type: C{integer}"""
    number_of_tp = models.IntegerField()
    """How many target prices does the Ticker have
         @type: C{integer}"""
    consensus_min = models.FloatField()
    """Minimum value for the consensus measure
         @type: C{float}"""
    consensus_avg = models.FloatField()
    """Average value for the consensus measure
         @type: C{float}"""
    consensus_max = models.FloatField()
    """Maximum value for the consensus measure
         @type: C{float}"""

    slug = models.SlugField()
    """The slug to reach the page
        @type: C{str}"""

    def get_absolute_url(self):
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


class FeatureAnalyticTicker(models.Model):
    """
    The place where analytic, Ticker and feature meets
    """

    value = models.FloatField()
    """The value of the feature
         @type: C{float}"""
    feature = models.ForeignKey(Feature)
    """Defines the type of the feature (how near, fixation, ...)
         @type: L{Feature}"""
    analytic = models.ForeignKey(Analytic)
    """The analytic for which the feature was calculated
         @type: L{Analytic}"""
    ticker = models.ForeignKey(Ticker)
    """The Ticker on which the feature was calculated
         @type: L{Ticker}"""

    def hash(self):
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
    """The date of released target price
         @type: C{Date}"""
    price = models.FloatField()
    """The price of the target price
         @type: C{Float}"""
    change = models.FloatField()
    """The price change over the last price
         @type: C{Float}"""
    ticker = models.ForeignKey(Ticker)
    """The Ticker on which target price was released
         @type: L{Ticker}"""
    analytic = models.ForeignKey(Analytic)
    """The analytic, which published the target price
         @type: L{Analytic}"""

    objects = TargetPriceManager()

    def hash(self):
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
