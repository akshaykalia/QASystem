#Author: Aparajita Choudhury
from collections import defaultdict
from decimal import *
import sys
import re
import os

class FeatureBuilder():

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
			
			curr_token = curr_pos = curr_tag = ''
			prev_token = prev_pos = prev_tag = ''
			prev_prev_token = prev_prev_pos = prev_prev_tag = ''
			next_token = next_pos = next_tag = ''
			next_next_token = next_next_pos = next_next_tag = ''
			inputf_name, inputf_ext = os.path.splitext(inputf)
			if inputf_ext == '.pos-chunk':
				if curr_line:
					curr_token,curr_pos,curr_tag = curr_line.split('\t')
				if prev_line:
					prev_token,prev_pos,prev_tag = prev_line.split('\t')
				if prev_prev_line:
					prev_prev_token,prev_prev_pos,prev_prev_tag = prev_prev_line.split('\t')
				if next_line:
					next_token,next_pos,next_tag = next_line.split('\t')
				if next_next_line:
					next_next_token,next_next_pos,next_next_tag = next_next_line.split('\t')
				
				if not curr_line:
					outfile.write('\n')
				else:
					outfile.write(curr_token+'\t'+'prev_prev_token='+prev_prev_token+'\t'+'prev_prev_pos='+prev_prev_pos+'\t'+'prev_prev_tag='+prev_prev_tag+'\t'+'prev_prev_token_len='+str(len(prev_prev_token))+'\t'+'prev_token='+prev_token+'\t'+'prev_pos='+prev_pos+'\t'+'prev_tag='+prev_tag+'\t'+'prev_token_len='+str(len(prev_token))+'\t'+'curr_token='+curr_token+'\t'+'curr_pos='+curr_pos+'\t'+'curr_token_cap='+str(curr_token[0].isupper())+'\t'+'curr_token_len='+str(len(curr_token))+'\t'+'next_token='+next_token+'\t'+'next_pos='+next_pos+'\t'+'next_token_len='+str(len(next_token))+'\t'+'next_next_token='+next_next_token+'\t'+'next_next_pos='+next_next_pos+'\t'+'next_next_token_len='+str(len(next_next_token))+'\t'+'p_c_token='+prev_token+'|'+curr_token+'\t'+'c_n_token='+curr_token+'|'+next_token+'\t'+'pp_p_pos='+prev_prev_pos+'|'+prev_pos+'\t'+'p_c_pos='+prev_pos+'|'+curr_pos+'\t'+'c_n_pos='+curr_pos+'|'+next_pos+'\t'+'n_nn_pos='+next_pos+'|'+next_next_pos+'\t'+'pp_p_c_pos='+prev_prev_pos+'|'+prev_pos+'|'+curr_pos+'\t'+'p_c_n_pos='+prev_pos+'|'+curr_pos+'|'+next_pos+'\t'+'c_n_nn_pos='+curr_pos+'|'+next_pos+'|'+next_next_pos+'\t'+curr_tag+'\n')
				
			elif inputf_ext == '.pos':
				if curr_line:
					curr_token,curr_pos = curr_line.split('\t')
				if prev_line:
					prev_token,prev_pos = prev_line.split('\t')
				if prev_prev_line:
					prev_prev_token,prev_prev_pos = prev_prev_line.split('\t')
				if next_line:
					next_token,next_pos = next_line.split('\t')
				if next_next_line:
					next_next_token,next_next_pos = next_next_line.split('\t')
					
				if not curr_line:
					outfile.write('\n')
				else:
					outfile.write(curr_token+'\t'+'prev_prev_token='+prev_prev_token+'\t'+'prev_prev_pos='+prev_prev_pos+'\t'+'prev_prev_tag='+'@@'+'\t'+'prev_prev_token_len='+str(len(prev_prev_token))+'\t'+'prev_token='+prev_token+'\t'+'prev_pos='+prev_pos+'\t'+'prev_tag='+'@@'+'\t'+'prev_token_len='+str(len(prev_token))+'\t'+'curr_token='+curr_token+'\t'+'curr_pos='+curr_pos+'\t'+'curr_token_cap='+str(curr_token[0].isupper())+'\t'+'curr_token_len='+str(len(curr_token))+'\t'+'next_token='+next_token+'\t'+'next_pos='+next_pos+'\t'+'next_token_len='+str(len(next_token))+'\t'+'next_next_token='+next_next_token+'\t'+'next_next_pos='+next_next_pos+'\t'+'next_next_token_len='+str(len(next_next_token))+'\t'+'p_c_token='+prev_token+'|'+curr_token+'\t'+'c_n_token='+curr_token+'|'+next_token+'\t'+'pp_p_pos='+prev_prev_pos+'|'+prev_pos+'\t'+'p_c_pos='+prev_pos+'|'+curr_pos+'\t'+'c_n_pos='+curr_pos+'|'+next_pos+'\t'+'n_nn_pos='+next_pos+'|'+next_next_pos+'\t'+'pp_p_c_pos='+prev_prev_pos+'|'+prev_pos+'|'+curr_pos+'\t'+'p_c_n_pos='+prev_pos+'|'+curr_pos+'|'+next_pos+'\t'+'c_n_nn_pos='+curr_pos+'|'+next_pos+'|'+next_next_pos+'\t'+'@@'+'\n')
				
		outfile.write('\n')
				
				
				
featurebuilder = FeatureBuilder(sys.argv[1])
featurebuilder.featurebuild(sys.argv[1],sys.argv[2])
