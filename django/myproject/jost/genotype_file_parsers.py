from numpy import *
import re

def arlequin_parser(lines):
	"""parse arlequin popgen format into """
	
	# 	Basic format of processed data:
	# [   [u'Locus 1', u'Locus 2'],
	#     [u'Species_w_20_loci', u'SpeciesB', u'SpeciesA'],
	#     [   [   [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002']],


	def process_allele_lines(allele_lines):
		left_alleles = allele_lines[0][2:]
		right_alleles = allele_lines[1]
		allele_pairs = zip(left_alleles,right_alleles)
		genotypes = []
		for allele_pair in allele_pairs:
			genotype = ''.join(allele_pair)
			genotypes.append(genotype)
		return genotypes

	def get_loci_names(line):
		if line.find('Data for'):
			line = line.strip()
			line = line.split(':')
			line = line[1].split()
			return line
		else: 
			return False	 # no loci

	# switches
	profile_switch = False
	data_switch = False
	samples_switch = False
	sample_data_switch = False
	structure_switch = False
	pop_switch = False

	# parameters
	pop_names = []
	loci_names = []
	allele_lines = []

	list_of_pop_genotypes = []

	for line in lines:								# loop through lines in file
		if line.find('[Profile]') != -1:			# set profile switch
			profile_switch = True
	
		if line.find('[Data]') != -1:				# set data switch
			data_switch = True
	
		if line.find('[[Samples]]') != -1:			# set samples switch
			samples_switch = True
			loci_names = get_loci_names(line)
		
		if line.find('[[Structure]]') != -1:		# set structure switch
			structure_switch = True
		
		if samples_switch == True and structure_switch == False:	# if in 'Population' Section do stuff
		
			if line.strip().split('=')[0] == 'SampleName':			# find population name
				name = line.strip().split('=')[1].strip("\"")
				pop_names.append(name)
				population_genotypes = []							# state making storage list of genotype info
			
			if line.strip()[-1] == "}":								# id end of population
				pop_switch = False
				list_of_pop_genotypes.append(population_genotypes)	# update storage list of population genotypes
			
			if sample_data_switch == True and pop_switch == True:	# if in individuals in population
		
				allele_lines.append(line.strip().split())			# setup pairs of list (right and left alleles)
				if len(allele_lines) == 2:
					genotypes = process_allele_lines(allele_lines)	# send individual's set of alleles to be ziped into genotypes
					population_genotypes.append(genotypes)
					allele_lines = []								# empty list for next individual
			
			if line.strip().split('=')[0] == 'SampleData':			
				pop_switch = True
			
			if line.strip().split('=')[0] == 'SampleData':
				sample_data_switch = True
				
		else:pass
		

	loci_names = range(1,(len(list_of_pop_genotypes[0][0]))+1)		# make a list of anonymous locus names starting with 1 to total number	
	loci_names = map(str, loci_names)								# convert loci name, currently integers, to strings

	return [loci_names,pop_names,list_of_pop_genotypes]


def genepop_parser(lines):
	"""process genpop lines into multidimentional array"""
	header = lines[0].strip() 			# header info
	loci_names = []
	all_loci = []
	loci_list = []
	population_names = []
	pops_flag = 0						# zero indicates in population names
	population_name = ''				# use to find first line of a population
	loci_on_multiple_lines = True
	line_counter = 0					# tracks index of current line
	# REGEX stuff
	pattern = re.compile('pop', re.IGNORECASE)
	loci_punct = re.compile(',(?:\s*)|\s*')
	
	# GenePop Format Test
	if pattern.match(lines[2]):						# assumes multiple populations...
		loci_names = loci_punct.split(lines[1])
		loci_on_multiple_lines = False
	
	for line in lines[1:]:							# skip header line
		line = line.strip()							# clean whitspace
		line_match = pattern.match(line)

		# DO STUFF WITH POPULATIONS
		if pops_flag >= 1:
			if line_match == None:
				line_parts = line.split(',')						# split line with populations
				loci = line_parts[1].strip()						# id loci
				loci_list.append(loci.split())						# add loci to loci list
		
		# FLAG POPULATION AND UPDATE STORAGE LIST (All_Loci)
		if line_match:				# Flag Pops
			population_name = lines[line_counter+2].split()[0]		# get current pop name
			population_names.append(population_name)
			pops_flag += 1
			if pops_flag >= 2:
				all_loci.append(loci_list)
			loci_list = []
		
		# PUT POPULATION NAMES IN A LIST
		if pops_flag == 0:				# get population names
			if loci_on_multiple_lines == True:
				loci_names.append(line)		# make list of population names
				
		line_counter += 1
			
	all_loci.append(loci_list)			# add last set of locus to all_loci
	return [loci_names, population_names, all_loci]

def unique_alleles_per_locus(loci):
	"""create empty dictionary with keys for each allele in data set"""
	dict_of_alleles = {}
	for locus in loci:
		for row_of_allele_pairs in locus:
			for allele_pair in row_of_allele_pairs:
					left_allele = int(allele_pair[:len(allele_pair)/2])		# split allele pair e.g. ))				
					right_allele = int(allele_pair[len(allele_pair)/2:])
					dict_of_alleles[left_allele] = 0						# make sure dictionary is empty
					dict_of_alleles[right_allele] = 0
	return dict_of_alleles
	
	
def population_parser(population,unique_alleles):

	sorted_allele_ids = sorted(unique_alleles.keys())  # make list of sorted alleles
	dict_of_loci_lists = unique_alleles.copy()
	final_array = []
	
	for item in range(len(population[0])):
		locus = []
		unique_locus = unique_alleles.copy()
		
		
		for row in population:
			locus.append(row[item])
		
		for allele in locus:
				left_allele = int(allele[:len(allele)/2])
				right_allele = int(allele[len(allele)/2:])
				unique_locus[left_allele] = unique_locus[left_allele] + 1
				unique_locus[right_allele] = unique_locus[right_allele] + 1
		
		total_numb_alleles = float(sum(unique_locus.values()))

		for allele_id in sorted_allele_ids:
			allele_freq = unique_locus[allele_id]/total_numb_alleles
			if dict_of_loci_lists[allele_id] == 0:
				dict_of_loci_lists[allele_id] = [allele_freq]
			else:
				dict_of_loci_lists[allele_id].append(allele_freq)
	
	
	for allele_id in sorted_allele_ids:
		final_array.append(dict_of_loci_lists[allele_id])
	final_array = array(final_array)
	return final_array

def determine_file_type(file_string):
	"""docstring for determine_file_type"""
	os = ""
	file_format = 'unknown'
	
	# DETERMINE OS ENDING TYPE
	if file_string.find('\r') != -1:
		os = "\r"
	if file_string.find('\n')  != -1:
		os = "\n"
	if file_string.find('\r\n') != -1:
		os = "\r\n"
	
	# DETERMINE FILE FORMAT
	if file_string.find('[Profile]') != -1:  # [Profile] is only found in the first line of Arlequin files
		file_format = 'Arlequin'
		
	return (os, file_format)

