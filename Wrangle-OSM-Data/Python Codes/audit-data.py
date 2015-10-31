"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE = "singapore.osm"

street_type_re = re.compile(r'(\b\S+\.?$)|(\b\S+\.?\s+\d+$)', re.IGNORECASE)
#checks for strings starting with J or L
malay_type_re = re.compile(r'(^J\S+)|(^L\S+)', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
"Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Central",
"Circle", "Close", "Crescent", "Link", "Park", "Terrace", "Walk",
"View", "Way", "Quay", "Hill", "Rise", "Loop", "Vale", "Gardens", "Plains", "Estate", 
"Green", "Field", "Grove"]

malay = ["Lorong", "Jalan"]

mapping = { "St": "Street",
            "St.": "Street",
            "Ave.": "Avenue",
            "Ave": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Lor": "Lorong",
            "Jln": "Jalan",
            "Aenue":"Avenue",
            "Avebue":"Avenue"
            "Cresent":"Crescent"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    #splits street_name to obtain first word for comparison against malay
    first = street_name.split()
    if m:
        street = m.group()
        street_type = street.split()
        if (street_type[0] not in expected) and (first[0] not in malay):
        		street_types[street_type[0]].add(street_name.title())


def audit_postcode(postcodes, number):
	#checks postcode length and adds anomalous number to set
	if (len(number)!=6):
		postcodes.add(number)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            	elif is_postcode(tag):
            		audit_postcode(postcodes,tag.attrib['v'])

    return (street_types, postcodes)


def update_name(name, mapping):

    m = street_type_re.search(name)
    first = name.split()
    if m:
        street = m.group()
        street_type = street.partition(" ")
        
        # replaces abbreviated English street_types if mapping available
        if (street_type[0] not in expected) and (street_type[0] in mapping.keys()):
            name = re.sub(street_type_re, mapping[street_type[0]], name) + " " + street_type[2]
            
        # replaces abbreviated Malay street_types if mapping available. 
        elif first[0] in mapping.keys():
			name = re.sub(malay_type_re, mapping[first[0]], name)		
		
	return name

def update_postcode(number):

    if (len(number)!=6):
    	if 'Singapore' in number:
    		number = number.lstrip("Singapore")
        elif 'S' in number:
			number = number.lstrip("S")
    
    return number
		

if __name__ == '__main__':
    
    st_types, postcodes = audit(OSMFILE)
    
    #print anomalous postcodes and street types
    print postcodes
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            if better_name != name:
            	print name, "=>", better_name
            	
    for postcode in postcodes:
        postcode_new= update_postcode(postcode)
        if postcode!=postcode_new:
        	print postcode, "=>", postcode_new