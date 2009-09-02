import re
import pprint
import codecs	# deal with unicode characters
import MySQLdb
conn = MySQLdb.connect(host = "localhost", user = "nick", passwd = "valve123", db = "my_webapps")
cursor = conn.cursor()

fin = open('anohandlist_definitions.txt', "r") # read as unicode


def convertlist2dict(mylist):
	"""docstring for convertlist2dict"""
	final_dict = {}
	while len(mylist) != 0:
		mypair = mylist[:2]
		final_dict[mypair[0]] = mypair[1]
		mylist = mylist[2:]
	return final_dict
		


def make_dictionary_of_characters():
	"""docstring for di"""
	character_states_dict = {}
	line_count = 0
	for line in fin:
		x =  re.search("\xe2",line) # find lines with bullet characters
		if x != None:
			temp = re.search('Fig',line) # find 'Fig' citation at end of line
			colons = re.search(':',line)
			if temp != None:
				line = line[colons.start():temp.start()]
				line_parts = re.split('[:\.]',line)
				line_parts = map(lambda value: value.strip(), line_parts)
				line_parts = line_parts[:-1]
				line_count += 1
		
			if temp == None:
				line = line[colons.start():]
				line_parts = re.split('[:\.]',line)
				line_parts = map(lambda value: value.strip(), line_parts)
				line_parts = line_parts[:-1]
				line_count += 1
			
			# print line_parts
			# print unicode(line,'utf-8')
			# print line_parts[1].lower(), line_parts[2:]
		
			if len(line_parts[2:]) % 2 != 0:
				line_elements = line_parts[2:]
				line_elements.insert(0,'range')
				character_name = line_parts[1].lower()
				characters_dict = convertlist2dict(line_elements)
				character_states_dict[character_name] = characters_dict
			else:
				character_name = line_parts[1].lower()
				line_elements = line_parts[2:]
				characters_dict = convertlist2dict(line_elements)
				character_states_dict[character_name] = characters_dict
				
				
	
	return character_states_dict
	

DoC = make_dictionary_of_characters()
for key, value in DoC.items():
	print key, value
	query = """ select characters_id from Characters C where C.character = '""" + key + """'"""
	cursor.execute(query)
	row = cursor.fetchone()
	characters_id = row[0]
	
	for character, accepted_value in value.items():
		cursor.execute("""insert into Character_States (characters_id, state, accepted_values) values (%s, %s, %s)""", (characters_id, character, accepted_value)) 
	 	conn.commit()
fin.close() 
