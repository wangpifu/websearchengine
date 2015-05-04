# coding=utf-8
from numpy import *
import os
import re
from nltk.corpus import stopwords
import nltk
import operator
import math

def getCateWordsProb(strDir):
    #strDir = TrainSample0 
    cateWordsNum = {}
    cateWordsProb = {}
    cateDir = os.listdir(strDir)
    for i in xrange(len(cateDir)):
        count = 0 # 记录每个目录下（即每个类下）单词总数
        sampleDir = strDir + '/' + cateDir[i]
        sample = os.listdir(sampleDir)
        for j in xrange(len(sample)):
            sampleFile = sampleDir + '/' + sample[j]
            words = open(sampleFile).readlines()
            for line in words:
                count = count + 1
                word = line.strip('\n')                
                keyName = cateDir[i] + '_' + word
                cateWordsProb[keyName] = cateWordsProb.get(keyName,0)+1 # 记录每个目录下（即每个类下）每个单词的出现次数
        cateWordsNum[cateDir[i]] = count
        print 'cate %d contains %d' % (i,cateWordsNum[cateDir[i]])
    print 'cate-word size: %d' % len(cateWordsProb)
    return cateWordsProb, cateWordsNum

def NBprocess(traindir,testdir,classifyResultFileNew):
    crWriter = open(classifyResultFileNew,'w')
    # traindir = 'TrainSample0'
    # testdir = 'TestSample0'
    #返回类k下词C的出现次数，类k总词数
    cateWordsProb, cateWordsNum = getCateWordsProb(traindir)

    #训练集的总词数
    trainTotalNum = sum(cateWordsNum.values())
    print 'trainTotalNum: %d' % trainTotalNum

    #开始对测试样例做分类
    testDirFiles = os.listdir(testdir)
    for i in xrange(len(testDirFiles)):
        testSampleDir = testdir + '/' + testDirFiles[i]
        testSample = os.listdir(testSampleDir)
        for j in xrange(len(testSample)):
            testFilesWords = []
            sampleDir = testSampleDir + '/' + testSample[j]
            lines = open(sampleDir).readlines()
            for line in lines:
                word = line.strip('\n')
                testFilesWords.append(word)

            maxP = 0.0
            trainDirFiles = os.listdir(traindir)
            for k in xrange(len(trainDirFiles)):
                p = computeCateProb(trainDirFiles[k], testFilesWords,\
                                    cateWordsNum, trainTotalNum, cateWordsProb)
                if k==0:
                    maxP = p
                    bestCate = trainDirFiles[k]
                    continue
                if p > maxP:
                    maxP = p
                    bestCate = trainDirFiles[k]
            crWriter.write('%s %s\n' % (testSample[j],bestCate))
    crWriter.close()

'''
 param traindir       类k
 param testFilesWords 某个测试文档
 param cateWordsNum   训练集类k下单词总数 <类目，单词总数>
 param totalWordsNum  训练集单词总数
 param cateWordsProb  训练集类k下词c出现的次数 <类目_单词 ,某单词出现次数>
 计算 条件概率 =（类k中单词i的数目+0.0001）/（类k中单词总数+训练样本中所有类单词总数）
 计算 先验概率 =（类k中单词总数）/（训练样本中所有类单词总数）
'''
def computeCateProb(traindir,testFilesWords,cateWordsNum,\
                    totalWordsNum,cateWordsProb):
    prob = 0
    wordNumInCate = cateWordsNum[traindir]  # 类k下单词总数 <类目，单词总数>
    for i in xrange(len(testFilesWords)):
        keyName = traindir + '_' + testFilesWords[i]
        if cateWordsProb.has_key(keyName):
            testFileWordNumInCate = cateWordsProb[keyName] # 类k下词c出现的次数
        else: testFileWordNumInCate = 0.0
        xcProb = math.log((testFileWordNumInCate + 0.0001) / (wordNumInCate + totalWordsNum)) # 求对数避免很多很小的数相乘下溢出                 
        prob = prob + xcProb
    res = prob + math.log(wordNumInCate) - math.log(totalWordsNum)
    return res

def computeAccuracy(rightCate,resultCate,k):
    rightCateDict = {}
    resultCateDict = {}
    rightCount = 0.0

    for line in open(rightCate).readlines():
        (sampleFile,cate) = line.strip('\n').split(' ')
        rightCateDict[sampleFile] = cate
        
    for line in open(resultCate).readlines():
        (sampleFile,cate) = line.strip('\n').split(' ')
        resultCateDict[sampleFile] = cate
        
    for sampleFile in rightCateDict.keys():
        #print 'rightCate: %s  resultCate: %s' % \
         #     (rightCateDict[sampleFile],resultCateDict[sampleFile])
        #print 'equal or not: %s' % (rightCateDict[sampleFile]==resultCateDict[sampleFile])

        if (rightCateDict[sampleFile]==resultCateDict[sampleFile]):
            rightCount += 1.0
    print 'rightCount : %d  rightCate: %d' % (rightCount,len(rightCateDict))
    accuracy = rightCount/len(rightCateDict)
    print 'accuracy %d : %f' % (k,accuracy)
    return accuracy


def step1():
    for i in range(10):       
        traindir = 'TrainSample' + str(i)
        testdir = 'TestSample' + str(i)
        classifyResultFileNew = 'classifyResultFileNew' + str(i) + '.txt'
        NBprocess(traindir,testdir,classifyResultFileNew)

def step2():
    accuracyOfEveryExp = []
    for i in range(10):
        rightCate = 'classifyRightCate'+str(i)+'.txt'
        resultCate = 'classifyResultFileNew'+str(i)+'.txt'
        accuracyOfEveryExp.append(computeAccuracy(rightCate,resultCate,i))
    return accuracyOfEveryExp


if __name__=="__main__":
    step1()
    step2()
