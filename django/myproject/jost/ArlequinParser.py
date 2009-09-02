import genotype_file_parsers

def get_info_value(line,split_value):
	line = line.strip()
	line_parts = line.split(split_value)
	return line_parts[1].strip()

def inProfile(line):
	if line.find('NbSamples') != -1:
		NbPops = get_info_value(line,'=')
		print NbPops
	if line.find('GenotypicData') != -1:
		GenotypicData = get_info_value(line,'=')
		print GenotypicData
	if line.find('GameticPhase') != -1:
		GameticPhase = get_info_value(line,'=')
		print GameticPhase
	if line.find('RecessiveData') != -1:
		RecessiveData = get_info_value(line,'=')
		print RecessiveData
	if line.find('DataType') != -1:
		DataType = get_info_value(line,'=')
		print DataType
	if line.find('LocusSeparator') != -1:
		LocusSeparator = get_info_value(line,'=')
		print LocusSeparator
	if line.find('MissingData') != -1:
		MissingData = get_info_value(line,'=')
		MissingData = MissingData.strip("'")			# remove quotes from missing data
		print MissingData
	if line.find('CompDistMatrix') != -1:
		CompDistMatrix = get_info_value(line,'=')
		print CompDistMatrix


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
	else: return False	 # no loci

def get_lines_from_file(filename):
	fin = open(filename,'r')
	lines = []
	for line in fin:
		line = line.strip()
		lines.append(line)
	return lines

def arlequin_parser(lines):
	# 	Basic format of processed data:
	# [   [u'Locus 1', u'Locus 2'],
	#     [u'Species_w_20_loci', u'SpeciesB', u'SpeciesA'],
	#     [   [   [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002']],

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
				name = line.strip().split('=')[1]
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
		
	return [loci_names,pop_names,list_of_pop_genotypes]
	
	
x = get_lines_from_file("/Users/nick/Desktop/django/myproject/arlequin_example_file.txt")
z = arlequin_parser(x)
print z