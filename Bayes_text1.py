# coding=utf-8
from numpy import *
import os
import re
from nltk.corpus import stopwords
import nltk
import operator
def createFiles():
    srcFilesList = os.listdir('originSample')
    for i in range(len(srcFilesList)):
        if i==0: continue
        dataFilesDir = 'originSample/' + srcFilesList[i] # 20个文件夹每个的路径
        dataFilesList = os.listdir(dataFilesDir)
        targetDir = 'processedSample_includeNotSpecial/' + srcFilesList[i] # 20个新文件夹每个的路径
        if os.path.exists(targetDir)==False:
            os.makedirs(targetDir)
        else:
            print '%s exists' % targetDir
        for j in range(len(dataFilesList)):
            createProcessFile(srcFilesList[i],dataFilesList[j]) # 调用createProcessFile()在新文档中处理文本
            #print '%s %s' % (srcFilesList[i],dataFilesList[j])

def createProcessFile(srcFilesName,dataFilesName):
    srcFile = 'originSample/' + srcFilesName + '/' + dataFilesName
    targetFile= 'processedSample_includeNotSpecial/' + srcFilesName\
                + '/' + dataFilesName
    fw = open(targetFile,'w')
    dataList = open(srcFile).readlines()
    for line in dataList:
        resLine = lineProcess(line) # 调用lineProcess()处理每行文本
        for word in resLine:
            fw.write('%s\n' % word) #一行一个单词
    fw.close()
def lineProcess(line):
    stopwords = nltk.corpus.stopwords.words('english') #去停用词
    porter = nltk.PorterStemmer()  #词干分析
    splitter = re.compile('[^a-zA-Z]')  #去除非字母字符，形成分隔
    words = [porter.stem(word.lower()) for word in splitter.split(line)\
             if len(word)>0 and\
             word.lower() not in stopwords]
    return words



if __name__=="__main__":
    createFiles()