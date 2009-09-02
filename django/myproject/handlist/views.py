# Create your views here.
from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from webapps.handlist import parse_handlist_2_database


# from my_webapps.handlist.parse_handlist_2_database import main

class UploadFileForm(forms.Form):
    file  = forms.FileField()

class CharactersForm(forms.Form):
    abbreviation = forms.CharField(max_length=10)
    character = forms.CharField(max_length=30)
    definition = forms.CharField(max_length=6000, widget=forms.Textarea)
    comment = forms.CharField(max_length=6000, widget=forms.Textarea)

# ======================================================================
#	Helper Fuctions: (move to own file at some point in the future)
# ======================================================================

def handle_uploaded_file(f):
    for chunk in f.chunks():
        print chunk


# =======================
#	Define Pages:
# =======================


def index(request):
	if request.method == 'GET':
		main_text = 'home'
		return render_to_response('handlist/index.html', {'main_text':main_text})
	else:
		return render_to_response('handlist/index.html')
		
def index_2(request):
	""" use this page for trying out new html ideas"""
	return render_to_response('handlist/index_2.html')

def add_data(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():  # checks if there is data and if it is valid
			file_data = request.FILES['file']
			text = file_data.read()
			text = text.split('\r')  # convert to list
			parse_handlist_2_database.main_script(text) 
			return render_to_response('handlist/add_data.html', {'form':form, 'file_data':file_data, 'text':text})
	else:
		form = UploadFileForm()
		return render_to_response('handlist/add_data.html', {'form':form})


def chars(request):
	if request.method == 'POST':
		all_characters = Characters.objects.all().order_by('character')
		character_values = CharacterStates.objects.all()
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():  # checks if there is data and if it is valid
			print request.FILES, request.FILES.keys()
			handle_uploaded_file(request.FILES['file'])
			return render_to_response('handlist/chars.html', {'form':form,'current_data':all_characters, 'character_values':character_values})
	else:
		all_characters = Characters.objects.all().order_by('character')
		character_values = CharacterStates.objects.all()
		form = UploadFileForm()
		return render_to_response('handlist/chars.html', {'form':form, 'current_data':all_characters, 'character_values':character_values})