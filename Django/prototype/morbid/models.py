from django.db import models
from django.core.urlresolvers import reverse


class Unit(models.Model):
	"""
	The units of the feature
	"""

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
	volatility = models.IntegerField()
	"""Measure of uncertainty
	   @type: C{integer}"""
	last_target_price = models.FloatField()
	"""Last target price analytic released
	   @type: C{float}"""

	slug = models.SlugField()
	"""Slug to reach the page of analytic
	  @type: C{str}"""

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

class Ticket(models.Model):
	"""
	The ticket (or more precise to call it a company) name
	"""

	name = models.CharField(max_length=200)
	"""Name of the ticket (AAPL, GOOG)
	   @type: C{str}"""
	long_name = models.CharField(max_length=200)
	"""Full name of the ticket (Apple Inc, Google Inc)
	   @type: C{str}"""
	last_stock_price = models.FloatField()
	"""Last stock price of the ticket (live update maybe)
	   @type: C{float}"""
	number_of_analytics = models.IntegerField()
	"""Number of analytics analyzing the ticket
	   @type: C{integer}"""
	number_of_tp = models.IntegerField()
	"""How many target prices does the ticket have
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

	def natural_key(self):
		"""
		The natural return key -- not index (pk), but the name (short name) 
		of the ticket

		@return: string
		"""
		return self.name

	def __unicode__(self):
		"""
		The object return name
		"""
		return self.long_name + " (" + self.name + ")"

class FeatureAnalyticTicket(models.Model):
	"""
	The place where analytic, ticket and feature meets
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
	ticket = models.ForeignKey(Ticket)
	"""The ticket on which the feature was calculated
	   @type: L{Ticket}"""

	def __unicode__(self):
		"""
		The object return name

		@return: string
		"""
		return str(self.value) + " " + str(self.feature) + " " + str(self.analytic)

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
	ticket = models.ForeignKey(Ticket)
	"""The ticket on which target price was released
	   @type: L{Ticket}"""
	analytic = models.ForeignKey(Analytic)
	"""The analytic, which published the target price
	   @type: L{Analytic}"""

	# def __unicode__(self):
		# return str(self.price) + " " + str(self.ticket)