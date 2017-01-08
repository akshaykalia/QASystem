import os, sys, re, string
from subprocess import *
reload(sys)
sys.setdefaultencoding('utf8')

chunkModel = 'chunk\\chunk-model'
nerModel = 'name\\model-ner'
qTypeModel = 'GetQuestionType\\qtype-model'
solrURL = 'http://localhost:8983/solr/wiki'
clear = lambda: os.system('cls')
def jarWrapper(*args):
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
    ret = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith('\n'):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')
    return ret

cleanr =re.compile(r'(<[^>]+>|{{[^}]+}})')
replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
def remove_tags(text):
    try:
        text = text.encode('utf-8', 'ignore')
    except:
        text = text.encode('utf-8', 'ignore')
        text = text.decode('utf-8', 'ignore')
    return re.sub(cleanr,'', text)

question = sys.argv[1]
'''if question endswith '?':
    question = question
    # check if space before ?
else:
    question = question + ' ?'
'''
clear()
print '*'*40
print question
print '*'*40
fileName = 'output/user-question.txt'
words = question.split()
words.insert(0,'')
words.append('')
words.append('')
full_path = os.path.realpath(__file__)
curDirectory = os.path.dirname(full_path) + '\\'

fout = open(fileName, 'w')
for word in words:
	fout.write(word+"\n")
fout.close()
#run POS tagger
p = Popen([curDirectory + "POS\\HMM_Fast.py", curDirectory + fileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()
posfileName = fileName.split(".")[0] + '.pos'

#run Chunk feature builder 
chunkFeaturesfileName = fileName.split(".")[0] + '.chunk_features'
p = Popen([curDirectory + "Chunk\\feature_builder_chunk.py", curDirectory + posfileName, curDirectory + chunkFeaturesfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

#run Chunk tagger
chunkfileName = fileName.split(".")[0] + '.chunk'
args = [curDirectory + 'jar\\METagger.jar', curDirectory + chunkFeaturesfileName, curDirectory + chunkModel, curDirectory + chunkfileName] # Any number of args to be passed to the jar file
result = jarWrapper(*args)

#Combine POS + Chunk
chunkPOSfileName = fileName.split(".")[0] + '.pos_chunk'
p = Popen([curDirectory + "files-combiner.py", 'True' ,curDirectory + posfileName, curDirectory + chunkfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

#run Name feature builder 
nerFeaturesfileName = fileName.split(".")[0] + '.name_features'
p = Popen([curDirectory + "Name\\feature_builder_ner.py", curDirectory + chunkPOSfileName, curDirectory + nerFeaturesfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

#run Name tagger
nerfileName = fileName.split(".")[0] + '.name'
args = [curDirectory + 'jar\\METagger.jar', curDirectory + nerFeaturesfileName, curDirectory + nerModel, curDirectory + nerfileName] # Any number of args to be passed to the jar file
result = jarWrapper(*args)

#Combine POS + Chunk + Name
nerChunkPOSfileName = fileName.split(".")[0] + '.pos_chunk_name'
p = Popen([curDirectory + "files-combiner.py", 'False' ,curDirectory + posfileName, curDirectory + chunkfileName, curDirectory + nerfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

# run head word + qType
qtypeHeadfileName = fileName.split(".")[0] + '.qtype_test'
p = Popen([curDirectory + "Head\\head_word.py" ,curDirectory + nerChunkPOSfileName, curDirectory + qtypeHeadfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

with open(qtypeHeadfileName) as l:
    result = l.read().splitlines()
    result = filter(None,result)

splittedValues = result[0].split('\t')
headword = splittedValues[4]

# create question type feature
qtypeFeaturefileName = fileName.split(".")[0] + '.feature_test'
p = Popen([curDirectory + "Question-Feature\\question_feature.py" ,curDirectory + qtypeHeadfileName, curDirectory + qtypeFeaturefileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

#run Question Type Tagger
qTypefileName = fileName.split(".")[0] + '.qtype'
args = [curDirectory + 'jar\\METagger.jar', curDirectory + qtypeFeaturefileName, curDirectory + qTypeModel, curDirectory + qTypefileName] # Any number of args to be passed to the jar file
result = jarWrapper(*args)

# Get Maximum count of QuestionType
finalFile = fileName.split(".")[0] + '.final'
p = Popen([curDirectory + "GetQuestionType\\get_qtype.py" ,curDirectory + qTypefileName, curDirectory + finalFile], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

with open(finalFile) as l:
    result = l.read().splitlines()
    qType = result[0]
    print 'Question Classification : ', qType

# query SOLR with question minus stopwords
# SOLR limit can be len(question) * 5

stopWordsFile = curDirectory + 'resources\\stop_words.txt'
with open(stopWordsFile) as f:
    stopwords = f.read().splitlines()

cleanQuestionWords = []
for word in words:
    if word.lower() not in stopwords and word:
        cleanQuestionWords.append(word)

cleanWordsStr = ' '.join(cleanQuestionWords)
from solrq import Q, Proximity
import pysolr

solr = pysolr.Solr(solrURL)

#res = solr.search(cleanWordsStr.replace(' ','+'))
res = solr.search(Q(text=Proximity(cleanWordsStr, 10)))
#print len(res), ' results found'

# Just loop over it to access the results.

fout = open('wiki.result', 'w')

for r in res:
    #print("Reading wiki article : '{0}'.".format(r['title']))
    articleBody = r['text'].replace('[[','').replace(']]','')
    fout.write(remove_tags(articleBody))
    break
fout.close()

log = headword.lower()

cleanedLinesWithHead = [ line.replace('[[','').replace(']]','') for line in open('wiki.result') if headword.lower() in line.lower() and not line.startswith("===") and len(line) > 50 and not line.startswith("*") and "|thumb|" not in line]
cleanLinesCombined = '.'.join(cleanedLinesWithHead)
cleanLines = cleanLinesCombined.split('.')
cleanLinesA = [line for line in cleanLines if len(line) > 20 and any(keyword.lower() in line.lower() for keyword in cleanQuestionWords)]
fout = open('wiki-filtered.result','w')
for item in cleanLinesA:
  fout.write("%s\n" % item)

'''
phrases = [x.lower() for x in cleanQuestionWords]
phrases.remove(log.lower())
'''
import nltk
def contains_ner_entity(text,qType):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if type(chunk) == nltk.tree.Tree:
                res = str(chunk)
                if qType == 'HUM' and ('PERSON' in res or 'ORGANIZATION' in res):
                    return True
                if qType == 'LOC' and ('GPE' in res and 'NNP' in res):
                    return True
                #if qType == 'LOC' and ('CD' in res):
                    #return True
    return False

def contains_pos_entity(text,tag):
    for sent in nltk.sent_tokenize(text):
        for pos in nltk.pos_tag(nltk.word_tokenize(sent)):
            return True
    return False

valid = []
with open('wiki-filtered.result') as l:
    lines = l.read().splitlines()
    fout = open('answer.summary', 'w')
    for line in lines:
        if qType in ['LOC','HUM']:
            if contains_ner_entity(line,qType):
                fout.write(line + "\n")
                print(line)
        elif qType == 'NUM':
            if contains_pos_entity(line,'CD'):
                fout.write(line + "\n")
                print(line)
        else:
            fout.write(line + "\n")
        #fout.write("\n")

'''
from summa import summarizer
with open('answer.summary') as l:
    lines = l.read().splitlines()
fout = open('answer.summary', 'w')  
for line in lines:
    try:
        fout.write(summarizer.summarize(line)+"\n")
    except:
        continue
        #fout.write("\n")


# dictionary of question type and answers
qTypeDict = {'HUM':['NNP']}
# tag answers
ansfileName = 'output\\answers.wiki'
fout = open(ansfileName, 'w')
with open('wiki-filtered.result') as l:
    result = l.read().splitlines()
    for r in result:
        words = r.split()
        for word in words:
            fout.write(word+"\n")
        fout.write("\n")

p = Popen([curDirectory + "POS\\HMM_Fast.py", curDirectory + ansfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()
ansPosfileName = ansfileName.split(".")[0] + '.pos'

#run Chunk feature builder 
ansFeaturesfileName = ansfileName.split(".")[0] + '.chunk_features'
p = Popen([curDirectory + "Chunk\\feature_builder_chunk.py", curDirectory + ansPosfileName, curDirectory + ansFeaturesfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

#run Chunk tagger
anschunkfileName = ansfileName.split(".")[0] + '.chunk'
args = [curDirectory + 'jar\\METagger.jar', curDirectory + ansFeaturesfileName, curDirectory + chunkModel, curDirectory + anschunkfileName] # Any number of args to be passed to the jar file
result = jarWrapper(*args)

#Combine POS + Chunk
ansChunkPOSfileName = ansfileName.split(".")[0] + '.pos_chunk'
p = Popen([curDirectory + "files-combiner.py", 'True' ,curDirectory + ansPosfileName, curDirectory + anschunkfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()


#run Name feature builder 
ansNerFeaturesfileName = ansfileName.split(".")[0] + '.name_features'
p = Popen([curDirectory + "Name\\feature_builder_ner.py", curDirectory + ansChunkPOSfileName, curDirectory + ansNerFeaturesfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()

#run Name tagger
ansNerfileName = ansfileName.split(".")[0] + '.name'
args = [curDirectory + 'jar\\METagger.jar', curDirectory + ansNerFeaturesfileName, curDirectory + nerModel, curDirectory + ansNerfileName] # Any number of args to be passed to the jar file
result = jarWrapper(*args)

#Combine POS + Chunk + Name
ansNerChunkPOSfileName = ansfileName.split(".")[0] + '.pos_chunk_name'
p = Popen([curDirectory + "files-combiner.py", 'False' ,curDirectory + ansPosfileName, curDirectory + anschunkfileName, curDirectory + ansNerfileName], shell=True, stdin=PIPE, stdout=PIPE)
output = p.communicate()'''