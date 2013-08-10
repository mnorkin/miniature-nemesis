# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unit'
        db.create_table('morbid_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('morbid', ['Unit'])

        # Adding model 'Feature'
        db.create_table('morbid_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Unit'])),
            ('display_in_frontpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('morbid', ['Feature'])

        # Adding model 'Analytic'
        db.create_table('morbid_analytic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('morbid', ['Analytic'])

        # Adding model 'Ticker'
        db.create_table('morbid_ticker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_stock_price', self.gf('django.db.models.fields.FloatField')()),
            ('last_stock_change', self.gf('django.db.models.fields.FloatField')()),
            ('consensus_min', self.gf('django.db.models.fields.FloatField')()),
            ('consensus_avg', self.gf('django.db.models.fields.FloatField')()),
            ('consensus_max', self.gf('django.db.models.fields.FloatField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('morbid', ['Ticker'])

        # Adding model 'TargetPriceNumberAnalyticTicker'
        db.create_table('morbid_targetpricenumberanalyticticker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('analytic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Analytic'])),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Ticker'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('morbid', ['TargetPriceNumberAnalyticTicker'])

        # Adding model 'TargetPriceAnalyticTicker'
        db.create_table('morbid_targetpriceanalyticticker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('analytic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Analytic'])),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Ticker'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('morbid', ['TargetPriceAnalyticTicker'])

        # Adding model 'Volatility'
        db.create_table('morbid_volatility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('analytic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Analytic'])),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Ticker'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('morbid', ['Volatility'])

        # Adding model 'FeatureAnalyticTicker'
        db.create_table('morbid_featureanalyticticker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Feature'])),
            ('analytic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Analytic'])),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Ticker'])),
        ))
        db.send_create_signal('morbid', ['FeatureAnalyticTicker'])

        # Adding model 'TargetPrice'
        db.create_table('morbid_targetprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('change', self.gf('django.db.models.fields.FloatField')()),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Ticker'])),
            ('analytic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['morbid.Analytic'])),
        ))
        db.send_create_signal('morbid', ['TargetPrice'])

        # Adding model 'ApiKey'
        db.create_table('morbid_apikey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keys', unique=True, to=orm['auth.User'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('morbid', ['ApiKey'])


    def backwards(self, orm):
        # Deleting model 'Unit'
        db.delete_table('morbid_unit')

        # Deleting model 'Feature'
        db.delete_table('morbid_feature')

        # Deleting model 'Analytic'
        db.delete_table('morbid_analytic')

        # Deleting model 'Ticker'
        db.delete_table('morbid_ticker')

        # Deleting model 'TargetPriceNumberAnalyticTicker'
        db.delete_table('morbid_targetpricenumberanalyticticker')

        # Deleting model 'TargetPriceAnalyticTicker'
        db.delete_table('morbid_targetpriceanalyticticker')

        # Deleting model 'Volatility'
        db.delete_table('morbid_volatility')

        # Deleting model 'FeatureAnalyticTicker'
        db.delete_table('morbid_featureanalyticticker')

        # Deleting model 'TargetPrice'
        db.delete_table('morbid_targetprice')

        # Deleting model 'ApiKey'
        db.delete_table('morbid_apikey')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'morbid.analytic': {
            'Meta': {'object_name': 'Analytic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'morbid.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keys'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'morbid.feature': {
            'Meta': {'object_name': 'Feature'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_in_frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Unit']"})
        },
        'morbid.featureanalyticticker': {
            'Meta': {'object_name': 'FeatureAnalyticTicker'},
            'analytic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Analytic']"}),
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Feature']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Ticker']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'morbid.targetprice': {
            'Meta': {'object_name': 'TargetPrice'},
            'analytic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Analytic']"}),
            'change': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Ticker']"})
        },
        'morbid.targetpriceanalyticticker': {
            'Meta': {'object_name': 'TargetPriceAnalyticTicker'},
            'analytic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Analytic']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Ticker']"})
        },
        'morbid.targetpricenumberanalyticticker': {
            'Meta': {'object_name': 'TargetPriceNumberAnalyticTicker'},
            'analytic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Analytic']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Ticker']"})
        },
        'morbid.ticker': {
            'Meta': {'object_name': 'Ticker'},
            'consensus_avg': ('django.db.models.fields.FloatField', [], {}),
            'consensus_max': ('django.db.models.fields.FloatField', [], {}),
            'consensus_min': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_stock_change': ('django.db.models.fields.FloatField', [], {}),
            'last_stock_price': ('django.db.models.fields.FloatField', [], {}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'morbid.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'morbid.volatility': {
            'Meta': {'object_name': 'Volatility'},
            'analytic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Analytic']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['morbid.Ticker']"}),
            'total': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['morbid']