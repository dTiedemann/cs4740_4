#!/usr/bin/env python
from combine import *
import chunker
import mlpy

def question_candidates(q_id):
#Incomplete
	'''Select some useful subset of the candidates for a particular question.
	Return them in a list.
	'''
	return [ ('400 micrograms', 'AP881126-0094', 55, 'VP'), ('farther', 'AP881126-0094', 56, 'NP'), ('away', 'AP881126-0094', 57, 'S')]

def question_learning_data(first=201,last=399):
	x=[]
	y=[]
	for q_id in range(first,last+1):
		cand=question_candidates(q_id)
		x=x+run_evaluators(cand)
		y=y+map(lambda a:check_answers.check_answer(q_id,a),cand)
	
if __name__ == '__main__':
	main()
