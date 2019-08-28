#!/usr/bin/env python3

'''
e.g. remove_after_hash.py section1_2rounds_example.txt

Will skip any blank lines '\n'
Will skip any lines with whitespace to left of #.
'''

import sys
import inspect

if(len(sys.argv) != 2):
  raise SystemExit('e.g. remove_after_hash.py section1_2rounds_example.txt'+__file__+' line number: '+str(inspect.stack()[0][2]))

#ifh = open('section1_2rounds_example.txt')
ifh = open(sys.argv[1])

ofh = open('data.txt','w')

for i,line in enumerate(ifh):

  if(line != '\n'):

    tokens = line.split('#')
    #print(tokens,len(tokens))
    if(len(tokens)==2 and tokens[0] != ''):
      print(tokens[0].strip()+'\n',file=ofh,end='')
    elif(len(tokens)==1):
      print(line.strip()+'\n',file=ofh,end='')

ifh.close()
ofh.close()

print('Output file=data.txt')

exit()
