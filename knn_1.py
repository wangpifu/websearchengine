# -*- coding: utf-8 -*-
import time
from os import listdir
from math import log
from numpy import *
from numpy import linalg
from operator import itemgetter

#calculate idf values of all words
def computeIDF():
    fileDir = 'processedSampleOnlySpecial_2'
    wordDocMap = {}  # <word, set(docM,...,docN)>
    IDFPerWordMap = {}  # <word, IDF>
    countDoc = 0.0
    cateList = listdir(fileDir)
    for i in xrange(len(cateList)):
        sampleDir = fileDir + '/' + cateList[i]
        sampleList = listdir(sampleDir)
        for j in xrange(len(sampleList)):
            sample = sampleDir + '/' + sampleList[j]
            for line in open(sample).readlines():
                word = line.strip('\n')
                if word in wordDocMap.keys():
                    wordDocMap[word].add(sampleList[j]) # set结构保存单词word出现过的文档
                else:
                    wordDocMap.setdefault(word,set())
                    wordDocMap[word].add(sampleList[j])
        print 'just finished %d round ' % i

    for word in wordDocMap.keys():
        countDoc = len(wordDocMap[word]) # 统计set中的文档个数
        IDF = log(20000/countDoc)/log(10)
        IDFPerWordMap[word] = IDF
 
    return IDFPerWordMap

#write idf value into file    
def main():
    start=time.clock()
    IDFPerWordMap = computeIDF()
    end=time.clock()
    print 'runtime: ' + str(end-start)
    fw = open('IDFPerWord','w')
    for word, IDF in IDFPerWordMap.items():
        fw.write('%s %.6f\n' % (word,IDF))
    fw.close()

if __name__=="__main__":
    main()