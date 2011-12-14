from array import array

f = open('shredded.txt')

input_table = []
for str in  f:
  input_table.append(str.strip().split('|'))

"""Transpose"""
col_table = zip(*input_table)
print repr(col_table[1][5])
#for line in input_table:
  #print line[2]

