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

Structure will be as follows:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

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
  the tag is ignored, for example:
  
	<tag k="addr:housenumber" v="5158"/>
	<tag k="addr:street" v="North Lincoln Avenue"/>
	<tag k="addr:street:name" v="Lincoln"/>
	<tag k="addr:street:prefix" v="North"/>
	<tag k="addr:street:type" v="Avenue"/>
	<tag k="amenity" v="pharmacy"/>

    is turned into:

	{...
	"address": {
 	   "housenumber": 5158,
 	   "street": "North Lincoln Avenue"
	}
	"amenity": "pharmacy",
	...
	}
	
- all other second level tags not starting with "addr:" are processed as regular key/value
 pairs 
- for "way" specifically, second level nd "ref" values are added to a "nodes_ref" array i.e.

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

is turned into
"node_refs": ["305896090", "1719825889"]
"""

file = "small.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


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
                    else:
                        key = key[5:]
                        node["address"][key] = val
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
	
	pprint.pprint(data[:-5])
	