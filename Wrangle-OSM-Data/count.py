#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Use iterative parsing to process the map file to 
find out what tags are present and how many of each there are. 
"""
import xml.etree.cElementTree as ET
import pprint
file = "small.osm"

def count_tags(filename):
    
    tags = {}
    
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags.keys():
            tags[elem.tag] = tags[elem.tag] + 1
        else:
            tags[elem.tag] = 1
    
    return tags
   

if __name__ == "__main__":
    tags = count_tags(file)
    pprint.pprint(tags)