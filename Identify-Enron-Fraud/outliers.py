#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot as plt
import pprint

def dataPlot(data_dict, features_list):

	### quick and dirty check for outliers for each feature
	for feature in features_list[1:len(features_list)]:
		entry = []
		poi = []
		max = 0
		max_index = 0
		min = 0
		min_index = 0
		i = 0
	
	### generate list of values for each feature and finds max and min value
		for key in data_dict.keys():
			entry.append(data_dict[key][feature])
			if data_dict[key][feature]!= "NaN":
				if data_dict[key][feature] > max:
					max = data_dict[key][feature]
					max_index = i	
				elif data_dict[key][feature] < min:
					min = data_dict[key][feature]
					min_index = i	
		
			i += 1
			poi.append(data_dict[key]['poi'])
	
	### plot data points for each feature, ignore "NaN" values and differentiate poi/nonpoi
		for j in range(0, len(data_dict)):
			if entry[j] != "NaN":
				if poi[j] == 1:
					plt.scatter(j, entry[j], color = 'r')
				else:
					plt.scatter(j, entry[j], color = 'b')
			
		plt.xlabel('entry_no.')
		plt.ylabel(feature)
		plt.text(max_index,max,"%d, %s" %(max, data_dict.keys()[max_index]))
		if min != 0:
			plt.text(min_index,min,"%d, %s" %(min, data_dict.keys()[min_index]))
		plt.grid('on')
		plt.savefig(feature)
		plt.show()

def checkNaN(data_dict, features_list):
	
	check_nan =[]
	###  checks whether pois are less likely to have NaN values for features compared to non-pois
	for feature in features_list:
		val_poi = 0
		val_notpoi = 0
		for key in data_dict.keys():
			if data_dict[key]['poi']==1:
				if data_dict[key][feature]!="NaN":
					val_poi+=1
			else:
				if data_dict[key][feature]!="NaN":
					val_notpoi+=1	
		
		entry = {'feature': feature, 'val_poi': val_poi,'val_notpoi' : val_notpoi, 'fract': float(val_poi)/float(val_notpoi)}
		check_nan.append(entry)
	
	pprint.pprint(check_nan)


if __name__ == "__main__":

	
	features_list = ['poi','salary', 'deferral_payments', 'total_payments', 'loan_advances', 
	'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 
	'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 
	'restricted_stock', 'director_fees','to_messages', 'from_poi_to_this_person', 
	'from_messages', 'from_this_person_to_poi',  
	'shared_receipt_with_poi']

	### Load the dictionary containing the dataset
	with open("final_project_dataset.pkl", "r") as data_file:
		data_dict = pickle.load(data_file)
	
	data_dict.pop('TOTAL')
	
	new_feature = ['to_messages_POI', 'from_messages_POI', 'shared_messages_POI']
	for key in data_dict.keys():
		data_dict[key]['to_messages_POI'] = "NaN"
		data_dict[key]['from_messages_POI'] = "NaN"
		data_dict[key]['shared_messages_POI'] = "NaN"

		if data_dict[key]['to_messages']>0 and data_dict[key]['to_messages']!="NaN":
			data_dict[key]['to_messages_POI'] = float(data_dict[key]['from_poi_to_this_person'])/float(data_dict[key]['to_messages'])
		
		if data_dict[key]['from_messages']>0 and data_dict[key]['from_this_person_to_poi']!="NaN":
			data_dict[key]['from_messages_POI'] = float(data_dict[key]['from_this_person_to_poi'])/float(data_dict[key]['from_messages'])
	
		if data_dict[key]['to_messages']>0 and data_dict[key]['shared_receipt_with_poi']!="NaN":
			data_dict[key]['shared_messages_POI'] = float(data_dict[key]['shared_receipt_with_poi'])/float(data_dict[key]['to_messages'])

	features_list = features_list + new_feature
	toremove = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

	for feature in toremove:
		features_list.remove(feature)
	
	dataPlot(data_dict, features_list)
	checkNaN(data_dict, features_list)
			