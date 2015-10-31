#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


"""
transform OSM data into a list of dictionaries, audit and clean data and saves data as 
JSON. JSON file is then imported to MongoDB for queries.


PROCESSING RULES: 

- Only 2 types of top level tags: "node" and "way" are processed
- all attributes of "node" and "way" are turned into regular key/value pairs, except:
    - attributes in the CREATED array are added under a key "created"
    - attributes for latitude and longitude are added to a "pos" array
- if second level tag "k" value contains problematic characters, it is ignored
- if second level tag "k" value starts with "addr:", it is added to a dictionary "address",
Corresponding key in the "address" dictionary will be given by the text following the ":"
in the "addr:"
- if there is a second ":" that separates the type/direction of a street,
  the tag is ignored, for example, k="addr:housenumber" is processed but  k="addr:street:name" is not
- all other second level tags not starting with "addr:" are processed as regular key/value
 pairs 
- for "way" specifically, second level nd "ref" values are added to a "nodes_ref" array i.e.
"""

file = "singapore.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'(\b\S+\.?$)|(\b\S+\.?\s+\d+$)', re.IGNORECASE)
#checks for strings starting with J or L
malay_type_re = re.compile(r'(^J\S+)|(^L\S+)', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

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
            "Avebue":"Avenue",
            "Cresent":"Crescent"
            }

"""
updates street names for consistency
"""
def update_name(name, mapping):

    m = street_type_re.search(name)
    first = name.split()
    if m:
        street = m.group()
        
        #partitions street_type so that numbered streets can be cleaned as well
        street_type = street.partition(" ")
        
        # replaces abbreviated English street_types if mapping available
        if (street_type[0] not in expected) and (street_type[0] in mapping.keys()):
            name = re.sub(street_type_re, mapping[street_type[0]], name) + " " + street_type[2]
        
        # replaces abbreviated Malay street_types if mapping available. 
        elif first[0] in mapping.keys():
			name = re.sub(malay_type_re, mapping[first[0]], name)
				
		
	return name

"""
removes redundant text from postcodes
"""
	
def update_postcode(number):

    if (len(number)!=6):
    	if 'Singapore' in number:
    		number = number.lstrip("Singapore")
        elif 'S' in number:
			number = number.lstrip("S")
    
    return number
		
"""
processes osm data into list of dictionaries according to processing rules
"""
def shape_element(element):
    node = {}

    
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag
        for attrib in element.attrib:
           if attrib in CREATED:
               if "created" not in node:
                   node["created"]={}
               node["created"][attrib] = element.get(attrib)
           elif  attrib == "lat":
               if "pos" not in node:
                   node["pos"]=[None] * 2
               node["pos"][0] = float(element.get(attrib))    
           elif attrib == "lon":
               if "pos" not in node:
                   node["pos"]=[None] * 2
               node["pos"][1] = float(element.get(attrib))           
           else:
                node[attrib] = element.get(attrib)
        
        for child in element:
            if child.tag == "tag":
                key = child.get('k')
                val = child.get('v')
                if problemchars.search(key):
                    continue
                elif key.startswith("addr:"):
                    if "address" not in node:
                        node["address"] = {}
                    if ':' in key[5:]:
                        continue
                    elif (key == "addr:city") and (val!="Singapore"):
                		continue
                    elif key == "addr:street":
                    	node["address"][key[5:]] = update_name(val, mapping) 
                    elif key == "addr:postcode":
                    	node["address"][key[5:]] = update_postcode(val)
                    else:    
                        node["address"][key[5:]] = val
                else:
                    node[key] = val
            elif child.tag == "nd":  
                if "node_refs" not in node:
                    node["node_refs"] = []
                node["node_refs"].append(child.get("ref"))
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):

    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    

if __name__ == "__main__":
	
	data = process_map(file, False)
	
	n = 0
	

	