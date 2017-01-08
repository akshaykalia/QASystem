#Author: Aparajita Choudhury
from collections import defaultdict
from decimal import *
import sys
import re
import os

class Feature_Builder():

	def __init__(self, inputFile):
		self.inputf = sys.argv[1]
		
	def prev_curr_next(self, inputf):
		iter_infile = iter(inputf)
		prev_prev_line = ''
		prev_line = ''
		curr_line = iter_infile.next()
		next_line = iter_infile.next()
		for next_next_line in iter_infile:
			yield (prev_prev_line,prev_line,curr_line,next_line,next_next_line)
			prev_prev_line = prev_line
			prev_line = curr_line
			curr_line = next_line
			next_line = next_next_line
		yield (prev_prev_line,prev_line,curr_line,next_line,'')
		
	
	def featurebuild(self, inputf, featurefile):
		outfile = open(featurefile, 'w')
		lines = (line.strip() for line in open(inputf))
		for prev_prev_line,prev_line,curr_line,next_line,next_next_line in self.prev_curr_next(lines):
			
			curr_token = curr_pos = curr_tag = curr_ner = curr_qtype = curr_head = curr_qword = ''
			prev_token = prev_pos = prev_tag = prev_ner = prev_qtype = prev_head = prev_qword = ''
			prev_prev_token = prev_prev_pos = prev_prev_tag = prev_prev_ner = prev_prev_qtype = prev_prev_head = prev_prev_qword = ''
			next_token = next_pos = next_tag = next_ner = next_qtype = next_head = next_qword = ''
			next_next_token = next_next_pos = next_next_tag = next_next_ner = next_next_qtype = next_next_head = next_next_qword = ''
				
			inputf_name, inputf_ext = os.path.splitext(inputf)
			if inputf_ext == '.qtype_train':
				if curr_line:
					curr_token,curr_pos,curr_tag,curr_ner,curr_qtype,curr_head,curr_qword = curr_line.split('\t')
				if prev_line:
					prev_token,prev_pos,prev_tag,prev_ner,prev_qtype,prev_head,prev_qword = prev_line.split('\t')
				if prev_prev_line:
					prev_prev_token,prev_prev_pos,prev_prev_tag,prev_prev_ner,prev_prev_qtype,prev_prev_head,prev_prev_qword = prev_prev_line.split('\t')
				if next_line:
					next_token,next_pos,next_tag,next_ner,next_qtype,next_head,next_qword = next_line.split('\t')
				if next_next_line:
					next_next_token,next_next_pos,next_next_tag,next_next_ner,next_next_qtype,next_next_head,next_next_qword = next_next_line.split('\t')
				
				
				if not curr_line:
					outfile.write('\n')
				else:
					outfile.write(curr_token+'\t'+'prev_prev_token='+prev_prev_token+'\t'+'prev_prev_pos='+prev_prev_pos+'\t'+'prev_prev_tag='+prev_prev_tag+'\t'+'prev_prev_ner='+prev_prev_ner+'\t'+'prev_token='+prev_token+'\t'+'prev_pos='+prev_pos+'\t'+'prev_tag='+prev_tag+'\t'+'prev_ner='+prev_ner+'\t'+'curr_pos='+curr_pos+'\t'+'curr_tag='+curr_tag+'\t'+'curr_ner='+curr_ner+'\t'+'next_token='+next_token+'\t'+'next_pos='+next_pos+'\t'+'next_tag='+next_tag+'\t'+'next_ner='+next_ner+'\t'+'next_next_token='+next_next_token+'\t'+'next_next_pos='+next_next_pos+'\t'+'next_next_tag='+next_next_tag+'\t'+'next_next_ner='+next_next_ner+'\t'+'head='+curr_head+'\t'+'qword='+curr_qword+'\t'+curr_qtype+'\n')

			elif inputf_ext == '.qtype_test':
				if curr_line:
					curr_token,curr_pos,curr_tag,curr_ner,curr_head,curr_qword = curr_line.split('\t')
				if prev_line:
					prev_token,prev_pos,prev_tag,prev_ner,prev_head,prev_qword = prev_line.split('\t')
				if prev_prev_line:
					prev_prev_token,prev_prev_pos,prev_prev_tag,prev_prev_ner,prev_prev_head,prev_prev_qword = prev_prev_line.split('\t')
				if next_line:
					next_token,next_pos,next_tag,next_ner,next_head,next_qword = next_line.split('\t')
				if next_next_line:
					next_next_token,next_next_pos,next_next_tag,next_next_ner,next_next_head,next_next_qword = next_next_line.split('\t')
				
				
				if not curr_line:
					outfile.write('\n')
				else:
					outfile.write(curr_token+'\t'+'prev_prev_token='+prev_prev_token+'\t'+'prev_prev_pos='+prev_prev_pos+'\t'+'prev_prev_tag='+prev_prev_tag+'\t'+'prev_prev_ner='+prev_prev_ner+'\t'+'prev_token='+prev_token+'\t'+'prev_pos='+prev_pos+'\t'+'prev_tag='+prev_tag+'\t'+'prev_ner='+prev_ner+'\t'+'curr_pos='+curr_pos+'\t'+'curr_tag='+curr_tag+'\t'+'curr_ner='+curr_ner+'\t'+'next_token='+next_token+'\t'+'next_pos='+next_pos+'\t'+'next_tag='+next_tag+'\t'+'next_ner='+next_ner+'\t'+'next_next_token='+next_next_token+'\t'+'next_next_pos='+next_next_pos+'\t'+'next_next_tag='+next_next_tag+'\t'+'next_next_ner='+next_next_ner+'\t'+'head='+curr_head+'\t'+'qword='+curr_qword+'\t'+'@@'+'\n')					

featurebuilder = Feature_Builder(sys.argv[1])
featurebuilder.featurebuild(sys.argv[1],sys.argv[2])