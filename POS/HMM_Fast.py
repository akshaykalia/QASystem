# Author : Akshay Kalia
from collections import defaultdict
import sys
import re, os
import profile

#Files
trainingFile = 'WSJ_02-21.pos'
testFile = 'WSJ_23.words'
saveFileName = 'WSJ_23.pos'
full_path = os.path.realpath(__file__)
curDirectory = os.path.dirname(full_path) + '\\'
wordModelFileName = curDirectory + 'model/HMM-pos.words'
transModelFileName = curDirectory +'model/HMM-pos.trans'
emisModelFileName = curDirectory + 'model/HMM-pos.emis'
tmcModelFileName = curDirectory + 'model/HMM-pos.transMapCount'
emcModelFileName = curDirectory + 'model/HMM-pos-words.emisMapCount'

#global variables
words = defaultdict(int)
emissionMap = defaultdict(int)
emissionMapCount = defaultdict(int)
transitionMap = defaultdict(int)
transitionMapCount = defaultdict(int)
TotalWords=0
skipTraining = True
skipTagging = False

def predictUnknownTags(word):
    if not re.search(r'\w',word):
        return ':'
    elif re.search(r'[A-Z]',word):
        return '<CAP>'
    elif re.search(r'\d',word):
        return '<DIGITS>'
    elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)',word):
        return '<VERB>'
    elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)',word):
        return '<NN>'
    elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)',word):
        return '<JJ>'
    else:
        return '<OTHER>'

def CleanWordCount(wc):
    temp = defaultdict(int)
    for (tag,word) in wc:
        temp[(tag,word)] = wc[(tag,word)]
        if wc[(tag,word)] < 5:
            temp[(tag,predictUnknownTags(word))] += wc[(tag,word)]
    return temp

def trainer():
	prev = "START"
	global TotalWords
	global emissionMap
	global words
    #Calculate the word count
	for l in open(trainingFile, 'r'):
		l = l.strip()
		if not l:
			prev = "START"
		else:
			line = l.replace(' ', '\t')
			splitted = line.split('\t')
			w = splitted[0]
			pos = splitted[1]
			TotalWords += 1
			emissionMap[(pos,w)] += 1
			emissionMapCount[pos] += 1
			transitionMap[(prev,pos)] += 1
			transitionMapCount[prev] += 1
			prev = pos
	words = set([key[1] for key in emissionMap.keys()])
	emissionMap = CleanWordCount(emissionMap)
	words = set([key[1] for key in emissionMap.keys()])
    #emissionMap = CleanWordCount(emissionMap)
	print 'Saving Model File...'
	fout = open(wordModelFileName, 'w')
	for k in words:
		fout.write("%s\n" % (str(TotalWords)))
		fout.write("%s\n" % (str(k)))
	fout.close()
	fout = open(emisModelFileName, 'w')
	for k,v in emissionMap.iteritems():
		fout.write("%s\t%s\n" % (str(k), str(v)))
	fout.close()
	fout = open(emcModelFileName, 'w')
	for k,v in emissionMapCount.iteritems():
		fout.write("%s\t%s\n" % (str(k), str(v)))
	fout.close()
	fout = open(transModelFileName, 'w')
	for k,v in transitionMap.iteritems():
		fout.write("%s\t%s\n" % (str(k), str(v)))
	fout.close()
	fout = open(tmcModelFileName, 'w')
	for k,v in transitionMapCount.iteritems():
		fout.write("%s\t%s\n" % (str(k), str(v)))
	print 'Model Files Generated !'

	#print len(words), len(emissionMap), len(emissionMapCount), len(transitionMap),len(transitionMapCount)

def GetWord(sentence,index):
    if index < 0:
        return ''
    else:
        return sentence[index]

def getEmissionProbab(word,state):
	Ecount = emissionMap[(state,word)]
	if(Ecount == 0):
		#word = predictUnknownTags(word)
		#Ecount = emissionMap[(state,word)]
		#if (Ecount == 0):
		return float(1) / TotalWords

		'''if (word.matches("[A-Z]+") and word.lower().endswith("s") and state =="NNPS"):
			 return (1 / TotalWords)+0.001
		if (word.matches("[A-Z]+") and state =="NNP"):
			return (1 / TotalWords)+0.001
		if (Pattern.compile("^[A-Z]").matcher(word).find() and word.lower().endswith("s") and state =="NNPS"):
			 return (1 / TotalWords)+0.0001
		if ((Pattern.compile("^[A-Z]").matcher(word).find()) and state =="NNP"):
			return (1 / TotalWords)+0.0001
		if (Pattern.compile("^.*[0-9].*").matcher(word).find() and state =="CD"):
			return (1 / TotalWords)+0.1
		'''
		if (word.lower().endswith("s") and (state =="NNS") or state =="VBZ"):
			return (1 / TotalWords)+0.00001
		if (word.lower().endswith("ed") and (state =="VBN")):
			return (1 / TotalWords)+0.001
		if (word.lower().endswith("ly") and state =="RB"):
			return (1 / TotalWords)+0.001
		
		if ((word.lower().endswith("able") or word.lower().endswith("al") or word.contains("-")) and state =="JJ"):
			return (1 / TotalWords)+0.0001
		if (word.lower().endswith("ion") and state =="NN"):
			return (1 / TotalWords)+0.0001
		if (word.lower().endswith("ing") and state =="VBG"):
			return (1 / TotalWords)+0.0001
		
		
		
	
	EcountT = emissionMapCount[state]
	
	if(EcountT == 0):
		return float(1) / TotalWords
	
	return float(Ecount) / EcountT
	
def getTransitionProbab(prev,curr):
	Tcount = transitionMap[(prev,curr)]
			
	if(Tcount == 0):
		return float(1) / TotalWords
	
	TcountT = transitionMapCount[prev]
	
	if(TcountT == 0):
		return float(1) / TotalWords;
		
	return float(Tcount) / TcountT

def viterbi(sentence):
	PosMap = {}
	index = 0
	path = []
	for prev, pos in transitionMapCount.items():
		PosMap[index] =  prev
		index += 1

	states = len(PosMap)
	wordCount = len(sentence)
	
	viterbiTable = defaultdict(float)
	StateTable = defaultdict(int)
	
	for i in xrange(0,states):
		if(PosMap.get(i)=="START"):
			viterbiTable[(i,0)] = float(1)
			StateTable[(i,0)] = -1
		else:
			viterbiTable[(i,0)] = float(0)

	'''for k in range(1,len(sentence)+1):
		word = GetWord(sentence,k-1)
		if word not in words:
			word = predictUnknownTags(word)'''

	for i in range(1,wordCount+1):
		if(i%8==0):
			for j in xrange(0,states):
				viterbiTable[(j,i-1)] *=1000000000;
				
		currWord = sentence[i-1]
		if currWord not in words:
			currWord = predictUnknownTags(currWord)
		for currState in xrange(0,states):
			currStateName = PosMap[currState]
						
			if(currStateName == "START"):
				viterbiTable[(currState,i)] = 0
				continue;
			
			currEmisProbab = getEmissionProbab(currWord,currStateName)
			maxV = -999
			prevMaxState = -1
			for prevState in xrange(0,states):				
				prevStateName = PosMap[prevState]
				transProbab = getTransitionProbab(prevStateName,currStateName)
												
				if(float(maxV) < (float(transProbab) * viterbiTable[(prevState,i-1)])):
					maxV = (float(transProbab) * viterbiTable[(prevState,i-1)])
					prevMaxState = prevState

			viterbiTable[(currState,i)] = maxV * currEmisProbab
			StateTable[(currState,i)] = prevMaxState
	currS = 0;
	for i in xrange(0,states):
		if (viterbiTable[(i,wordCount)]>viterbiTable[(currS,wordCount)]):
			currS = i
	path.append(PosMap[currS])
	#print PosMap[currS]
	for i in reversed(range(1,wordCount + 1)):
		path.append(PosMap[StateTable[(currS,i)]])
		currS = StateTable[(currS,i)]

	return list(reversed(path))

#end temp

def tagger():
	global TotalWords,words,emissionMap,emissionMapCount,transitionMap,transitionMapCount
	if skipTraining:
		from collections import defaultdict
		print 'Reading Model Files'
		print 'Creating Word Dictionary...........',
		with open(wordModelFileName) as l:
			word = l.read().splitlines()
		TotalWords = int(word[0])
		word = word[1:]
		words = set(word)

		emissionMap = defaultdict(int)
		emissionMapCount = defaultdict(int)
		transitionMap = defaultdict(int)
		transitionMapCount = defaultdict(int)

		print 'Done'
		print 'Creating Emission Dictionary.......',
		with open(emisModelFileName) as l:
			emis = l.read().splitlines()
			emissionMap = {eval(k):int(v) for k,v in (x.split('\t') for x in emis) }
			emissionMap = defaultdict(int,emissionMap)
		with open(emcModelFileName) as l:
			emc = l.read().splitlines()
			emissionMapCount = {k:int(v) for k,v in (x.split('\t') for x in emc) }
			emissionMapCount = defaultdict(int,emissionMapCount)
		print 'Done'
		print 'Creating Transmission Dictionary...',
		with open(transModelFileName) as l:
			tran = l.read().splitlines()
			transitionMap = {eval(k):int(v) for k,v in (x.split('\t') for x in tran) }
			transitionMap = defaultdict(int,transitionMap)
		with open(tmcModelFileName) as l:
			tmc = l.read().splitlines()
			transitionMapCount = {k:int(v) for k,v in (x.split('\t') for x in tmc) }
			transitionMapCount = defaultdict(int,transitionMapCount)
		print 'Done'
	print 'Tagging...'
	saveFileName = testFile.split(".")[0] + '.pos'
	fout = open(saveFileName, 'w')
	sentence = []
	keyFile = open(testFile, 'r')
	noOfLines = len(keyFile.readlines())
	keyFile.close()
	currentLine = 1
	fout.write('\n')
	for l in open(testFile, 'r'):

		l = l.strip()
		if not l:
			if sentence:
				#sys.stderr.write("Sentence " + str(currentLine)+ "/" + str(noOfLines) + " : " +str(sentence)+'\n')
				path = viterbi(sentence)
				#print path
				for i in range(len(sentence)):
				    fout.write(sentence[i]+'\t'+path[i+1]+'\n')
				sentence = []
				fout.write('\n')
		else:
			sentence.append(l)
		currentLine += 1
	fout.close()

if not skipTraining:
	print 'Training from ' + trainingFile        
	trainer()
	#profile.run('trainer()')
	print 'Completed Training'
if not skipTagging:
	testFile = sys.argv[1]
	print 'Tagging file ' + testFile
	tagger()
	print 'File tagged completely'
#profile.run('tagger()')