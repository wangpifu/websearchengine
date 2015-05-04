# coding=utf-8
from numpy import *
import os
import re
from nltk.corpus import stopwords
import nltk
import operator

def createTestSample(indexOfSample,classifyRightCate,trainSamplePercent=0.9):
    fr = open(classifyRightCate,'w')
    fileDir = 'processedSampleOnlySpecial_2'
    sampleFilesList=os.listdir(fileDir)
    for i in range(len(sampleFilesList)):
        sampleFilesDir = fileDir + '/' + sampleFilesList[i]
        sampleList = os.listdir(sampleFilesDir)
        m = len(sampleList)
        testBeginIndex = indexOfSample * ( m * (1-trainSamplePercent) ) 
        testEndIndex = (indexOfSample + 1) * ( m * (1-trainSamplePercent) )
        for j in range(m):
            # 序号在规定区间内的作为测试样本，需要为测试样本生成类别-序号文件，最后加入分类的结果，
            # 一行对应一个文件，方便统计准确率  
            if (j > testBeginIndex) and (j < testEndIndex): 
                fr.write('%s %s\n' % (sampleList[j],sampleFilesList[i])) # 写入内容：每篇文档序号 它所在的文档名称即分类
                targetDir = 'TestSample'+str(indexOfSample)+\
                            '/'+sampleFilesList[i]
            else:
                targetDir = 'TrainSample'+str(indexOfSample)+\
                            '/'+sampleFilesList[i]
            if os.path.exists(targetDir) == False:
                os.makedirs(targetDir)
            sampleDir = sampleFilesDir + '/' + sampleList[j]
            sample = open(sampleDir).readlines()
            sampleWriter = open(targetDir+'/'+sampleList[j],'w')
            for line in sample:
                sampleWriter.write('%s\n' % line.strip('\n'))
            sampleWriter.close()
    fr.close()

def test():
    for i in range(10):
        classifyRightCate = 'classifyRightCate' + str(i) + '.txt'
        createTestSample(i,classifyRightCate)

if __name__=="__main__":
    test()