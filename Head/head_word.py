#Author: Aparajita Choudhury
from collections import defaultdict
from decimal import *
import sys
import re
import os

class Head_Word():

	def __init__(self, inputFile):
		self.inputf = sys.argv[1]
		
	def get_sentence(self, inputf, headfile):
		token = []
		pos = []
		tag = []
		ner = []
		qtype = []
		inputf_name, inputf_ext = os.path.splitext(inputf)
		with open(inputf, 'r') as infile:
			for line in infile:
				if not line:
					if inputf_ext == '.pos_chunk_name_qtype':
						token.append('')
						pos.append('')
						tag.append('')
						ner.append('')
						qtype.append('')
					else:
						token.append('')
						pos.append('')
						tag.append('')
						ner.append('')
					continue
				else:
					#print line.strip()
					if inputf_ext == '.pos_chunk_name_qtype':
						if line.strip():
							curr_token,curr_pos,curr_tag,curr_ner,curr_qtype = line.strip().split('\t')
							token.append(curr_token)
							pos.append(curr_pos)
							tag.append(curr_tag)
							ner.append(curr_ner)
							qtype.append(curr_qtype)
						else:
							token.append('')
							pos.append('')
							tag.append('')
							ner.append('')
							qtype.append('')

					elif inputf_ext == '.pos_chunk_name':
						if line.strip():
							curr_token,curr_pos,curr_tag,curr_ner = line.strip().split('\t')
							token.append(curr_token)
							pos.append(curr_pos)
							tag.append(curr_tag)
							ner.append(curr_ner)
						else:
							token.append('')
							pos.append('')
							tag.append('')
							ner.append('')

		#print len(token),len(pos),len(tag),len(ner), len(qtype)
		check_nn = re.compile("NN")
		found_nn = False
		found_b = False
		head_word = []
		ques_word = []
		#ques_word.append('')
		#head = ''
		#qword = ''
		for i in xrange(0,len(pos)-1):
			if check_nn.match(pos[i]) and found_nn==False:
				found_nn = True
				head = token[i]
				head_word.append(head)
			if pos[i] == '':
				found_b = True
				found_nn = False
				head = ''
				qword = token[i+1]
				ques_word.append(token[i])
				ques_word.append(qword)

			if pos[i] != '':
				head_word.append(head)
			if pos[i] != '' and pos[i+1] != '':
				ques_word.append(qword)
			if pos[i+1] == '' and found_nn==False:
				head_word.append('')

		first = True
		for i in xrange(len(head_word)-2,0,-1):
			if head_word[i] == '' and first == True:
				word = head_word[i+1]
				first = False
			if head_word[i] == '' and head_word[i-1] == '':
				head_word[i] = word
			if head_word[i] == '' and head_word[i-1] != '':
				first = True

		ques_word.append('')
		head_word.append('')
		#print len(token),len(pos),len(tag),len(ner), len(ques_word), len(head_word)
		outfile = open(headfile, 'w')
		for i in xrange(0,len(token)-1):
			if pos[i] == '':
				outfile.write('\n')
				#print '\n'
			else:
				if inputf_ext == '.pos_chunk_name_qtype':
					outfile.write(token[i] + '\t' + pos[i] + '\t' + tag[i] + '\t' + ner[i] + '\t' + qtype[i] + '\t' + head_word[i] + '\t' + ques_word[i] + '\n')
					#print token[i] + '\t' + pos[i] + '\t' + tag[i] + '\t' + ner[i] + '\t' + qtype[i] + '\t' + head_word[i] + '\t' + ques_word[i] + '\n'
				elif inputf_ext == '.pos_chunk_name':
					outfile.write(token[i] + '\t' + pos[i] + '\t' + tag[i] + '\t' + ner[i] + '\t' + head_word[i] + '\t' + ques_word[i] + '\n')
					#print token[i] + '\t' + pos[i] + '\t' + tag[i] + '\t' + ner[i] + '\t' + head_word[i] + '\t' + ques_word[i] + '\n'
		outfile.write('\n')
		#print '\n'
					
headword = Head_Word(sys.argv[1])
headword.get_sentence(sys.argv[1], sys.argv[2])
print 'Done!'
				