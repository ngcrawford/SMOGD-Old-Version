#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Nicholas Crawford on 2009-04-11.
Copyright (c) 2009 Boston Univeristy. All rights reserved.
"""
import scipy as sp
import numpy as np
from Jost_Stats_Calc import *
#import pprint
# pp = pprint.PrettyPrinter(indent=4)
# from copy import deepcopy


# processed_data = [   [u'Locus 1', u'Locus 2'],
#     [u'SpeciesA', u'SpeciesB'],
#     [   [   [u'001001', u'001001'],
#             [u'001001', u'001001'],
#             [u'001001', u'001001'],
#             [u'002002', u'002002'],
#             [u'002002', u'002002'],
#             [u'002002', u'002002']],
#         [  [u'001001', u'001001'],
#            [u'001001', u'001001'],
#            [u'001001', u'001001'],
#            [u'002002', u'002002'],
#            [u'002002', u'002002'],
#            [u'002002', u'002002'],
# 		   [u'002002', u'002002'],
# 		   [u'000000', u'000000']]]]


processed_data = [   [u'Locus 1', u'Locus 2'],
				     [u'A', u'B', u'C'],
				     [  [   [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001']],
				        [   [u'001001', u'002001'],
				            [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'001001', u'002002'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001']],
				        [   [u'001001', u'001001'],
				            [u'001001', u'001001'],
				            [u'001001', u'001001'],
				            [u'001001', u'001001'],
				            [u'001001', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001'],
				            [u'002002', u'001001']]]]

"""
store mean of measure(s) as dict
within loop of X number of replicates:
	1.) for each population resample inviduals
	2.) recreate data formate
	3.) calculate diversity measures
"""


def Create_Bootstrap_Replicate(data):
	"""loop through populations creating new sample of each population
		probably try to avoid creating copies, just draw from original
		population each time."""
	genotypes_by_population = data[2]
	bootstrap_replicate = []
	for pop in genotypes_by_population:
		pop = np.array(pop)
		sample_size = len(pop)
		choices = sp.random.random_integers(0, sample_size-1, sample_size)
		sample = pop[choices]
		bootstrap_replicate.append(sample)  # this may slow things down as it requires creating a new array
	result = [data[0], data[1], bootstrap_replicate]
	return result
	
def Bootstrap(processed_data, numb_of_replicates):

	if numb_of_replicates == 0:
		bootstrap_results = []
		return bootstrap_results

	initial_numb_of_replicates = copy(numb_of_replicates)
	bootstrap_results = []
	Dest_storage_list = []
	empty_dict = create_empty_dictionaries_of_unique_alleles(processed_data)
	boot_est_parameters = {'Hs_est':[], 'Ht_est':[], 'G_est':[], 'G_Hedrick':[], 'D_est':[]}

	# could make this a general fuction and call 
	# it once in 'main' (very modest speed improvement perhaps)

	locus_dict = {}							# dict with loci and empty lists
	for locus in processed_data[0]:
		locus_dict[locus] = deepcopy(boot_est_parameters)			# deepcopy is really important!
	
	while numb_of_replicates != 0:
		# 1. create replicate
		replicate = Create_Bootstrap_Replicate(processed_data)
		# 2. get measurements from replicate
		allele_counts = generate_allele_counts(replicate[0], replicate[1], replicate[2], empty_dict)
		population_sizes = generate_population_sizes(replicate[2], replicate[1], replicate[0])
		frequencies = generate_frequencies(replicate, allele_counts)
		results = fstats(frequencies, replicate[1], replicate[0], population_sizes)
		
		# 3. save lists of results to dictionary of loci and parameters...
		for locus in results[1]:
			# not adding just to the specific dict key
			locus_dict[locus[0]]['Hs_est'].append(locus[2])
			locus_dict[locus[0]]['Ht_est'].append(locus[3])
			locus_dict[locus[0]]['G_est'].append(locus[4])
			locus_dict[locus[0]]['G_Hedrick'].append(locus[5])
			locus_dict[locus[0]]['D_est'].append(locus[6])

		numb_of_replicates -= 1
	
	# unpack results and calculate stats (mean, variance)
	for locus in processed_data[0]:
		for parameter in ['Hs_est', 'Ht_est', 'G_est', 'G_Hedrick', 'D_est']:
			bootstrapped_parameters = locus_dict[locus][parameter]
			# calculate C.I @ 95% cutoff
			
			sorted_bootstrapped_parameters = np.sort(bootstrapped_parameters)
			min_five_percent = int(abs(initial_numb_of_replicates*.04))
			max_five_percent = int(abs(initial_numb_of_replicates*.96))
			min_CI = sorted_bootstrapped_parameters[min_five_percent]
			max_CI = sorted_bootstrapped_parameters[max_five_percent]
			
			bootstrap_results.append([locus, parameter, np.mean(bootstrapped_parameters), np.var(bootstrapped_parameters), sp.stats.tsem(bootstrapped_parameters), min_CI, max_CI])
	return bootstrap_results

Bootstrap(processed_data, 100)

