# -*- coding: utf-8 -*-
import time
from os import listdir
from math import log
from numpy import *
from numpy import linalg
from operator import itemgetter
#<cate, doc, (word1, tdidf1), (word2, tdidf2),...> 存入文件
# @param indexOfSample set 0
# @param trainSamplePercent set 9:1
########################################################
def computeTFMultiIDF(indexOfSample, trainSamplePercent):
#def computeTFMultiIDF(testSamplePercent):
    IDFPerWord = {} # <word, IDF>
    for line in open('IDFPerWord').readlines():
        (word, IDF) = line.strip('\n').split(' ')
        IDFPerWord[word] = IDF        
    
    fileDir = 'processedSampleOnlySpecial_2'
    trainFileDir = "docVector/" + 'wordTFIDFMapTrainSample' + str(indexOfSample)
    testFileDir = "docVector/" + 'wordTFIDFMapTestSample' + str(indexOfSample)
    #trainFileDir = "docVector/" + 'wordTFIDFMapTrainSample' 
    #testFileDir = "docVector/" + 'wordTFIDFMapTestSample' 

    tsTrainWriter = open(trainFileDir, 'w')
    tsTestWriter = open(testFileDir, 'w')

        
    cateList = listdir(fileDir)
    for i in xrange(len(cateList)):
        sampleDir = fileDir + '/' + cateList[i]
        sampleList = listdir(sampleDir)
        
        testBeginIndex = indexOfSample * ( len(sampleList) * (1-trainSamplePercent) )
        testEndIndex = (indexOfSample+1) * ( len(sampleList) * (1-trainSamplePercent) )
        #testBeginIndex = int(min(sampleList))
        #testEndIndex = testBeginIndex + (int(max(sampleList))-int(min(sampleList)))*testSamplePercent
        
        for j in xrange(len(sampleList)):
            TFPerDocMap = {} # <word, 文档doc下该word的出现次数>
            sumPerDoc = 0  # record total words num in file
            sample = sampleDir + '/' + sampleList[j]
            for line in open(sample).readlines():
                sumPerDoc += 1
                word = line.strip('\n')
                TFPerDocMap[word] = TFPerDocMap.get(word, 0) + 1
            
            if(j >= testBeginIndex) and (j <= testEndIndex):
                tsWriter = tsTestWriter
            else:
                tsWriter = tsTrainWriter

            tsWriter.write('%s %s ' % (cateList[i], sampleList[j])) # 写入类别cate，文档doc

            for word, count in TFPerDocMap.items():
                TF = float(count)/float(sumPerDoc)
                tsWriter.write('%s %f ' % (word, TF * float(IDFPerWord[word]))) # 继续写入类别cate下文档doc下的所有单词及它的TF-IDF值

            tsWriter.write('\n')

        print 'just finished %d round ' % i

        #if i==0: break

    tsTrainWriter.close()
    tsTestWriter.close()
    tsWriter.close()

if __name__=="__main__":
        computeTFMultiIDF(0,0.9)