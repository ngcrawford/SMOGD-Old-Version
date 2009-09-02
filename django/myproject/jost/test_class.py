from pyparsing import *

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
	
def main(filename):
	
	tests = (
    "NbSamples=3",
    "GenotypicData=1",
    "GameticPhase=0",
    "RecessiveData=0",
    "DataType=MICROSAT",
    "LocusSeparator=WHITESPACE",
    "MissingData='?'",
    "CompDistMatrix=1",
	"Title='Anolis marmoratus trinucleotide repeats'"
	)

	# parsing profile
	
	keyword 		= Word(alphas+"'").setResultsName('keyword')
	equals 			= Literal('=')
	value 			= OneOrMore(Word(alphas+nums+"?'")).setResultsName("value")
	
	profile_properties = keyword + equals + value
	
	for line in tests:
		results =  profile_properties.parseString(line)
		print results.keyword
		print results.value
	
	
main("/Users/nick/Desktop/django/myproject/arlequin_example_file.txt")
