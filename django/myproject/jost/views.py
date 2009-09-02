# Create your views here.
from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader, Context
import Jost_Stats_Calc
import main_script

form_text = """"Title line: delete this example..
Locus 1
Locus 2
Pop
A , 001001 002002
A , 001001 002002
A , 002002 002002
A , 002002 002002
A , 002002 002002
A , 002002 001001
A , 002002 001001
A , 002002 001001
A , 002002 001001
A , 002002 001001
Pop
B , 002002 002002
B , 002002 002002
B , 001001 002002
B , 001001 002002
B , 001001 002002
B , 001001 001001
B , 001001 001001
B , 001001 001001
B , 001001 001001
B , 001001 001001"""




class index_form(forms.Form):
	genepop = forms.CharField(initial=form_text, widget=forms.Textarea())
	numb_of_replicates = forms.IntegerField(initial='0', 
											help_text=""" To reduce load on the server the maximum number of bootstrap
														replicates allowed is 1000. Setting the number of replicates to zero prevents
														your data set from being bootstrapped.""", 
														min_value=0, 
														max_value=1000, 
														widget=forms.TextInput(attrs={'size':'8'}))



def index(request):
	if request.method == 'POST':
		form = index_form(request.POST, auto_id=False)
		if form.is_valid():
			genepop_file = form.cleaned_data
			jost_results = main_script.main(genepop_file['genepop'], genepop_file['numb_of_replicates'])
			
			fstat = jost_results[0][0]				# fstat like results, jost table 1
			fstat_est = jost_results[0][1]			# estimated paramters
			bootstrap_est = jost_results[1]			# boostrapped results
			fstat_url = jost_results[2][0]
			fstat_est_url = jost_results[2][1]
			bootstrap_url = jost_results[2][2]
			matrix_url = jost_results[2][3]
			
			return render_to_response('jost/index.html',{'form':form, 
														'fstat':fstat, 
														'fstat_est':fstat_est, 
														'bootstrap_est':bootstrap_est, 
														'numb_of_replicates':genepop_file['numb_of_replicates'],
														'fstat_url': fstat_url,
														'fstat_est_url':fstat_est_url,
														'bootstrap_url':bootstrap_url,
														'matrix_url':matrix_url,
														})

		else:
			form = index_form(auto_id=False)
			return render_to_response('jost/index.html',{'form':form})
	
	else:
		form = index_form(auto_id=False)
		return render_to_response('jost/index.html',{'form':form})