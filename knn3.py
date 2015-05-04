# -*- coding: utf-8 -*-
import time
from os import listdir
from math import log
from numpy import *
from numpy import linalg
from operator import itemgetter

def doProcess():
    trainFiles = 'docVector/wordTFIDFMapTrainSample0'
    testFiles = 'docVector/wordTFIDFMapTestSample0'
    kNNResultFile = 'docVector/KNNClassifyResult0'

    trainDocWordMap = {}  # 字典<key, value> key=cate_doc, value={{word1,tfidf1}, {word2, tfidf2},...}

    for line in open(trainFiles).readlines():
        lineSplitBlock = line.strip('\n').split(' ')
        trainWordMap = {}
        m = len(lineSplitBlock)-1
        for i in xrange(2, m, 2):  # 在每个文档向量中提取(word, tfidf)存入字典
            trainWordMap[lineSplitBlock[i]] = lineSplitBlock[i+1]

        temp_key = lineSplitBlock[0] + '_' + lineSplitBlock[1]  # 在每个文档向量中提取类目cate，文档doc，
        trainDocWordMap[temp_key] = trainWordMap 

    testDocWordMap = {}

    for line in open(testFiles).readlines():
        lineSplitBlock = line.strip('\n').split(' ')
        testWordMap = {} 
        m = len(lineSplitBlock)-1
        for i in xrange(2, m, 2):
            testWordMap[lineSplitBlock[i]] = lineSplitBlock[i+1]

        temp_key = lineSplitBlock[0] + '_' + lineSplitBlock[1]
        testDocWordMap[temp_key] = testWordMap #<类_文件名，<word, TFIDF>>

    #check distance and classify
    count = 0
    rightCount = 0
    KNNResultWriter = open(kNNResultFile,'w')
    print 'start to write'
    for item in testDocWordMap.items():
        classifyResult = KNNComputeCate(item[0], item[1], trainDocWordMap)  # 调用KNNComputeCate做分类

        count += 1
        #print 'this is %d round' % count

        classifyRight = item[0].split('_')[0]
        KNNResultWriter.write('%s %s\n' % (classifyRight,classifyResult))
        if classifyRight == classifyResult:
            rightCount += 1
        print '%s %s rightCount:%d' % (classifyRight,classifyResult,rightCount)

    accuracy = float(rightCount)/float(count)
    print 'rightCount : %d , count : %d , accuracy : %.6f' % (rightCount,count,accuracy)
    return accuracy
            


# @param cate_Doc <cate_doc>
# @param testDic {{word, TFIDF}}
# @param trainMap <cate_doc，<word, TFIDF>>
# @return sortedCateSimMap[0][0] return minium distance

def KNNComputeCate(cate_Doc, testDic, trainMap):
    simMap = {} 
    for item in trainMap.items():
        similarity = computeSim(testDic,item[1])  # computeSim()
        simMap[item[0]] = similarity

    sortedSimMap = sorted(simMap.iteritems(), key=itemgetter(1), reverse=True) #sort by value

    k = 20
    cateSimMap = {} #<类，距离和>
    for i in xrange(k):
        cate = sortedSimMap[i][0].split('_')[0]
        cateSimMap[cate] = cateSimMap.get(cate,0) + sortedSimMap[i][1]

    sortedCateSimMap = sorted(cateSimMap.iteritems(),key=itemgetter(1),reverse=True)

    return sortedCateSimMap[0][0]   
        
    

# @param testDic <<word, tfidf>>
# @param trainDic <<word, tfidf>>
# @return cosine
def computeSim(testDic, trainDic):
    testList = []  # 测试向量与训练向量共有的词在测试向量中的tfidf值
    trainList = []  # # 测试向量与训练向量共有的词在训练向量中的tfidf值
    
    for word, weight in testDic.items():
        if trainDic.has_key(word):
            testList.append(float(weight)) # 
            trainList.append(float(trainDic[word]))

    testVect = mat(testList)  # 列表转矩阵
    trainVect = mat(trainList)
    num = float(testVect * trainVect.T)
    denom = linalg.norm(testVect) * linalg.norm(trainVect)
    #print 'denom:%f' % denom
    return float(num)/(1.0+float(denom))

if __name__=="__main__":
    doProcess()