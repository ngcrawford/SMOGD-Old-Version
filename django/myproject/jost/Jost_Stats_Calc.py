#!/usr/bin/env python
# encoding: utf-8
"""
Jost_Stats_Calc.py

Created by Nicholas Crawford on 2008-12-13.
Copyright (c) 2008 Boston Univeristy. All rights reserved.
"""

from numpy import *
from scipy import stats
from copy import deepcopy
import time
import csv
# import pprint
# pp = pprint.PrettyPrinter(indent=4)

def create_empty_dictionaries_of_unique_alleles(processed_data):
	""" indentify all unique alleles in each locus in all populations
    make this as empty dictionaries with alleles as keys..."""
  
	numb_of_loci = len(processed_data[0])
	unique_loci_by_locus = {}
	
	for locus in range(numb_of_loci):
		unique_alleles = {}
		for pop in processed_data[-1]:
			pop = array(pop)					# create array so you can
			for allele in pop[:,locus]:			# slice by columns
				left = allele[:len(allele)/2]	# split allele pairs into left and right pieces
				right = allele[len(allele)/2:]
				for allele in (left,right):							# update dictionary alleles as keys
					unique_alleles[allele] = 0
						
		locus_name = processed_data[0][locus]
		unique_loci_by_locus[locus_name] = unique_alleles
	return unique_loci_by_locus
	

def generate_allele_counts(loci_names, pop_names, processed_data, count_dict):

	dict_of_counts = {}
	
	for locus in range(len(loci_names)):
		unique_alleles = {}
		pop_counter = 0
		for pop in processed_data:
			pop = array(pop)
			pop_loc_id = pop_names[pop_counter] + "||" + loci_names[locus] 
			current_locus_dict = count_dict[loci_names[locus]].copy()			# copy is important!
			pop_list = []
			# print pop_names[pop_counter]
			for genotype in pop[:,locus]:			# slice by columns
				if genotype == '000000':
					continue
				if genotype == '0000':
					continue
				if genotype == 'NA':
					continue
				if genotype == '00':
					continue
				if genotype == '0':
					continue
				if genotype == '??':
					continue
				if genotype == '?':
					continue
				if genotype == 'BADDNA':
					continue
			
				left = genotype[:len(genotype)/2]	# split allele pairs into left and right pieces
				right = genotype[len(genotype)/2:]
				current_locus_dict[left] += 1
				current_locus_dict[right] += 1
					
			dict_of_counts[pop_loc_id] = current_locus_dict	
			pop_list.append({})
			pop_counter += 1
	return dict_of_counts
	
def generate_frequencies(processed_data, allele_counts):
	loci_data_structure = []
	for locus in processed_data[0]:
		allele_freqs = generate_allele_frequencies(locus, processed_data[1], allele_counts)
		loci_data_structure.append(allele_freqs)
	return loci_data_structure

def generate_allele_frequencies(locus, pop_names, allele_counts):
	"""Get allele frequencies for each locus. Each column is a population. Each row is an allele."""
	pops_locus = sorted(allele_counts.keys())	# does this work with missing data?
	locus_list = []
	for pl in pops_locus:
		p_l = pl.split('||')				# split binomial names
		l = p_l[1]							# get locus name (l)
		if l == locus:						
			allele_freqs = []
			total_sum = sum(allele_counts[pl].values())		# get total sum
			allele_ids = sorted(allele_counts[pl].keys())	# this is a bit slow...
			for allele_id in allele_ids:
				allele_freqs.append(allele_counts[pl][allele_id]/float(total_sum))
			locus_list.append(allele_freqs)
	locus_list = array(locus_list)
	return locus_list

def generate_population_sizes(processed_data, population_names, loci_names ):
	# make empty locus dictinoary with empty lists
	locus_size_dict = {}
	for locus in loci_names:
		locus_size_dict[locus] = []
	pop_counter = 0
	for pop in processed_data:
		pop = array(pop)
		pop = column_stack(pop)
		locus_sizes = []
		locus_counter = 0
		for locus in pop:
			locus_len = 0
			for genotype in locus:
				if genotype == '000000':
					continue
				if genotype == '0000':
					continue
				if genotype == 'NA':
					continue
				if genotype == '0':
					continue
				if genotype == 'BADDNA':
					continue
				else:
					locus_len += 1
			locus_size_dict[loci_names[locus_counter]].append(locus_len)
			locus_counter +=1 
		pop_counter += 1
	return locus_size_dict


def fstats(locus_by_pop_freqs, population_names, loci_names, population_sizes):
	""" Calculate basic measures of diversity in Jost 2008. 
	     Results are for each locus across all populations"""

	def H_total(allele_freqs):
		"""method to calcluate Ht from a single locus."""
		allele_freqs = array(allele_freqs)						# convert to array so column stack will work
		allele_freqs_columns = column_stack(allele_freqs)		# make an array of indential alleles from each population

		# create list of squared averages of each allele:
		mean_squared_list = []
		for column in allele_freqs_columns:
			mean_squared = pow(mean(column),2)					# calculate mean of like alleles and then square
			mean_squared_list.append(mean_squared)				# append to 'storage list'

		# calculate Ht
		Ht = 1-sum(mean_squared_list)						# sum squared allele frequencies and subtract from 1
		return Ht

	def H_sub(allele_freqs):
		"""calcluate Hs from a single locus."""
		allele_freqs = array(allele_freqs)						# convert allele freqs to numpy array
		allele_freqs_squared = pow(allele_freqs,2)				# square freqs

		# create list of Hexps.  One Hexp per population
		Hexp_for_pop_list = []
		for pop in allele_freqs_squared:
			Hexp = 1 - sum(pop)
			Hexp_for_pop_list.append(Hexp)
		Hs = mean(Hexp_for_pop_list)							# calculate Hs
		return Hs

	def calc_harmonic_mean(population_sizes):
		"""calculates harmonic mean from list of integers"""
		n = len(population_sizes)
		denominator = 0
		for pop in population_sizes:
			fract = 1/float(pop)
			denominator = denominator + fract
		return n/denominator

	# storage lists
	basic_results = []
	est_results = []
	results = []			# this list contains the final set (two lists) or basic and est results
	
	# universal parameters (e.g. n, N_harmonic_mean)
	list_of_pop_sizes = array(population_sizes.values()) # not in population order
	n = float(len(population_names))

	locus_counter = 0
	for locus in locus_by_pop_freqs:
		N_harmonic = calc_harmonic_mean(population_sizes[loci_names[locus_counter]])
		# N_harmonic = stats.hmean(population_sizes[loci_names[locus_counter]])
		Locus = loci_names[locus_counter]
		
		# Per Locus parameters
		Hs = H_sub(locus)
		Ht = H_total(locus)
		
		Hs_est = ((2*N_harmonic)/(2*N_harmonic-1))*Hs
		Ht_est = Ht+Hs_est/(2*N_harmonic*n)
		
		# Basic Equations
		Hst = (Ht-Hs)/(1-Hs)
		delta_s = pow((1-Hs),-1)
		delta_t = pow((1-Ht),-1)
		delta_st = delta_t/delta_s
		delta_s_delta_t = delta_s/delta_t 
		Hs_Ht = Hs/Ht 
		Dst = Ht-Hs													# Nei's Dst (absolute differentiation)
		Gst = (Dst)/Ht												# Nei's Gst (relative differentiation)
		D = ((Ht-Hs)/(1-Hs))*(n/(n-1))								# Jost's D
		
		# Estimated Parameters for small sample sizes
		G_est = (Ht_est-Hs_est)/Ht_est
		G_Hedrick = (G_est*(n-1+Hs_est))/((n-1)*(1-Hs_est))
		D_est = ((Ht_est-Hs_est)/(1-Hs_est))*(n/(n-1))
		# print "Locus, n,  Hs, Ht, Dst, Gst, Hst, delta_st, D, Hs_Ht, delta_s_delta_t"
		# print Locus, n, Hs, Ht, Dst, Gst, Hst, delta_st, D, Hs_Ht, delta_s_delta_t
		basic_results.append([Locus, n, Hs, Ht, Dst, Gst, Hst, delta_st, D, Hs_Ht, delta_s_delta_t])
		est_results.append([Locus, N_harmonic, Hs_est, Ht_est, G_est, G_Hedrick, D_est])
		locus_counter += 1
	
	print est_results
	
	for result in est_results:
		print result[6]
	return (basic_results, est_results)
	
def generate_pairwise_stats(loci_names,population_names,populations):
	""" generates a pairswise distance matices of G_est, G_Hedrick (G'st) and Dest for each locus"""
	
	counter = 0
	list_of_rows = []
	list_of_dicts = []
	pop_len = len(populations)
	
	est_parameters = {'G_est':[], 'G_Hedrick':[], 'D_est':[]}

	dict_pairwise_tables = {}
	for locus in loci_names:
		dict_pairwise_tables[locus] = deepcopy(est_parameters)			# deep copy is key!

	for pop in populations:
		current_row = []
		current_multi_row = deepcopy(dict_pairwise_tables)
		if len(populations[counter+1:]) > 0:				# don't append empty list!
			counter_2 = counter+1

			for pop_2 in populations[counter+1:]:

				current_row.append(pop_2)
				pop_duo_names =  [population_names[counter], population_names[counter_2]]
				processed_data = [loci_names,pop_duo_names,[pop,pop_2]]
				empty_dict = create_empty_dictionaries_of_unique_alleles(processed_data)  # create empty dictionaries of alleles in each locus
				allele_counts = generate_allele_counts(processed_data[0], processed_data[1], processed_data[2], empty_dict)
				population_sizes = generate_population_sizes(processed_data[2], processed_data[1], processed_data[0])		# dictionary of population sizes
				frequencies = generate_frequencies(processed_data, allele_counts)
				results = fstats(frequencies, processed_data[1], processed_data[0], population_sizes)
				# print pop_duo_names, results[1]

				for locus in results[1]:
					current_multi_row[locus[0]]['G_est'].append(locus[4])
					current_multi_row[locus[0]]['G_Hedrick'].append(locus[5])
					current_multi_row[locus[0]]['D_est'].append(locus[6])

				counter_2 += 1
			list_of_dicts.append(current_multi_row)

		counter +=1	

	pop_len = len(population_names)

	# make the top row of the matirx
	top_row = deepcopy(population_names)
	top_row.insert(0,'--')

	# make printable data structure...
	pop_matices_ready_for_csv = []
	parameter_values = sorted(est_parameters.keys())
	for locus in loci_names:
		for parameter in parameter_values:

			pop_matices_ready_for_csv.append([locus, parameter])
			pop_matices_ready_for_csv.append(top_row)
			counter = 0

			for item in list_of_dicts:
				current_row = item[locus][parameter]
				num_of_zeros = pop_len - len(current_row)

				for x in range(num_of_zeros):
					current_row.insert(0,'na')							# write matrix rows
				current_row.insert(0,population_names[counter])

				pop_matices_ready_for_csv.append(current_row)

				if num_of_zeros == pop_len - 1: 
					final_row = []
					for x in range(pop_len):
						final_row.append('na')							# write final matrix row
					final_row.insert(0,population_names[counter+1])

					pop_matices_ready_for_csv.append(final_row)
				counter += 1

	return tuple(pop_matices_ready_for_csv)

def update_csv_file(header,data):
	timestamp = time.localtime()
	timestamp = "%s%s%s%s%s%s%s%s%s" % timestamp[:]  # (2009, 4, 17, 13, 57, 28, 4, 107, 1)
	filename = '/home/ngcrawford/webapps/web_media/temp_files/'+header+'_'+ timestamp +'.txt'
	#filename = '/Users/nick/Web_Design/django_templates/media/temp_files/'+header+'_'+ timestamp +'.csv'  # uncomment for online
	filename = '/Users/nick/Web_Design/django_templates/media/temp_files/'+header+'_'+ timestamp +'.txt'	# local
	url = '/web_media/temp_files/'+header+'_'+ timestamp +'.txt'
	data_writer = csv.writer(open(filename, 'w'), delimiter='\t', quotechar='|')
	for row in data:
		data_writer.writerow(row)
	return url

