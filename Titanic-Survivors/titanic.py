#!/usr/bin/python

import numpy
import csv
import pandas

from sklearn.cross_validation import StratifiedShuffleSplit, train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn import grid_search
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

data = pandas.read_csv('/Users/SherryT/Documents/Projects/Titanic-Survivors/train.csv')
data = data.dropna()
labels = data['Survived']
features_list = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare' ]
features = data[features_list]


bin_embarked = pandas.get_dummies(data['Embarked'], prefix='em')
bin_sex = pandas.get_dummies(data['Sex'], prefix='mf')
features = features.join(bin_embarked)
features = features.join(bin_sex)

print features[0:4]

### set up pipeline for SVM algorithm
#feat_select = SelectKBest(f_classif)
#svm = SVC()
#scaler = MinMaxScaler()
clf = GaussianNB()
#pipe = Pipeline(steps=[('feat_select', feat_select),('NB',NB)])



### splits data into training and testing set
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)




### INITIAL TUNING OF PARAMETERS, including selection of features. optimum k found to be 8. 

### set params for gridsearch
#params = dict(feat_select__k = range(4, len(features_list)))
#, svm__gamma=[0.1, 0.5, 1], 
#svm__C=[1,10,100], svm__kernel=['rbf', 'poly', 'sigmoid', 'linear'])

#estimator = grid_search.GridSearchCV(pipe,  param_grid=params)
#estimator.fit(features_train, labels_train)
#print estimator.best_params_

clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

print "Accuracy, Precision and Recall calculated using sklearn.metrics and 70/30 data split :"
print accuracy_score(labels_test, pred)
print precision_score(labels_test, pred)
print recall_score(labels_test, pred)

"""
### identify best k features (k=8) used in POI identifier and save to updated_features list
feat_select.set_params(k=8)
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

"""