# -*- coding: utf-8 -*-
# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#Table view model
#Author: Dang Xiaobin
#Email:  dangxiaobin@gmail.com
#Date:   20/10/2012
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

# system packages 
import os
import sys
import string

# third party packages
import numpy as np
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import RegexpStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


class TMWordPipeModel():
    """
    Stemmer and word frequent
    """
    def __init__(self):
        self._stemmer = ['SnowballStemmer',\
                         'RegexpStemmer']
                         #'LancasterStemmer']
        self.stemmer = ''
        self.result = []
        self.word = ''
        
    def setStemmer(self,id):
        """Choose a stemmer """
        self.stemmer = self._stemmer[id]
        
    def stemTopicWord(self,word):
        """
        Stem single word.
        """
        if self.stemmer == self._stemmer[0]:
            stemmer = SnowballStemmer('english')
            self.word = stemmer.stem(word) 
           # print self.word
      
        elif self.stemmer == self._stemmer[1]:
            #stemmer = RegexpStemmer('ing$|s$|es$|d$|', min=4)
            stemmer = RegexpStemmer('s$|', min=4)
            self.word = stemmer.stem(word)
          #  print self.word
        else:
            return word
        '''
        elif self.stemmer == self._stemmer[1]:
            stemmer = LancasterStemmer()
            self.word = stemmer.stem(word)   
         #   print self.word
        '''
        return self.word
        
    def stemTopicWordLine(self,wordLine):
        """
        Srem word line. a string.
        """
        result = []
        self.result = []
        self.nonIdResult = []
        
        wordsTokens = WhitespaceTokenizer().tokenize(wordLine)
       
        if self.stemmer == self._stemmer[0]:
            stemmer = SnowballStemmer('english')
            for word in wordsTokens:
                result.append(stemmer.stem(word))
           # print self.result
        elif self.stemmer == self._stemmer[1]:
            #stemmer = RegexpStemmer('ing$|s$|es$|d$|', min=4)
            stemmer = RegexpStemmer('s$|', min=4)
            for word in wordsTokens:
                result.append(stemmer.stem(word))
           # print self.result
        else:
            return wordLine

        self.result = '  '.join(result)
        result.remove(result[0])        
        self.nonIdResult = ' '.join(result)
        
         
        '''
        elif self.stemmer == self._stemmer[1]:
            stemmer = LancasterStemmer()
            for word in wordsTokens:
                result.append(stemmer.stem(word))
           # print self.result
        '''
        return self.nonIdResult,self.result
    
    def topicWordFreq(self,wordline):
        """
        Statistic word stream frequency.
        """
        wordstream = []
        wordsTokens = WhitespaceTokenizer().tokenize(wordline)
        wordsTokens.remove(wordsTokens[0])
        wordstream.append('  '.join(wordsTokens))
        wordstream = ' '.join(wordstream)
        #print wordstream
        
        fdist = FreqDist()
        for word in word_tokenize(wordstream):
            fdist.inc(word)
        result = [list(item) for item in fdist.items()]
        num = float(fdist.N())
        result = [[val[0],val[1],val[1]/num] for val in result]
        #print "smaples:"
        #print fdist.items()
        #print fdist.keys()
       
        return result
       
    def removeRepetitiveWord(self,wordList):
        """
        Remove repetiveWord.
        """
        list = wordList
        tmpList = sorted(set(list),key=list.index)
        return tmpList

"""
def main():
   
    word = ['1 connectivity connectivitys connectivitys connectivitys functional brain \
    structural network networks fmri regions anatomical state activation global graph \
    properties cortical organization efficiency resting scale',
            '2 high resolution time imaging spatial data signal effects results number \
            noise contrast present acquired low standard improved measurements parameters',
            '3 tractography imaging mr mm nerve images methods volunteers conclusion \
            obtained purpose sequence materials study nerves single muscle feasibility radiol',
            '4 asd asd asd asd asd asd asd d s as sdf']
    print word
    wp = TMWordPipeModel()
    wp.setStemmer(2)
    for l in word:
        list = wp.stemTopicWordLine(l)
        wp.topicWordFreq(list)
        #print list
    #rr = wp.removeRepetitiveWord(list)
   
   # print rr
        
if __name__ == '__main__':
    main()
"""