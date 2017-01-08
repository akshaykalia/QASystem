import sys, getopt



nerFile = 'testset_vect.name'
chunkFile = 'testset_vect.chunk'
posFile = 'testset_vect.pos'
fileName = 'testset_vect.pos_chunk'

skipNER = 'False'

skipNER = sys.argv[1]
posFile = sys.argv[2]
chunkFile = sys.argv[3]
if len(sys.argv) > 4:
	nerFile = sys.argv[4]
fileName = posFile.split(".")[0] + '.pos_chunk'
with open(posFile) as l:
	pos = l.read().splitlines()
	#pos = [i.split('\t', 1) for i in lines]

with open(chunkFile) as l:
	lines = l.read().splitlines()
	chunk = [i.split('\t', 1) for i in lines]

ner = []
if skipNER == 'False':
	fileName = fileName + '_name'
	with open(nerFile) as l:
		lines = l.read().splitlines()
		ner = [i.split('\t', 1) for i in lines]

fout = open(fileName, 'w')
for i in xrange(0,len(chunk)):
	chunkValue = ''
	if chunk[i][0]:
		chunkValue = chunk[i][1]
	fout.write("%s\t%s" % (pos[i], chunkValue))
	if skipNER == 'False':
		nerValue = ''
		if ner[i][0]:
			nerValue = ner[i][1]
		fout.write("\t%s" % nerValue)
	fout.write("\n")

print 'Done !'