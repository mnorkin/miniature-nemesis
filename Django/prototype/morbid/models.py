from django.db import models    # Model description
from django.contrib.auth import models as auth_models    # Authentication
from django.contrib.auth.models import User    # User manager
from django.contrib.auth.management import create_superuser    # Superuser manager
from django.db.models import signals    # Signal handling
import string    # String lib for alphabet
from datetime import date
from datetime import timedelta
from morbid.queries import front_page_query
from morbid.queries import target_prices_for_ticker_query
from morbid.queries import target_prices_for_analytic_query
from morbid.queries import sort_by_features_query
from morbid.queries import sort_by_change
from morbid.queries import sort_by_features_ticker_query
from morbid.queries import sort_by_change_ticker_query
from morbid.queries import sort_by_features_analytic_query
from morbid.queries import sort_by_change_analytic_query
from morbid.queries import target_prices_query
from morbid.queries import features_query

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
    display = models.BooleanField()
    description = models.TextField()
    position = models.IntegerField()
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
    name = models.CharField(
        db_index=True,
        max_length=200
    )
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

    def number_of_companies(self):
        """
        Returning the number of companies, analytic does analysis on
        """
        return TargetPrice.objects.filter(
            analytic=self
        ).distinct('ticker').count()

    def number_of_target_prices(self):
        """
        Returning the active number of target prices, which belongs to analytic
        """
        return TargetPrice.objects.valid().filter(
            analytic=self
        ).count()

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


class TickerManager(models.Manager):
    """
    Ticker Manager
    """

    def with_display(self):
        """
        Returning all the tickers, which has positive display field
        """
        return Ticker.objects.filter(display=1)


class Ticker(models.Model):
    """
    The Ticker (or more precise to call it a company) name
    """
    name = models.CharField(
        db_index=True,
        max_length=200
    )
    long_name = models.CharField(
        db_index=True,
        max_length=200
    )
    # Last stock group gives information on
    # stock market price change
    last_stock_price = models.FloatField()
    last_stock_change = models.FloatField()
    consensus_min = models.FloatField()
    consensus_avg = models.FloatField()
    consensus_max = models.FloatField()
    slug = models.SlugField()
    display = models.BooleanField()

    objects = TickerManager()

    def last_stock_change_percent(self):
        """
        Returning the stock change from percent to real value
        """
        try:
            return (self.last_stock_price-self.last_stock_change)/self.last_stock_price
        except ZeroDivisionError:
            return 0

    def get_absolute_url(self, slug=None):
        """
        Generating absolute url
        """
        if slug is None:
            return "/ticker/%s/" % self.slug
        else:
            return "/ticker/%s/" % slug

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

    def number_of_analytics(self):
        """
        Returning the number of analytics of the ticker
        """
        return TargetPrice.objects.filter(
            ticker__name=self.name
        ).distinct('analytic').count()

    def number_of_target_prices(self):
        """
        Returning number of active target prices of ticker
        """
        return TargetPrice.objects.valid().filter(
            ticker__name=self.name
        ).count()


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


class TargetPriceAnalyticTicker(models.Model):
    """
    This is the calculator storage, to validate the calculated
    features and skip
    calculations if the data is already available
    """
    analytic = models.ForeignKey(Analytic)
    ticker = models.ForeignKey(Ticker)
    date = models.DateField()


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


class FeatureAnalyticTickerCheck(models.Model):
    """
    Testing platform to check the calculations
    """
    value = models.FloatField()
    feature_analytic_ticker = models.ForeignKey(FeatureAnalyticTicker)

    def __unicode__(self):
        return str(self.value)


class TargetPriceManager(models.Manager):
    """
    Custom Target Price Manager
    """
    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def with_count(self):
        """
        Return the target prices with more than repeatable number defined
        """
        from django.db import connection
        cursor = connection.cursor()
        query = " \
            SELECT ticker_id \
            FROM morbid_targetprice  \
            GROUP BY ticker_id  \
            HAVING COUNT(ticker_id) > 1 \
        "
        cursor.execute(query)
        results_list = []
        for row in cursor.fetchall():
            results_list.append(row[0])
        return self.filter(ticker_id__in=results_list)

    def construct_hash(self, row):
        """
        Construction of hash
        """
        all_letters = string.lowercase
        id_hash = "".join(
            [all_letters[int(letter)] for letter in str(row['date']).replace("-", "")]
        )
        price_hash = "".join(
            [all_letters[int(letter)] for letter in str(row['price']).replace(".", "")]
        )
        return price_hash + row['analytic_slug'] + row['ticker_slug'] + id_hash

    def construct_change(self, row):
        """
        Construction of change
        """
        value = 0
        direction = 'up'
        # try:
        #     # value = round(float(row['price'] - row['last_stock_price'])/row['price']*100*10)/10
        # except ZeroDivisionError:
        #     pass

        value = row['change']

        if value < 0:
            direction = 'down'

        return {
            'abs_value': abs(value),
            'value': value,
            'direction': direction
        }

    def construct_features(self, row):
        """
        Construction of features
        """
        from django.db import connection
        features_cursor = connection.cursor()
        features_cursor.execute(features_query % { 
            'ticker_id': row['ticker_id'], 
            'analytic_id': row['analytic_id']
        })
        features = []
        for feature in self.dictfetchall(features_cursor):
            features.append({
                'name': feature['name'],
                'value': feature['value'],
                'slug': feature['slug']
            })
        return features

    def construct_targets(self, cursor):
        """
        Constructing target prices
        """
        results_list = []
        for row in self.dictfetchall(cursor):
            """
            Append the results
            """
            results_list.append({
                'date': row['date'],
                'ticker_name': row['ticker_name'],
                'ticker_long_name': row['ticker_long_name'],
                'analytic': row['analytic_name'],
                'analytic_slug': row['analytic_slug'],
                'price': round(row['price']*10)/10,
                'hash': self.construct_hash(row),
                'features': self.construct_features(row),
                'change': self.construct_change(row),
                'url': '/ticker/' + row['ticker_slug'] + '/',
            })
        return results_list

    def recent_target_prices(self, page=0, entries_per_page=20):
        """
        Return recent target prices

        This took a lot of my blood, but it looks like it is working
        """
        from django.db import connection

        """
        Define offset
        """
        offset = 0
        if int(page) != 0:
            offset = (int(page)*entries_per_page)+1

        """
        Connection cursors
        """
        cursor = connection.cursor()
        """
        Describe queries
        """
        cursor.execute(front_page_query % {
            'limit': entries_per_page,
            'offset': offset
        })
        return self.construct_targets(cursor)

    def analytic_target_prices(self, analytic_slug=None, page=0, entries_per_page=20):
        """
        Target prices, which belongs to particular analytic
        """
        from django.db import connection

        """
        Define offset
        """
        offset = 0
        if int(page) != 0:
            offset = (int(page)*entries_per_page)+1

        """
        Connection cursors
        """
        cursor = connection.cursor()
        cursor.execute(target_prices_for_analytic_query % {
            'analytic_slug': analytic_slug, 
            'limit': entries_per_page, 
            'offset': offset
        })
        return self.construct_targets(cursor)

    def ticker_target_prices(self, ticker_slug=None, page=0, entries_per_page=20):
        """
        Target prices, which belongs to particular ticker
        """
        from django.db import connection

        """
        Define offset
        """
        offset = 0
        if int(page) != 0:
            offset = (int(page)*entries_per_page)+1

        """
        Connection cursors
        """
        cursor = connection.cursor()
        cursor.execute(target_prices_for_ticker_query % {
            'ticker_slug': ticker_slug,
            'limit': entries_per_page, 
            'offset': offset
        })
        return self.construct_targets(cursor)

    def sorted_ticker_target_prices(self, ticker_slug, sort_by, sort_direction, page=0, limit=20):
        from django.db import connection
        results_list = []

        offset = 0
        if int(page) != 0:
            offset = (int(page)*limit) + 1

        if sort_direction == 'up':
            sort_direction = 'DESC'
        else:
            sort_direction = 'ASC'

        sort_cursor = connection.cursor()
        if sort_by == 'change':
            sort_cursor.execute(
                sort_by_change_ticker_query % {
                    'ticker_slug': ticker_slug,
                    'sort_direction': sort_direction,
                    'limit': limit,
                    'offset': offset
                }
            )
        else:
            sort_cursor.execute(
                sort_by_features_ticker_query % {
                    'ticker_slug': ticker_slug,
                    'sort_by': sort_by,
                    'sort_direction': sort_direction,
                    'limit': limit,
                    'offset': offset
                }
            )
        cursor = connection.cursor()

        for sort_row in self.dictfetchall(sort_cursor):
            cursor.execute(
                target_prices_query % {
                    'target_id': sort_row['target_id']
                }
            )
            row = self.dictfetchall(cursor)[0]

            results_list.append({
                'date': str(row['date']),
                'ticker_name': row['ticker_name'],
                'ticker_long_name': row['ticker_long_name'],
                'analytic': row['analytic_name'],
                'analytic_slug': row['analytic_slug'],
                'price': row['price'],
                'hash': self.construct_hash(row),
                'features': self.construct_features(row),
                'change': self.construct_change(row),
                'url': '/ticker/' + row['ticker_slug'] + '/',
            })

        return results_list

    def sorted_analytic_target_prices(self, analytic_slug, sort_by, sort_direction, page=0, limit=20):
        from django.db import connection
        results_list = []

        offset = 0
        if int(page) != 0:
            offset = (int(page)*limit)+1

        if sort_direction == 'up':
            sort_direction = 'DESC'
        else:
            sort_direction = 'ASC'

        sort_cursor = connection.cursor()

        if sort_by == 'change':
            sort_cursor.execute(
                sort_by_change_analytic_query % {
                    'analytic_slug': analytic_slug,
                    'sort_direction': sort_direction,
                    'limit': limit,
                    'offset': offset
                }
            )
        else:
            sort_cursor.execute(
                sort_by_features_analytic_query % {
                    'analytic_slug': analytic_slug,
                    'sort_by': sort_by,
                    'sort_direction': sort_direction,
                    'limit': limit,
                    'offset': offset
                }
            )
        cursor = connection.cursor()

        for sort_row in self.dictfetchall(sort_cursor):
            cursor.execute(
                target_prices_query % {
                    'target_id': sort_row['target_id']
                }
            )
            row = self.dictfetchall(cursor)[0]

            results_list.append({
                'date': str(row['date']),
                'ticker_name': row['ticker_name'],
                'ticker_long_name': row['ticker_long_name'],
                'analytic': row['analytic_name'],
                'analytic_slug': row['analytic_slug'],
                'analytic_name': row['analytic_name'],
                'price': row['price'],
                'hash': self.construct_hash(row),
                'features': self.construct_features(row),
                'change': self.construct_change(row),
                'url': '/ticker/' + row['ticker_slug'] + '/',
            })

        return results_list

    def sorted(self, sort_by='accuracy', sort_direction='down', page=0, entries_per_page=20):
        """
        Sorted target prices
        """
        from django.db import connection
        """
        Define offset
        """
        offset = 0
        if int(page) != 0:
            offset = (int(page)*entries_per_page)+1

        """
        Pre-define lists
        """
        results_list = []

        if sort_direction == 'up':
            sort_direction = 'DESC'
        else:
            sort_direction = 'ASC'

        sort_cursor = connection.cursor()
        if (sort_by == 'change'):
            sort_cursor.execute(
                sort_by_change % {
                    'sort_direction': sort_direction,
                    'limit': entries_per_page,
                    'offset': offset
                }
            )
        else:
            sort_cursor.execute(
                sort_by_features_query % {
                    'sort_by': sort_by,
                    'sort_direction': sort_direction,
                    'limit': entries_per_page,
                    'offset': offset
                }
            )
        cursor = connection.cursor()

        for sort_row in self.dictfetchall(sort_cursor):
            """
            Appending results
            """
            cursor.execute(target_prices_query % {
                'target_id': sort_row['target_id']
            })
            row = self.dictfetchall(cursor)[0]

            results_list.append({
                'date': str(row['date']),
                'ticker_name': row['ticker_name'],
                'ticker_long_name': row['ticker_long_name'],
                'analytic': row['analytic_name'],
                'analytic_slug': row['analytic_slug'],
                'price': row['price'],
                'hash': self.construct_hash(row),
                'features': self.construct_features(row),
                'change': self.construct_change(row),
                'url': '/ticker/' + row['ticker_slug'] + '/',
            })

        return results_list

    def valid(self):
        """
        Returning all the target prices, which are valid
        """
        year_ago = date.today() - timedelta(days=356)
        return TargetPrice.objects.filter(date__gt=year_ago)


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
        Unique identification of particular target price
        """
        all_letters = string.lowercase
        id_hash = "".join([all_letters[int(letter)] for letter in str(self.date).replace("-", "")])
        price_hash = "".join([all_letters[int(letter)] for letter in str(self.price).replace(".", "")])
        return price_hash + self.analytic.slug + self.ticker.slug + id_hash

    def get_change(self):
        last_stock_price = Ticker.objects.get(id=self.ticker_id).last_stock_price
        try:
            return float(last_stock_price - self.price)/last_stock_price*100
        except ZeroDivisionError:
            return 0

    def target_price_number_analytic_ticker(self):
        return TargetPriceNumberAnalyticTicker.objects.get(
            ticker=self.ticker,
            analytic=self.analytic
        )

    def volatility(self):
        return Volatility.objects.get(
            ticker=self.ticker,
            analytic=self.analytic
        )

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
    try:
        auth_models.User.objects.get(username='test')
    except auth_models.User.DoesNotExist:
        print 'Creating test user -- login: test, password: test'
        assert auth_models.User.objects.create_superuser('test', 'x@x.com', 'test')
    else:
        print 'Test user already exists'

signals.post_syncdb.connect(
    create_testuser,
    sender=auth_models,
    dispatch_uid='common.models.create_testuser'
)
