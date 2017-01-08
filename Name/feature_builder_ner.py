from collections import defaultdict
from decimal import *
import sys
import re
import os

full_path = os.path.realpath(__file__)
curDirectory = os.path.dirname(full_path) + '\\'

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
	
	def is_number(self, str):
		try:
			float(str)
			return True
		except ValueError:
			pass
		return False
	
	def is_punctuation(self, str):
		return not any(c.isalnum() for c in str)
			
	def featurebuild(self, inputf, featurefile):
		names_list = open(curDirectory + "names_list.txt").readlines()
		names_list = [name.strip().lower() for name in names_list]
		countries_list = open(curDirectory + "countries_list.txt").readlines()
		countries_list = [country.strip().lower() for country in countries_list]
		locations_list = open(curDirectory + "locations_list.txt").readlines()
		locations_list = [location.strip().lower() for location in locations_list]
		misc_list = open(curDirectory + "misc_list.txt").readlines()
		misc_list = [misc.strip().lower() for misc in misc_list]
		org_list = open(curDirectory + "org_list.txt").readlines()
		org_list = [org.strip().lower() for org in org_list]
		persons_list = open(curDirectory + "persons_list.txt").readlines()
		persons_list = [person.strip().lower() for person in persons_list]		
		outfile = open(featurefile, 'w')
		lines = (line.strip() for line in open(inputf))
		for prev_prev_line,prev_line,curr_line,next_line,next_next_line in self.prev_curr_next(lines):
			
			curr_token = curr_pos = curr_tag = curr_name = ''
			prev_token = prev_pos = prev_tag = prev_name = ''
			prev_prev_token = prev_prev_pos = prev_prev_tag = prev_prev_name = ''
			next_token = next_pos = next_tag = next_name = ''
			next_next_token = next_next_pos = next_next_tag = next_next_name = ''
			inputf_name, inputf_ext = os.path.splitext(inputf)
			if inputf_ext == '.pos_chunk_name':
				if curr_line:
					curr_token,curr_pos,curr_tag,curr_name = curr_line.split('\t')
				if prev_line:
					prev_token,prev_pos,prev_tag,prev_name = prev_line.split('\t')
				if prev_prev_line:
					prev_prev_token,prev_prev_pos,prev_prev_tag,prev_prev_name = prev_prev_line.split('\t')
				if next_line:
					next_token,next_pos,next_tag,next_name = next_line.split('\t')
				if next_next_line:
					next_next_token,next_next_pos,next_next_tag,next_next_name = next_next_line.split('\t')
				
				if not curr_line:
					outfile.write('\n')
				else:
					outfile.write(curr_token+'\t'+'prev_prev_token='+prev_prev_token+'\t'+'prev_prev_name='+prev_prev_name+'\t'+'prev_token='+prev_token+'\t'+'prev_name='+prev_name+'\t'+'curr_token='+curr_token+'\t'+'next_token='+next_token+'\t'+'next_next_token='+next_next_token+'\t'+'p_name_c_token='+prev_name+'|'+curr_token+'\t'+'p_token_c_token='+prev_token+'|'+curr_token+'\t'+'c_token_n_token='+curr_token+'|'+next_token+'\t'+'pp_token_p_token='+prev_prev_token+'|'+prev_token+'\t'+'n_token_nn_token='+next_token+'|'+next_next_token+'\t'+'pp_token_p_token_c_token='+prev_prev_token+'|'+prev_token+'|'+curr_token+'\t'+'p_token_c_token_n_token='+prev_token+'|'+curr_token+'|'+next_token+'\t'+
'pp_token_cap='+str(prev_prev_token[0].isupper() if prev_prev_token!='' else '')+'\t'+
'p_token_cap='+str(prev_token[0].isupper() if prev_token!='' else '')+'\t'+
'c_token_cap='+str(curr_token[0].isupper())+'\t'+
'n_token_cap='+str(next_token[0].isupper() if next_token!='' else '')+'\t'+
'nn_token_cap='+str(next_next_token[0].isupper() if next_next_token!='' else '')+'\t'+
'c_isallcaps='+str(True if curr_token.isupper() else False)+'\t'+
'c_odigit='+str(True if curr_token.isdigit() else False)+'\t'+
'c_isnumeric='+str(self.is_number(curr_token))+'\t'+
'c_alphahdigit='+str(True if re.match("^[A-Za-z0-9-]*$",curr_token) else False)+'\t'+
'c_haspunct='+str(True if not curr_token.isalnum() else False)+'\t'+
'c_ispunct='+str(self.is_punctuation(curr_token))+'\t'+
'c_prel3='+curr_token[:3]+'\t'+
'c_prel4='+curr_token[:4]+'\t'+
'c_sufl1='+curr_token[-1:]+'\t'+
'c_sufl2='+curr_token[-2:]+'\t'+
'c_sufl3='+curr_token[-3:]+'\t'+
'c_sufl4='+curr_token[-4:]+'\t'+
'prev_prev_pos='+prev_prev_pos+'\t'+
'prev_pos='+prev_pos+'\t'+
'curr_pos='+curr_pos+'\t'+
'next_pos='+next_pos+'\t'+
'next_next_pos='+next_next_pos+'\t'+
'curr_tag='+curr_tag+'\t'+
'c_person_check='+str(True if persons_list.__contains__(curr_token.lower()) else False)+'\t'+
'c_loctn_check='+str(True if locations_list.__contains__(curr_token.lower()) else False)+'\t'+
'c_org_check='+str(True if org_list.__contains__(curr_token.lower()) else False)+'\t'+
'c_misc_check='+str(True if misc_list.__contains__(curr_token.lower()) else False)+'\t'+
curr_name+'\n')				
					
				
			elif inputf_ext == '.pos_chunk':
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
					outfile.write(curr_token+'\t'+'prev_prev_token='+prev_prev_token+'\t'+'prev_prev_name='+'@@'+'\t'+'prev_token='+prev_token+'\t'+'prev_name='+'@@'+'\t'+'curr_token='+curr_token+'\t'+'next_token='+next_token+'\t'+'next_next_token='+next_next_token+'\t'+'p_name_c_token='+'@@'+'|'+curr_token+'\t'+'p_token_c_token='+prev_token+'|'+curr_token+'\t'+'c_token_n_token='+curr_token+'|'+next_token+'\t'+'pp_token_p_token='+prev_prev_token+'|'+prev_token+'\t'+'n_token_nn_token='+next_token+'|'+next_next_token+'\t'+'pp_token_p_token_c_token='+prev_prev_token+'|'+prev_token+'|'+curr_token+'\t'+'p_token_c_token_n_token='+prev_token+'|'+curr_token+'|'+next_token+'\t'+
'pp_token_cap='+str(prev_prev_token[0].isupper() if prev_prev_token!='' else '')+'\t'+
'p_token_cap='+str(prev_token[0].isupper() if prev_token!='' else '')+'\t'+
'c_token_cap='+str(curr_token[0].isupper())+'\t'+
'n_token_cap='+str(next_token[0].isupper() if next_token!='' else '')+'\t'+
'nn_token_cap='+str(next_next_token[0].isupper() if next_next_token!='' else '')+'\t'+
'c_isallcaps='+str(True if curr_token.isupper() else False)+'\t'+
'c_odigit='+str(True if curr_token.isdigit() else False)+'\t'+
'c_isnumeric='+str(self.is_number(curr_token))+'\t'+
'c_alphahdigit='+str(True if re.match("^[A-Za-z0-9-]*$",curr_token) else False)+'\t'+
'c_haspunct='+str(True if not curr_token.isalnum() else False)+'\t'+
'c_ispunct='+str(self.is_punctuation(curr_token))+'\t'+
'c_prel3='+curr_token[:3]+'\t'+
'c_prel4='+curr_token[:4]+'\t'+
'c_sufl1='+curr_token[-1:]+'\t'+
'c_sufl2='+curr_token[-2:]+'\t'+
'c_sufl3='+curr_token[-3:]+'\t'+
'c_sufl4='+curr_token[-4:]+'\t'+
'prev_prev_pos='+prev_prev_pos+'\t'+
'prev_pos='+prev_pos+'\t'+
'curr_pos='+curr_pos+'\t'+
'next_pos='+next_pos+'\t'+
'next_next_pos='+next_next_pos+'\t'+
'curr_tag='+curr_tag+'\t'+
'c_person_check='+str(True if persons_list.__contains__(curr_token.lower()) else False)+'\t'+
'c_loctn_check='+str(True if locations_list.__contains__(curr_token.lower()) else False)+'\t'+
'c_org_check='+str(True if org_list.__contains__(curr_token.lower()) else False)+'\t'+
'c_misc_check='+str(True if misc_list.__contains__(curr_token.lower()) else False)+'\t'+
'@@'+'\n')
					
				
		outfile.write('\n')
					
				
featurebuilder = FeatureBuilder(sys.argv[1])
featurebuilder.featurebuild(sys.argv[1],sys.argv[2])
