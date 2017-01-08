import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import MaxentClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from sklearn import cross_validation
from nltk import NaiveBayesClassifier as nbc
import sys,json
import numpy
import scipy
import ast, pickle
#import larch.pickle as pickle

skipTraining = True
from nltk.classify import MaxentClassifier
skipCreatingFeatureFile = True

test = [
     (dict(a=1,b=0,c=1)), # unseen
     (dict(a=1,b=0,c=0)), # unseen
     (dict(a=0,b=1,c=1)), # seen 3 times, labels=y,y,x
     (dict(a=0,b=1,c=0)) # seen 1 time, label=x
     ]

def word_feats(list):
	#return dict(map(string, x.split('=')) for x in list)
	list = filter(None, list)
	#return {k:v for k, _, v in (x.partition("=") for x in list) }
	#print list
	result = {}
	try:
		result = {k:v for k,v in (x.split('=',2) for x in list) }
	except:
		print list
	return result

def trainer(inputFile,modelFile):
	extension = inputFile.split(".")[-1]
	
	print 'Reading Model File:'
	classifier = pickle.load(open(modelFile, "rb" ))

	print 'reading test file'
	testFile = inputFile
	with open(testFile) as f:
		test = f.read().splitlines()
		test = filter(None,test)
		test = [ "word=" + x for x in test]
	
	final_test = []
	for ndx, member in enumerate(test):
		features = test[ndx].split('\t')
		features = filter(None, features)
		feat_dict = {}
		try:
			feat_dict = {k:v for k,v in (x.split('=',1) for x in features[:-1]) }
			final_test.append(feat_dict)
		except:
			 print "Unexpected error:", sys.exc_info()[0]	


	for featureset in final_test:
		pdist = classifier.prob_classify(featureset)
		print pdist
		exit()

	'''print ' '*11+''.join(['      test[%s]  ' % i for i in range(len(test))])
	print ' '*11+'     p(x)  p(y)'*len(test)
	print '-'*(11+15*len(test))



	for algorithm, classifier in classifiers.items():
		print '%11s' % algorithm,
		if isinstance(classifier, Exception):
		    print 'Error: %r' % classifier; continue
		for featureset in test:
			pdist = classifier.prob_classify(featureset)
			print '%8.2f%6.2f' % (pdist.prob('x'), pdist.prob('y')),
        print
	'''
	print 'Tagging Complete !'
	#f = open('model.pickle', 'wb')
	#pickle.dump(classifier, f)
	#f.close()
	#classifier.show_most_informative_features(10)


tagFile = sys.argv[1]
modelFile = sys.argv[2]
print 'Training from ' + tagFile
trainer(tagFile,modelFile)
print 'Tag file'