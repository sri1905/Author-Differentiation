from __future__ import division

import re
import math
from operator import itemgetter
from nltk import word_tokenize as wt

book = ['one', 'two', 'three', 'four', 'five']
stats = ['one', 'two', 'three', 'four', 'five']

n = 6 # n-gram

for itr in range(len(book)):

	fin = open('Books/'+book[itr], 'r')
	data = fin.read()
	fin.close()

	data = unicode(data, 'utf-8')
	token = wt(data)

	GvsF = {} # gram vs frequency
	count = {} # frequency vs count
	Next = {}

	# Frequencies of the grams
	for i in range(len(token)-n+1):

		gram = ''
		for j in range(n):
			gram += token[i+j]+'_'

		if gram in GvsF:
			GvsF[gram]+=1
		else:
			GvsF[gram]=1

	# Count of Frequencies
	for gram in GvsF:

		f = GvsF[gram] 
		if f in count:
			count[f]+=1
		else:
			count[f]=1

	# Sorting the frequencies
	freq = []
	for k in count.keys():
		if k not in freq:
			freq.append(k)
	freq = sorted(freq)
	last = freq[-1]

	# Finding the nearest Frequency for a given frequency
	for i in range(len(freq)):
		if freq[i]==last:
			Next[last] = 0
			continue
		Next[freq[i]] = freq[i+1]

	# GOOD TURING SMOOTHING
	GT = {}	# Good Turing scores for Freq

	for f in freq:
		if f==last:
			continue

		nplusone = count[Next[f]]
		nc = count[f]

		fstar = ((f+1)*nplusone)/nc

		GT[f]=fstar

	# List of gram GT_score to sort
	List = []
	for g in GvsF.keys():
		if GvsF[g]==last:
			continue
		tup = (g, GT[GvsF[g]])
		List.append(tup)
	List = sorted(List, key=itemgetter(1))

	# Write to File
	fout = open('Stats/'+stats[itr], 'w')

	i = 0
	for g in reversed(List):
		i+=1
		word = g[0].encode('utf-8')
		rank = str(math.log(i, 10))
		freq = str(math.log(g[1], 10))
		fout.write(word+" "+rank+" "+freq+"\n")

	fout.close()

