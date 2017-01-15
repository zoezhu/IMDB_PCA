# -*- coding: utf-8 -*-
import csv

__author__ = "Zoe ZHU"
__copyright__ = "Copyright 2017, Pitt"

# Excel cannot read the generate file, for the text in it is garbled, I think there is something tough problem with Excel
with open('/Users/zz/Desktop/doubanData.txt','r') as old:
    with open('/Users/zz/Desktop/doubanData.csv','w', encoding='utf-8') as new:
        fieldnames = old.readline().split()
        writer = csv.DictWriter(new, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        line = old.readline()
        while line:
            row = line.split('\t')
            dic = {}
            for i in range(len(fieldnames)):
                dic[fieldnames[i]] = row[i]
            # print(dic)
            writer.writerow(dic)
            line = old.readline()