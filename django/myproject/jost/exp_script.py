from numpy import *
from scipy import stats
import pprint
from Jost_Stats_Calc import *
from copy import deepcopy
import csv
import time
pp = pprint.PrettyPrinter(indent=4)

# processed_data = [   [u'Locus 1', u'Locus 2'],
# 				     [u'A', u'B', u'C'],
# 				     [  [   [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001']],
# 				        [   [u'001001', u'002001'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001']],
# 				        [   [u'001001', u'002001'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'001001', u'002002'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001'],
# 				            [u'002002', u'001001']]]]


processed_data = [   [u'Locus 1', u'Locus 2'],
    [u'SpeciesA', u'SpeciesB', u'SpeciesC','SpeciesD'],
    [   [   [u'001001', u'001001'],
            [u'001001', u'001001'],
            [u'001001', u'001001'],
            [u'001001', u'002002'],
            [u'001001', u'002002'],
            [u'001001', u'002002']],
        [  [u'002002', u'001001'],
           [u'002002', u'001001'],
           [u'002002', u'001001'],
           [u'002002', u'003003'],
           [u'002002', u'003003'],
           [u'002002', u'003003'],
		   [u'002002', u'003003'],
		   [u'000000', u'000000']],
		[  [u'003003', u'001001'],
           [u'003003', u'001001'],
           [u'003003', u'001001'],
           [u'003003', u'002002'],
           [u'003003', u'002002'],
           [u'003003', u'002002'],
		   [u'003003', u'002002'],
		   [u'000000', u'000000']],
		[  [u'004004', u'001001'],
           [u'004004', u'001001'],
           [u'004004', u'001001'],
           [u'004004', u'002002'],
           [u'004004', u'002002'],
           [u'004004', u'002002'],
		   [u'004004', u'002002'],
		   [u'000000', u'000000']]]]

def generate_pairwise_stats(loci_names,population_names,populations):

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
	data_writer = csv.writer(open('tab_delimited_data_'+ timestamp +'.txt', 'w'), delimiter='\t',  quotechar='|')
	for row in data:
		print row
		data_writer.writerow(row)
	

def main():
	
	# summarize data:
	empty_dict = create_empty_dictionaries_of_unique_alleles(processed_data)  # create empty dictionaries of alleles in each locus
	population_sizes = generate_population_sizes(processed_data[2], processed_data[1], processed_data[0])		# dictionary of population sizes
	allele_counts = generate_allele_counts(processed_data[0], processed_data[1], processed_data[2], empty_dict)
	frequencies = generate_frequencies(processed_data, allele_counts)
	
	# generate statistics:
	pairwise_stats = generate_pairwise_stats(processed_data[0], processed_data[1], processed_data[2])
	fstats_measures = fstats(frequencies, processed_data[1], processed_data[0], population_sizes)
	
	# create output
	update_csv_file('pairwise matrices',pairwise_stats)
	

main()