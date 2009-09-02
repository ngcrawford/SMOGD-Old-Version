#!/usr/bin/env python
# encoding: utf-8
"""
popgen_format_parsers.py

Created by Nicholas Crawford on 2009-02-14.
Copyright (c) 2009 Boston Univeristy. All rights reserved.
"""
from numpy import *
from scipy import stats   # for calculating harmonic mean
import re
from Jost_Stats_Calc import *
from bootstrap import Bootstrap
import genotype_file_parsers as gfp


def main(data, numb_of_replicates,):	
	data = data.strip()												# get data
	file_info = gfp.determine_file_type(data)					# determine file type (e.g. mac, linux, PC)
	lines = data.split(file_info[0])									# splits on file type endings (e.g., \r\n or \n or \r)
	
	#  PROCESS DATA, FIND UNIQUE ALLELES
	#
	# 	Basic format of processed data:
	# [   [u'Locus 1', u'Locus 2'],
	#     [u'Species_w_20_loci', u'SpeciesB', u'SpeciesA'],
	#     [   [   [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002']],
	#	etc.. 
	
	
	# pick appropriate file parser
	if file_info[1] == 'Arlequin':										
		processed_data = gfp.arlequin_parser(lines)
		
	if file_info[1] == 'unknown':
		processed_data = gfp.genepop_parser(lines)
	
	# process data, etc.
	empty_dict = create_empty_dictionaries_of_unique_alleles(processed_data)  # create empty dictionaries of alleles in each locus
	
	allele_counts = generate_allele_counts(processed_data[0], processed_data[1], processed_data[2], empty_dict)
	
	population_sizes = generate_population_sizes(processed_data[2], processed_data[1], processed_data[0])		# dictionary of population sizes
	
	frequencies = generate_frequencies(processed_data, allele_counts)
	
	results = fstats(frequencies, processed_data[1], processed_data[0], population_sizes)
	
	bootstrap_results = Bootstrap(processed_data, numb_of_replicates)
	
	pairwise_stats = generate_pairwise_stats(processed_data[0], processed_data[1], processed_data[2])
	
	# create urls and files:
	fstats_url = update_csv_file('fstats',results[0])
	fstats_est_url = update_csv_file('est_stats',results[1])
	bootstrap_url = update_csv_file('bootstrap_results',bootstrap_results)
	matrix_url = update_csv_file('pairwise_matrices',pairwise_stats)
	
	return (results, bootstrap_results, (fstats_url,fstats_est_url,bootstrap_url, matrix_url))
