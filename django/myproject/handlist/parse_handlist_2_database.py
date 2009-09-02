#!/usr/bin/env python
import codecs	# deal with unicode characters
import re
import pprint

from django.db import connection
# import models:  (mulitple lines to aid viewing)
from webapps.handlist.models import Characters, CharacterStates, CharacterData 
from webapps.handlist.models import Author, AuthorLiteratureId, Species, Anatomy 
from webapps.handlist.models import Behavior, Color, Ecology, Literature, Range, Synonymy

pp = pprint.PrettyPrinter(indent=4)

# create fuctions to assist with parsing:

def get_citation_id(citation, current_species):
	"""docstring for generate_search_terms_from_citation"""
	citation = citation.replace('and','&')
	punct = re.compile("[&\s]")
	search_terms = punct.split(citation)
	final_search_terms = []
	for item in search_terms:
		if len(item) > 3:
			item = item.strip(',')
			final_search_terms.append(item)
	search_terms = final_search_terms
	try:
		# use species ID
		matching_article = Literature.objects.get(species_id_id = current_species.species_id, temp_citation__icontains = search_terms[0], temp_citation__icontains = search_terms[1])
	except Exception, DoesNotExist:
		# don't use species ID
		matching_article = Literature.objects.filter(temp_citation__icontains = search_terms[0], temp_citation__icontains = search_terms[1])
		matching_article =  matching_article[0]  #not ideal... just returns first match...
	return matching_article


def get_genus_species_describer(item):
	items = item.split()
	genus = items[0]
	species = items[1]
	describer = items[2]
	return {'genus':genus,'species':species,'describer':describer}

def get_synonymy_info(item):
	species_dict = {}
	x =  re.split("\\x0b",item)  # split on non printing character...
	for item in x:
		if item.find("TYPE LOCALITY:") != -1:
			items = item.split("TYPE LOCALITY:")
			subspecies_info = items[0].strip().split()
			subspecies = subspecies_info[2]
			species = subspecies_info[2].strip()
			locality = items[1].strip()
			species_dict[subspecies] = locality
	return species_dict

def get_anatomy_info(line,current_species):
	"""docstring for get_anatomy_info"""	
	if len(line) == 0:
		pass	
	else:
		for body_part in line:
			body_part = body_part.strip(u'\u2022 ').strip()
			body_part = body_part.split(':',2)
			organ = body_part[0]
			citation = body_part[1]
			notes = body_part[2]
			matching_article = get_citation_id(citation, current_species) # get matching article from literature
			Anatomy.objects.create(species_id_id = current_species.species_id, literature_id_id = matching_article.literature_id,  organ = organ, notes = notes)

def get_behavior_info(line, current_species):
	if len(line) == 0:
		Behavior.objects.create(species_id_id = 5000, literature_id_id = 5000, notes = 'Currently no data (NGC)')
	else:	
		citation = line[:line.find(":")]
		print citation
		notes = line[line.find(":"):]
		matching_article = get_citation_id(citation, current_species)# get matching article from literature
		Behavior.objects.create(species_id_id = current_species.species_id, literature_id_id = matching_article.literature_id, notes = notes)


def get_color_info(line, current_species):
	line = re.split("\\x0b",line)
	for body_part in line:
		
		if len(body_part) != 3:
			continue
		
		#matching_article = Literature.objects.get(temp_citation__icontains = search_terms[0], temp_citation__icontains = search_terms[1]) # get matching article from literature
		body_part = body_part.strip(u'\u2022 ').strip()
		body_part = body_part.split(':',2)
		organ = body_part[0]
		citation = body_part[1]
		notes = body_part[2]
		matching_article = get_citation_id(citation, current_species) # get matching article from literature
		Color.objects.create(species_id_id = current_species.species_id, literature_id_id = matching_article.literature_id,  organ = organ, notes = notes)

def get_ecology_info(line,current_species):

	if len(line) == 0:
		Ecology.objects.create(species_id_id = 5000, literature_id_id = 5000, notes = 'Currently no data (NGC)')
	
	else:
		ref = line.split(':',1)
		citation = ref[0]
		notes = ref[1]
		if citation.find('ECOLOGY') != -1:
			ref = line.split(':',2)
			citation = ref[1]
			notes = ref[2]
		matching_article = get_citation_id(citation, current_species)
		Ecology.objects.create(species_id_id = current_species.species_id, literature_id_id = matching_article.literature_id, notes = notes)

def get_literature_info(line):
	articles = line.split('\x0b')
	for article in articles:
		article = article.split('.')
	return {'articles':articles}

def get_range_info(line,current_species):
	"""docstring for get_range_info"""
	first_period = line.find('.',1)
	species_range = line[:first_period]
	species_range = line[:first_period+1].strip()
	two_letter_code = species_range[:species_range.find(':')]
	if len(two_letter_code) != 2:
		two_letter_code = '' 
	countries = species_range[species_range.find(':')+1:].strip()
	notes = line[first_period+1:].strip()
	countries = countries.title()
	Range.objects.create(species_id_id = current_species.species_id, two_letter_code = two_letter_code, countries = countries, notes = notes)

def truncate_tables_in_database():
	cursor = connection.cursor()
	tables = ['Species', 'literature', 'Author', 'Species', 'anatomy', 'behavior', 'color', 'ecology', 'range', 'synonymy', ]
	for table in tables:
		query = 'truncate table ' + table
		cursor.execute(query)
	Literature.objects.create( literature_id = 5000, species_id_id = 5000, temp_citation = 'place holder citation')

# main script
def main_script(fileObj):
	"""Comments: the file object is actually a list of lines..."""
	
	truncate_tables_in_database()
	line_count = 0
	for line in fileObj:
		line = unicode(line, "utf-8")  # convert line to unicode
		if line_count > 0:  # ignore first line...
			line = line.split('\t')		# split on Tab character
			
			species_dict = get_genus_species_describer(line[0])
			Species.objects.create(describer = species_dict['describer'], genus = species_dict['genus'], species = species_dict['species']) 
			current_species = Species.objects.get(species = species_dict['species'])  #note using 'get' is key here... don't want an array!
			
			for item in get_synonymy_info(line[1]).items():
				Synonymy.objects.create(species_id_id = current_species.species_id, author = 'none',  subspecies = item[0], type_locality = item[1])
			
			for article in get_literature_info(line[7].strip())['articles']:
				Literature.objects.create(species_id_id = current_species.species_id, temp_citation = article)
			
			
			# call functions:
			get_behavior_info(line[4].strip(), current_species)
			get_color_info(line[5].strip(), current_species)
			get_anatomy_info(line[3].strip(),current_species)
			get_ecology_info(line[6].strip(), current_species)
			get_range_info(line[2].strip(), current_species)

			# ======= not yet working ===============
			character_data = line[8:-1]

		if line_count >= 15:
			break
		line_count += 1
