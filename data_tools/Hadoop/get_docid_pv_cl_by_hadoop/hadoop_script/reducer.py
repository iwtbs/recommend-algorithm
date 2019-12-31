#coding=gbk
import sys
import traceback
import os
import time
import math

docid = ""
pre_docid = ""
pv = 0
cl = 0

for line in sys.stdin:
    line = line.strip().decode("gbk","ignore")
    item = line.split('\t')
    if len(item) != 2:
        continue
    docid = item[0]
    if docid != pre_docid and pre_docid != "":
        output = pre_docid + "\t" + str(pv) + "\t" + str(cl)
        print output.encode("gbk","ignore")
        pv = 0
        cl = 0
    if item[1] == "pv":
        pv += 1
    elif item[1] == "cl":
        cl += 1
    pre_docid = docid

if docid != "":
    print docid + "\t" + str(pv) + "\t" + str(cl)
