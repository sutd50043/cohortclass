from mapreduce import *
import sys

infile = open(sys.argv[1], 'r')
lines = []
for line in infile: lines.append(line.strip())

def f(text):
    wordand1s = []
    for word in text.split(): wordand1s.append((word,1))
    return wordand1s

w1s = flatMap(f,lines)

# def g(x,y): return (x+y)

# res = reduceByKey(g,w1s,0)

def g(p):
    word,icounts = p
    return (word, sum(icounts))

res = reduceByKey2(g, w1s)

for word,count in res: print("%s,%d" % (word,count))


