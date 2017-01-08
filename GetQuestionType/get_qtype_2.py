import sys, shlex, re
from collections import defaultdict

class get_qtype():
	def __init__(self, inputfile):
		self.inputf = sys.argv[1]
		
	def get_type(self,inputf,qtypefile):
		#qtype = []
		qType = defaultdict(int)
		fout = open(qtypefile, 'w')
		with open(inputf,'r') as infile:
			for line in infile:
				line = line.strip()
				if line[0] == '?':
					if len(qType) > 0:
						result = max(qType.iteritems(), key=lambda x: x[1])
						fout.write(result[0] + '\n')
					qType = defaultdict(int)
				else:
					if line.strip():
						#print line
						res = line.split(',')
						ques = res[-1]
						print ques
						qType[ques] += 1
		# handling for last
		if len(qType) > 0:
			result = max(qType.iteritems(), key=lambda x: x[1])
			fout.write(result[0] + '\n')
		
				
getqtype = get_qtype(sys.argv[1])
getqtype.get_type(sys.argv[1],sys.argv[2])
			