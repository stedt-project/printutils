#!usr/bin/env python

import sys
import os
import itertools
import re

sources = [] #empty list which takes source chunks of stedtreferences
f = open('stedtreferences.bib','r')
text = f.read()
f.close()
for line in re.split(r'(@[^@]*)',text)[1::2]: #makes each bib entry into a list item, splitting inclusively by @
  sources.append(line)  #pipes into empty list

bib = [] #empty list to serve as 3-level list: list=>source=>sourcefields
for line in sources:
  row = []
  for subline in line.split('\n'): #split by newline
    subrow = []
    for word in re.split(r'\s\=\s', subline): #split by '  = '
      subrow.append(word) #put each source field element in source field line
    row.append(subrow) #put each source field line in source line
  bib.append(row) #put each source line in bib

for line in bib: 
  for subline in line:
    if len(subline) > 1:
      if subline[1] == '{},':           #get rid of empty fields 
        line.pop(line.index(subline))   #automatically generated by makeBib

def imprint( bib ):
  journ = re.compile(r'.*[\d|\(|\)]+\:\d+') #regex to find journal imprint, e.g., '97:123-234'
  book = re.compile(r'\w*\:\ \w*') #regex to find book imprint, e.g., 'Wiesbaden: Reichert'
  for line in bib:
    for subline in line:
      if subline[0].startswith('imprint'):
        if re.match(journ,subline[1]): #journ regex found?
          parts = re.split(r'[\d]*',subline[1][1:-3]) #split by just [\d]* to get volume
          if '. ' in subline[1][1:-3]:
            pgs = subline[1][1:-3].split('. ')[-1].split(':') #strips out punctuation after journal title, splits by ':'
          else:
            pgs = subline[1][1:-3].split()[-1].split(':') #splits by ':'
          journl = ['journal',str('{'+parts[0].strip(' .')+'},')] #takes first element of imprint, assumed to be journal title (sometimes gets more than that)
          vol = ['volume',str('{'+pgs[0].strip(' .')+'},')] #takes first element of pgs, thought to be journal volume
          if len(pgs) > 1:
            pgs = ['pages',str('{'+pgs[1].strip(' .')+'},')] #takes 2nd element of pgs, thought to be pg nos
          line.insert(-4,journl) #inserts these fields
          line.insert(-4,vol)    #back into source
          line.insert(-4,pgs)    #
        if re.match(book,subline[1]):
          parts = subline[1].split(': ')
          address = ['address',str('{'+parts[0]+'},')]
          publisher = ['publisher',str('{'+parts[1]+'},')]
          line.insert(-4,address)
          line.insert(-4,publisher)
# following block is incomplete. a big problem for edited volumes is that there seems to be no systematic bibliographic style employed!!
#        if 'ed.' in subline[1] or 'eds.' in subline[1]:
#          parts = re.split(r'(\d+\-\d+)|:|\e\d\.\ \b\y|\,\ \p\p\.\ ', subline[1])
#          page = re.compile(r'\d+\-\d+')
#          for word in parts:
#            if page.match(str(word)):
#              pgs = ['pages',str('{'word+'},')]
#          publisher = ['publisher',str('{'+parts[-1])]
#          if parts[-3].startswith('.  '):
#            address = ['address',str('{'+parts[-3].strip('.  ')+'},')]
#          if parts[-3].startswith('. '):
#            address = ['address',str('{'+parts[-3].strip('. ')+'},')]
          

  return bib
#        else:
#          newbib.append(subline)
#      else:
#        newbib.append(subline)
#  return newbib

def main():
#  imprint(bib)
#  for line in bib:
#    for subline in line:
#      print '\t\t= '.join(subline)
#not ready for primetime yet:
  imprint(bib)
  f = open('stedtreferences.bib', 'w')
  for line in bib:
    for subline in line:
      f.write('\t\t= '.join(subline)+'\n')
  f.close()


if __name__ == "__main__":
  main()
