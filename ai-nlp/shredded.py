from array import array
from Trigrams import Trigram

f = open('shredded.txt')

input_table = []
for str in  f:
  input_table.append(str.strip().split('|'))

"""Transpose"""
col_table = zip(*input_table)
max_i = 0;
max_prob = -1000000
for i in range(0,len(col_table)):
#for i in range(0,3):
  prob = 1
  for j in range(0,len(col_table[i])):
    word = " " + col_table[i][j]
    prob = prob + Trigram.tgram_prob(word.upper())
  print "%s : %f" % (word, prob)
  if prob > max_prob:
    max_prob = prob
    max_i = i

print "Col %d Prob: %f" % (max_i, max_prob)
print repr(col_table[max_i][j])
#for line in input_table:
  #print line[2]

