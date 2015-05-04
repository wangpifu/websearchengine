from numpy import *
import os
import re
from nltk.corpus import stopwords
import nltk
import operator

# calculate freq of every word
# return key-sorted dict
def countWords():
    wordMap = {}
    newWordMap = {}
    fileDir = 'processedSample_includeNotSpecial'
    sampleFilesList = os.listdir(fileDir)
    for i in xrange(len(sampleFilesList)):
        sampleFilesDir = fileDir + '/' + sampleFilesList[i]
        sampleList = os.listdir(sampleFilesDir)
        for j in xrange(len(sampleList)):
            sampleDir = sampleFilesDir + '/' + sampleList[j]
            for line in open(sampleDir).readlines():
                word = line.strip('\n')
                wordMap[word] = wordMap.get(word,0.0) + 1.0
    #return words which freq>4
    for key, value in wordMap.items():
        if value > 4:
            newWordMap[key] = value
    sortedNewWordMap = sorted(newWordMap.iteritems())
    print 'wordMap size : %d' % len(wordMap)
    print 'newWordMap size : %d' % len(sortedNewWordMap)
    return sortedNewWordMap


# create files contain selves' attribute word(freq>4 in this test)
def filterSpecialWords():
    fileDir = 'processedSample_includeNotSpecial'
    wordMapDict = {}
    sortedWordMap = countWords()
    for i in range(len(sortedWordMap)):
        wordMapDict[sortedWordMap[i][0]]=sortedWordMap[i][0]    
    sampleDir = os.listdir(fileDir)
    print sampleDir
    for i in range(len(sampleDir)):
        targetDir = 'processedSampleOnlySpecial_2' + '/' + sampleDir[i]
        srcDir = 'processedSample_includeNotSpecial' + '/' + sampleDir[i]
        if os.path.exists(targetDir) == False:
            print "false"
            os.makedirs(targetDir)
        sample = os.listdir(srcDir)
        for j in range(len(sample)):
            targetSampleFile = targetDir + '/' + sample[j]
            fr=open(targetSampleFile,'w')
            srcSampleFile = srcDir + '/' + sample[j]
            for line in open(srcSampleFile).readlines():
                word = line.strip('\n')
                if word in wordMapDict.keys():
                    fr.write('%s\n' % word)
            fr.close()

if __name__=="__main__":
    filterSpecialWords()