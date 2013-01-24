# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.core import serializers
from morbid.models import TargetPrice, Analytic, FeatureAnalyticTicket, Feature, Ticket
# from django.utils import simplejson

def index(request):
	"""
	Index page

	The main page of the app

	@return: Http Response
	"""
	# @TODO: make a join query to database, not separate queries
	# @TODO: filter by date
	latest_target_prices = TargetPrice.objects.all()

	target_price_list = []

	for target_price in latest_target_prices:

		analytic_features = []

		feature_analytic_tickets = FeatureAnalyticTicket.objects.filter(
			analytic_id=target_price.analytic_id, 
			ticket_id=target_price.ticket_id,
			feature__display_in_frontpage=True
			)

		target_price.fap = feature_analytic_tickets
		target_price_list.append(target_price)


	t = loader.get_template('morbid/index.html')

	c = Context({
		'latest_target_prices' : target_price_list
	})

	return HttpResponse(t.render(c))

def ticket(request, slug):
	"""
	Ticket page

	@param slug: the request for the specific ticket
	@type: C{str}

	@return: Http Response. If the ticket was not found -- rises the 404 error
	"""

	try:
		ticket = Ticket.objects.get(slug=slug)
	except Ticket.DoesNotExist:
		raise Http404

	# Load target orice info
	latest_target_prices = TargetPrice.objects.filter(ticket_id=ticket.id).order_by('analytic', 'date').reverse().distinct('analytic')

	target_price_list = []

	for target_price in latest_target_prices:

		analytic_features = []

		feature_analytic_tickets = FeatureAnalyticTicket.objects.filter(
			analytic_id = target_price.analytic_id,
			ticket_id = target_price.analytic_id,
			feature__display_in_frontpage=True
			)

		target_price.fap = feature_analytic_tickets
		target_price_list.append(target_price)

	# Load feature info
	list_of_features = Feature.objects.all()

	t = loader.get_template('morbid/ticket.html')

	c = Context({
		'ticket' : ticket,
		'target_prices' : target_price_list,
		'features' : list_of_features
	})

	return HttpResponse(t.render(c))

def analytic(request, slug):
	"""
	Analytic page

	@param slug: the slug to reach the page

	@return: Http Response. If the analytic was not found by the slug -- 404 
	error rises
	"""

	# Load analytic info
	try:
		analytic = Analytic.objects.get(slug=slug)
	except Analytic.DoesNotExist:
		raise Http404

	# Load target price info
	latest_target_prices = TargetPrice.objects.filter(analytic_id=analytic.id).order_by('ticket', 'date').reverse().distinct('ticket')

	target_price_list = []

	for target_price in latest_target_prices:

		analytic_features = []

		feature_analytic_tickets = FeatureAnalyticTicket.objects.filter(
			analytic_id = target_price.analytic_id,
			ticket_id = target_price.ticket_id,
			feature__display_in_frontpage=True
			)

		target_price.fap = feature_analytic_tickets
		target_price_list.append(target_price)

	# Load feature info
	list_of_features = Feature.objects.all()

	t = loader.get_template('morbid/analytic.html')

	c = Context({
		'analytic' : analytic,
		'target_prices' : target_price_list,
		'features' : list_of_features
	})

	return HttpResponse(t.render(c))

def feature_by_ticket(self, slug, feature_id):
	"""
	The feature return management on the ticket page

	@param slug: the slug to reach the ticket
	@param feature_id: the feature id to return

	@return: Http Response. If the ticket was not found using the slug -- 404 
	error rises

	JSON only
	"""

	try:
		ticket = Ticket.objects.get(slug=slug)
	except ticket.DoesNotExist:
		return Http404

	feature_analytic_tickets = FeatureAnalyticTicket.objects.filter(
		ticket_id = ticket.id
		)

	return HttpResponse(serializers.serialize('json', 
		feature_analytic_tickets, 
		fields=('analytic', 'value'),
		relations={'analytic':{'fields':('name',)}}))

def feature_by_analytic(self, slug, feature_id):
	"""
	The feature return management on the analytic page

	@param slug: the slug to reach the
	@param feature_id: the feature id to return

	@return: Http Response JSON only. If the analytic was not found using the 
	slug -- 404 error rises

	
	"""
	try:
		analytic = Analytic.objects.get(slug=slug)
	except analytic.DoesNotExist:
		return Http404

	feature_analytic_tickets = FeatureAnalyticTicket.objects.filter(
		analytic_id = analytic.id
		)

	return HttpResponse(serializers.serialize('json', 
		feature_analytic_tickets, 
		fields=('ticket', 'value'),
		relations={'ticket':{'fields':('name','long_name')}}))

def search(self, search_me):
	"""
	The search of the page

	@param search_me: The string to query search the database

	@return: Http Response in JSON.
	"""
	pass