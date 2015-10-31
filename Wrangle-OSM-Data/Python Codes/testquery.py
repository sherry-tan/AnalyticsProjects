#!/usr/bin/env python
"""
Use an aggregation query to answer the following question. 

What is the most common city name in our cities collection?

Your first attempt probably identified None as the most frequently occurring city name. 
What that actually means is that there are a number of cities without a name field at all. 
It's strange that such documents would exist in this collection and, depending on your situation, 
might actually warrant further cleaning. 

To solve this problem the right way, we should really ignore cities that don't have a name specified. 
As a hint ask yourself what pipeline operator allows us to simply filter input? 
How do we test for the existence of a field?

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation pipeline 
that can be passed to the MongoDB aggregate function. As in our examples in this lesson, 
the aggregation pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. 
If you want to run this code locally on your machine, you have to install MongoDB, 
download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a different version of the cities collection
provided in the course materials. If you attempt some of the same queries that we look at in the 
problem set, your results may be different.
"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    """pipeline = [{'$match':{'amenity':{"$exists":1}}},
                {'$group':{'_id':'$amenity', 'count':{'$sum':1}}},
                {'$sort':{'count':-1}},
                {'$project':{"count":1,'amenity': '$amenity'}},
                {'$limit':10}
                
               ]"""
	#anomalous postcodes detected by audit-data.py
    
    postcodes =['81100', '05901', '29461', '29466', '80300', '80200', '80050','80150', '<different>', '79200', '81750', '80000', '80250', '80400', 
	'Bukit Batok Street 25', '81300', '81310']

   
    
    #queries for entries with anomalous postcodes
    pipeline1 = [{'$match': {'address.postcode':{'$in':postcodes}}},
    			{'$limit': 50}]	
    #queries for count by address.city			
    pipeline2 =  [{'$match': {'address.city':{'$exists':1}}},
    			  {'$group': {'_id':'$address.city', 'count':{'$sum':1}}},
    			  {'$project':{'city':'$address.city', 'count':1}},
    			  {'$sort': {'count':-1}}]	
    #queries for entries with '<different>' in postcode to see what their addresses are   
    pipeline3 = [{'$match': {'address.postcode':'<different>'}},
    			 {'$project': {'street':'$address.street', 'housenumber':'$address.housenumber'}}]
    
    #queries for entries with 'Tuas Avenue 11' in street to see if any have postcodes populated			
    pipeline4 = [{'$match': {'address.street':'Tuas Avenue 11'}},
    			{'$project': {'postcode':'$address.postcode', 'housenumber':'$address.housenumber'}}]	
    				
    #queries for top contributing user			
    pipeline5 = [ {'$group':{'_id':'$created.user', 'count':{'$sum':1}}},
    			{'$sort':{'count':-1}},
    			{'$limit':1}]
    
     #queries for number of users appearing only once		
    pipeline6 = [ {'$group':{'_id':'$created.user', 'count':{'$sum':1}}},
    			{'$group':{'_id':'$count', 'freq':{'$sum':1}}},
    			{'$sort':{'_id':+1}},
    			{'$limit':1}]
    			
    #queries for top 10 appearing amenities			
    pipeline7 = [ {'$match':{'amenity':{'$exists':1}}},
    			{'$group':{'_id':'$amenity', 'count':{'$sum':1}}},
    			{'$sort':{'count':-1}},
    			{'$limit':10}]
    			
    #queries for top 5 fast food 			
    pipeline8 = [ {'$match':{'amenity':'fast_food', 'name':{'$exists':1}}},
    			{'$group':{'_id':'$name', 'count':{'$sum':1}}},
    			{'$sort':{'count':-1}},
    			{'$limit':10}]
    			
    #queries for top 5 religions	
    pipeline9 = [ {'$match':{'amenity':"place_of_worship", 'religion':{'$exists':1}}},
    			{'$group':{'_id':'$religion', 'count':{'$sum':1}}},
    			{'$sort':{'count':-1}},
    			{'$limit':5}]
    			
    #queries for top 5 cafes			
    pipeline10 = [ {'$match':{'amenity':'cafe', 'name':{'$exists':1}}},
    			{'$group':{'_id':'$name', 'count':{'$sum':1}}},
    			{'$sort':{'count':-1}},
    			{'$limit':5}]
    			
    #queries for top 5 cuisines		
    pipeline11 = [ {'$match':{'amenity':'restaurant', 'cuisine':{'$exists':1}}},
    			{'$group':{'_id':'$cuisine', 'count':{'$sum':1}}},
    			{'$sort':{'count':-1}},
    			{'$limit':5}]	
    					
    pipeline12 =[ {'$match':{'amenity':"parking"}},{'$limit':10}]

    return pipeline12

def aggregate(db, pipeline):
    return [doc for doc in db.SG.aggregate(pipeline)]


if __name__ == '__main__':
    # The following statements will be used to test your code by the grader.
    # Any modifications to the code past this point will not be reflected by
    # the Test Run.
    db = get_db('mydb')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result)
   
