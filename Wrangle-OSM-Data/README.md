This project uses Singapore map data from OpenStreetMap (https://www.openstreetmap.org),
audits the data for quality, transforms the original XML file into a list of dictionaries
and saves it as JSON. The resulting JSON file is then imported to MongoDB to facilitate
querying to glean insights from the data. 

This project is part of the Udacity Data Analyst Nanodegree.

NOTE: Work in Progress. Small subset of Singapore data (small.osm/small.json)
first used as test case to identify inconsistencies for subsequent cleaning of full data 
set.