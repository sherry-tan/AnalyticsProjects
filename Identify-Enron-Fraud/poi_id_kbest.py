#!/usr/bin/python

import sys
import pickle
import numpy
from feature_format import featureFormat, targetFeatureSplit
from outliers import dataPlot
from tester import dump_classifier_and_data
from evaluate import test_classifier

from sklearn.cross_validation import StratifiedShuffleSplit, train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn import grid_search
from sklearn.metrics import accuracy_score, precision_score, recall_score


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

### Preliminary longlist of features. will be updated as features are added and removed
features_list = ['poi','salary', 'deferral_payments', 'total_payments', 'loan_advances', 
'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 
'director_fees', 'to_messages', 'from_poi_to_this_person', 
'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi'] 

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers

### remove outliers identified from dataPlot.py
data_dict.pop("TOTAL", 0) 

#dataPlot(data_dict, features_list)
delete = ["FREVERT MARK A", "BHATNAGAR SANJAY"]

for key in delete:
	data_dict.pop(key, 0) 


### Task 3: Create new feature(s)

new_feature = ['to_messages_POI', 'from_messages_POI', 'shared_messages_POI']

### calculates messages received from POI or sent to POI as fraction of total messages received or sent for each person
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

### remove outlier identified in dataPlot 
#dataPlot(data_dict, ['poi', 'to_messages_POI', 'from_messages_POI', 'shared_messages_POI'])	
data_dict.pop("HUMPHREY GENE E", 0) 

### update features_list
features_list = features_list + new_feature
toremove = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

for feature in toremove:
	features_list.remove(feature)
	

### Store to my_dataset for easy export below.
my_dataset = data_dict


### Extract features and labels from dataset for local testing. NaN values are set to zero
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or, other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html


### set up pipeline for SVM algorithm
feat_select = SelectKBest(f_classif)
scaler = MinMaxScaler()
svm = SVC()
pipe = Pipeline(steps=[('scaler', scaler), ('feat_select', feat_select),('svm',svm)])


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


### splits data into training and testing set
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)


### implement cross-validation object for gridsearch 
folds = 100
cv = StratifiedShuffleSplit(labels_train, folds, random_state = 17)


"""
### INITIAL TUNING OF PARAMETERS, including selection of features. optimum k found to be 8. 

### set params for gridsearch
params = dict(feat_select__k = range(4, len(features_list)-1), svm__gamma=[0.1, 0.5, 1], 
svm__C=[1,10,100], svm__kernel=['rbf', 'poly', 'sigmoid'])

estimator = grid_search.GridSearchCV(pipe,  param_grid=params, scoring = 'f1', cv=cv)
estimator.fit(features_train, labels_train)
print estimator.best_params_
#pprint.pprint(estimator.grid_scores_)

"""

### identify best k features (k=8) used in POI identifier and save to updated_features list
feat_select.set_params(k=13)
feat_select.fit(features_train, labels_train)
array1 = feat_select.get_support()
array2 = feat_select.scores_

print "Scores for features selected using SelectKBest: "
updated_features = ['poi']
for i in range(0,len(array1)):
	if array1[i]==True:
		print features_list[i+1], array2[i]
		updated_features.append(features_list[i+1])

### store updated_features in features_list for export
features_list = updated_features
print "Features used in classifier: ", features_list


### update features_train and features_test for local testing
features_train = feat_select.transform(features_train)
features_test = feat_select.transform(features_test)

"""
### RETUNE WITH WIDER RANGE OF PARAMETERS USING OPTIMUM K=8 . Optimum C = 70, gamma = 0.5, kernel = 'sigmoid'

### set params for gridsearch
params = dict(svm__gamma=[0.01, 0.1, 0.5, 1.0], 
svm__C= range(10,100,10), svm__kernel=['rbf', 'poly', 'sigmoid', 'linear'])

pipe = Pipeline(steps=[('scaler', scaler),('svm',svm)])
estimator = grid_search.GridSearchCV(pipe,  param_grid=params, scoring = 'f1', cv=cv)
estimator.fit(features_train, labels_train)
print estimator.best_params_

### evaluate performance using the local train/test data and 100-fold stratified shuffle split
pred = estimator.predict(features_test)

print "Accuracy, Precision and Recall calculated using sklearn.metrics and 70/30 data split :"
print accuracy_score(labels_test, pred)
print precision_score(labels_test, pred)
print recall_score(labels_test, pred)

print "Performance using 100-fold stratified shuffle split: "
test_classifier(estimator, my_dataset, features_list)
"""

###  FINAL CLASSIFIER

### set optimized params and construct final classifier
svm.set_params(C=70, kernel='sigmoid', gamma=0.5)
clf = Pipeline(steps=[('scaler', scaler),('svm',svm)])
clf.fit(features_train, labels_train)

### evaluate performance using the local train/test data and 100-fold stratified shuffle split
pred = clf.predict(features_test)

print "Accuracy, Precision and Recall calculated using sklearn.metrics and 70/30 data split :"
print accuracy_score(labels_test, pred)
print precision_score(labels_test, pred)
print recall_score(labels_test, pred)

print "Performance using 100-fold stratified shuffle split: "
test_classifier(clf, my_dataset, features_list)



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

