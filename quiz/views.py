from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from .models import Card, Set, Language
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, HttpResponseRedirect
import logging
import json
from django.db import IntegrityError
import datetime

logger = logging.getLogger(__name__)

def index(request):
	template = loader.get_template('quiz/index.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def login_user(request):
	context = {}
	context.update(csrf(request))
	username = password = state = ''
	# This is when submit is already clicked once
	if request.POST:
		username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # Actual authenticated user
        if user is not None:
			# Successful login scenario
			login(request, user)
			state = "You're successfully logged in!"
			user_name = username
			user_id = User.objects.filter(username=username)
			sets = Set.objects.filter(user=user_id)
			response = HttpResponse()
			response = render(request, 'quiz/dashboard.html' ,{'state':state, 'msg':'You have not created any sets yet', 'username': username, 'password': password, 'sets': sets, 'number_of_sets': len(sets)})
			# response.set_cookie('user', username)
			return response
	state = "Invalid login credentials"
	return render(request, 'quiz/index.html', {'state': state})

def debug_view(request):
	template = loader.get_template('quiz/cardsInEditForm.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def signup_user(request):
	context = {}
	context.update(csrf(request))
	username = password = ''

	try:
		if request.POST:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = User.objects.create_user(username, username, password)
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			user.save()
	        authenticate(username=username, password=password)
	        login(request, user)
	        state = "New user successfully created"
	        response = HttpResponse()
	        response = render(request, 'quiz/dashboard.html' ,{'state':state, 'username': username, 'password': password})
	        # response.set_cookie('user', username)
	        return response
		return render(request, 'quiz/dashboard.html' ,{'state': 'Error occured', 'username': username, 'password': password})
	except IntegrityError as e:
		state = "User already exists"
		return render(request, 'quiz/index.html', {'state': state})

def create_set_form(request):
	return render(request, 'quiz/createSet.html', { 'languages': Language.objects.order_by('name') })

def userPage(request):
	template = loader.get_template('quiz/userPage.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def return_to_dashboard(request):
	state = "New set successfully created"
	retrieved_user = User.objects.get(username=request.user)
	sets = Set.objects.filter(user=retrieved_user)
	return render(request, 'quiz/dashboard.html' ,{'state':'Back home bitches', 'sets': sets, 'number_of_sets': len(sets)})


def search(request):
	context = {}
	context.update(csrf(request))
	print(request.user)
	if request.POST:
		decode_json = request.POST.get('srch-term')
		sets = Set.objects.filter(
			Q(title__contains=decode_json)|
			Q(description__contains=decode_json)|
			Q(language_from__name__contains=decode_json)|
			Q(language_to__name__contains=decode_json)
			).filter(user__username=request.user)
		print(sets)
		other_sets = Set.objects.filter(
			Q(title__contains=decode_json)|
			Q(description__contains=decode_json)|
			Q(language_from__name__contains=decode_json)|
			Q(language_to__name__contains=decode_json)
			).filter(~Q(user__username=request.user))
		print(other_sets)
		arguments = {'sets': sets,'msg': 'No search results found', 'number_of_sets': len(sets), 'OtherSets':other_sets, 'number_of_others': len(other_sets), 'username': request.user}
		return render(request, 'quiz/dashboard.html', arguments)
	
def deleteSet(request,set_id):

	context = {}
	context.update(csrf(request))
	
	Card.objects.filter(id = set_id).delete()
	Set.objects.filter(id = set_id).delete()

	
	sets = Set.objects.filter(user=request.user)
	print(sets)
	return render(request, 'quiz/dashboard.html' ,{'username': request.user, 'sets': sets, 'number_of_sets': len(sets)})
	
	
	#return HttpResponse(template.render(context))

def addSet(request, set_id):
	context = {}
	context.update(csrf(request))
	try:
		s = Set.objects.get(id=set_id)
		b = Set(title = s.title, description = s.description, language_to = s.language_to, language_from = s.language_from, user = request.user )
		# b = Domain(name = decode_json['0'],
			# full_name = decode_json['1'], status = decode_json['2'], account = accountObj, ips=decode_json['4'],
			# cname= decode_json['5'], billing_date_counter = decode_json['6'], created_at = decode_json['7'], is_active = decode_json['8'],)
		b.save()
		sets = Set.objects.filter(user=request.user)

		print(sets)
		return render(request, 'quiz/dashboard.html' ,{'username': request.user, 'sets': sets, 'number_of_sets': len(sets)})
	except IntegrityError as e:
		response = render(request, 'quiz/dashboard.html' ,{'msg':'Set already exists'})
		return response

def set_create(request):
	context = {}
	context.update(csrf(request))
	retrieved_user = User.objects.get(username=request.user)
	sets = Set.objects.filter(user=retrieved_user)
	try:
		if request.POST:
			request_title = request.POST.get('title')
			request_description = request.POST.get('description')
			request_language_to = request.POST.get('languageTo')
			request_language_from = request.POST.get('languageFrom')
			retrieve_language = lambda x: Language.objects.get(pk=x)
			created_set = Set(user = retrieved_user, 
				title = request_title, 
				description = request_description, 
				language_to = retrieve_language(request_language_to),
				language_from = retrieve_language(request_language_from))
			created_set.save()
			state = "New set successfully created"
			return render(request, 'quiz/dashboard.html' ,{'state':'successfully created set', 'sets': sets, 'number_of_sets': len(sets)})
		else:
			return render(request, 'quiz/dashboard.html' ,{'state':'Could not create set', 'sets': sets, 'number_of_sets': len(sets)})
	except IntegrityError as e:
		response = render(request, 'quiz/dashboard.html' ,{'msg':'Set already exists'})
		return response

def get_set(request, set_id):
	return render(request, 'quiz/viewCards.html', { 'SetCards': Card.objects.filter(set = set_id) })

# Get request to display form
def edit_set_form(request, set_id):
	required_set = Set.objects.get(pk=set_id)
	cards = Card.objects.filter(set = required_set)
	return render(request, 'quiz/editSet.html' ,{ 'languages': Language.objects.order_by('name'), 'set': Set.objects.get(pk=set_id), 'cards': cards })

def set_card_form(request, set_id):
	return render(request, 'quiz/setCards.html', { 'set_id': set_id })

# Triggered when OK is clicked. Needs set_id as part of get req body
def edit_set(request):
	retrieved_user = User.objects.get(username=request.user)
	sets = Set.objects.filter(user=retrieved_user)
	try:
		if request.POST:
			set_id = request.POST.get('setId')
			set_to_edit = Set.objects.get(pk=set_id)
			request_title = request.POST.get('title')
			request_description = request.POST.get('description')
			request_language_to = request.POST.get('languageTo')
			request_language_from = request.POST.get('languageFrom')
			retrieve_language = lambda x: Language.objects.get(pk=x)
			set_to_edit.title = request_title
			set_to_edit.description = request_description
			set_to_edit.language_to = retrieve_language(request_language_to)
			set_to_edit.language_from = retrieve_language(request_language_from)
			set_to_edit.save()
			return render(request, 'quiz/dashboard.html' ,{'state':'successfully edited set', 'sets': sets, 'number_of_sets': len(sets)})
		else:
			return render(request, 'quiz/dashboard.html' ,{'state':'Could not edit set', 'sets': sets, 'number_of_sets': len(sets)})
	except IntegrityError as e:
		response = render(request, 'quiz/dashboard.html' ,{'msg':'Set already exists'})
		return response
def create_card(request):
	retrieved_user = User.objects.get(username=request.user)
	sets = Set.objects.filter(user=retrieved_user)
	try:
		if request.POST:
			set_id = request.POST.get('setId')
			current_set = Set.objects.get(pk=set_id)
			request_term = request.POST.get('term')
			request_definition = request.POST.get('definition')
			card = Card(
				set = Set.objects.get(pk=set_id),
				term = request_term,
				definition = request_definition,
				)
			card.save()
			return render(request, 'quiz/editSet.html' ,{ 'languages': Language.objects.order_by('name'), 'set': current_set, 'cards': Card.objects.filter(set=current_set)})
	except IntegrityError as e:
		response = render(request, 'quiz/dashboard.html' ,{'msg':'Card already exists'})
		return response

def delete_card(request, card_id, set_id):
	card = Card.objects.get(pk=card_id)
	set = Set.objects.get(pk=set_id)
	card.delete()
	return render(request, 'quiz/editSet.html' ,{ 'languages': Language.objects.order_by('name'), 'set': set, 'cards': Card.objects.filter(set=set) })

def edit_card_form(request, card_id, set_id):
	card = Card.objects.get(pk=card_id)
	set = Set.objects.get(pk=set_id)
	return render(request, 'quiz/editCardForm.html' ,{ 'languages': Language.objects.order_by('name'), 'set': set, 'card': card })

# Triggered when OK is clicked. Needs card_id as part of get req body
def edit_card(request):
	retrieved_user = User.objects.get(username=request.user)
	sets = Set.objects.filter(user=retrieved_user)
	try:
		if request.POST:
			set_id = request.POST.get('setId')
			current_set = Set.objects.get(pk=set_id)
			request_term = request.POST.get('term')
			request_definition = request.POST.get('definition')
			card_id = request.POST.get('cardId')
			card_to_edit = Card.objects.get(pk=card_id)
			card_to_edit.term = request_term
			card_to_edit.definition = request_definition
			card_to_edit.save()
			return render(request, 'quiz/editSet.html' ,{ 'languages': Language.objects.order_by('name'), 'set': current_set, 'cards': Card.objects.filter(set=current_set)})
	except IntegrityError as e:
		response = render(request, 'quiz/dashboard.html' ,{'msg':'Card already exists'})
		return response