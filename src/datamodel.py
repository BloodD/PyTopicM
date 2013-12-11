# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#Data Model modual
#Author: Dang Xiaobin
#Email:  dangxiaobin@gmail.com
#Date:   20/10/2012
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

# system packages 
import os
import sys
import numpy as np
import string

class TMDataModel():
    """
    Data model...
    """
    def __init__(self):
        # define file directory parameters
        self.modelPath = os.path.dirname(os.path.join(os.getcwd(), __file__))
        self.topicTxtFile = self.modelPath + '\\tmp\\topic.txt'   
        self.documentProfile = self.modelPath + '\\tmp\\outputtopics.txt'
        self.documentIdFile = self.modelPath + '\\tmp\\idtitle.txt'
        self.abstractFile = self.modelPath + '\\tmp\\abstracts.txt'
        self.extrawordFile = self.modelPath + '\\tmp\\extra.txt'
        self.targetFile = ''
        
        # define topic model parameters
        self.TopicModelPara = [30,20,1000,'~']
        self.SearchTopicPara =[]

        # define result buffers   
        self.topics=[]
        self.listmodel = []
        self.tablemodel = []
        self.paperList = []
        self.IDList = []
        
    def setTargetFileName(self,filename):        
        self.targetFile = filename
        #print  self.targetFile
    
    def getTopics(self):
        return self.topics

    def getPaperList(self):
        return self.paperList

    def getListModel(self):
        return self.listmodel

    def getTableModel(self):
        return self.tablemodel

    def getRecommandResult(self):
        return self.paperList

    def getIDList(self):
        return self.IDList
    
    def getTopicModelParameter(self):
        return self.TopicModelPara
    
    def getSearchParameter(self):
        return self.SearchTopicPara

    def setTopicModelParameter(self, parameter):
        if len(parameter) == 3:
            self.TopicModelPara = parameter
            
    def setSearchParameter(self,parameter):
        if len(parameter) == 2:
            self.SearchTopicPara = parameter
        
    def extractAbstractFromTarget(self):
        
        args_idTitle = self.modelPath + '\\tmp\\idtitle.txt'
        args_abs = self.abstractFile        
        abstractFile = self.targetFile
        #print abstractFile
        inputfile = open(abstractFile,'r') 
        outputIdTitle = open(args_idTitle,'w')
        outputfile = open(args_abs,'w')

        id=100000
        
        nlines = inputfile.readlines()
        #extract Title Journal Year Abstract parts
        for nline in nlines:
            if string.find(nline,'Title:')!=-1 and string.find(nline,'Short Title:')==-1:
                titlestr=''
                titlestr=nline[7:]
            elif string.find(nline,'Journal:')!=-1 and string.find(nline,'Alternate Journal:')==-1:
                journal=''
                journal=nline[9:]
            elif string.find(nline,'Year:')!=-1:
                year=''
                year=nline[6:]
            elif string.find(nline,'Abstract:')!=-1:
                id += 1
                strn = 'ID%d        %s-%s--%s#      \n'%(id,year.rstrip('\n'),\
                                                         journal.rstrip('\n'),\
                                                         titlestr.rstrip('\n'))
                outputIdTitle.write(strn)
                str=strn.rstrip('\n')
            #    print str
                abs = nline[9:]
                outputfile.write(str)
                outputfile.write(abs)
            else:
                continue
        inputfile.close()
        outputfile.close()
        outputIdTitle.close()

        print "Total papers number: %d.\n" %(id-100000)
        return True
    
    def runModel(self,isEndnote):
        if isEndnote == True:
            if self.extractAbstractFromTarget() != True:
                return False
            
        '''
        self.workpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
        self.workpath = self.workpath.split('\\')
        self.workpath.pop()
        self.workpath.append('icon')
        self.iconDir = '\\'.join(self.workpath)
        self.workpath.pop()
        self.workpath.append('src')
        self.srcDir = '\\'.join(self.workpath)
        self.workpath.pop()
        self.workpath.append('data')
        self.datadir = '\\'.join(self.workpath)
        '''
        self.workpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
        self.workpath = self.workpath.split('\\')
        self.workpath.append('tmp')
        self.workpath.append('tops.mallet')
        self.tmp = '\\'.join(self.workpath)
       #print self.tmp
        self.workpath.pop()
        self.workpath.pop()
        self.workpath.append('mallet')
        self.mallet = '\\'.join(self.workpath)
        self.workpath.append('class')
        self.classpath0 = '\\'.join(self.workpath)
        
        self.workpath.pop()
        self.workpath.append('lib')
        self.workpath.append('mallet-deps.jar')
        self.classpath1 = '\\'.join(self.workpath) 
        self.classpath =  self.classpath0 +';'+ self.classpath1
        #print self.mallet
        #print self.classpath

        cmd_create_instance = "java -Xmx128m -ea -Dfile.encoding=UTF-8 \
             -classpath %s cc.mallet.classify.tui.Csv2Vectors \
            --input %s --output %s --keep-sequence --remove-stopwords TRUE \
            --extra-stopwords %s"%(self.classpath, self.abstractFile,\
                                                       self.tmp, self.extrawordFile)
                                
        '''                        
        cmd_create_instance = 'mallet  import-file --input %s --output ./tmp/tops.mallet --keep-sequence \
                                --remove-stopwords TRUE --extra-stopwords %s'%(self.abstractFile,\                                                                             self.extrawordFile)
        '''
        os.system(cmd_create_instance)
        
        #print cmd_create_instance
        
        cmd_run_model = "java -Xmx128m -ea -Dfile.encoding=UTF-8 \
             -classpath %s cc.mallet.topics.tui.Vectors2Topics \
            --input ./tmp/tops.mallet --num-topics %s --num-top-words %s \
                    --num-iterations %s  --num-threads 1  --output-state ./tmp/topicmodel.state.gz \
                    --output-doc-topics ./tmp/outputtopics.txt --topic-word-weights-file ./tmp/wordtopic.txt \
                    --output-topic-keys ./tmp/topic.txt"%(self.classpath,self.TopicModelPara[0],\
                                                          self.TopicModelPara[1],self.TopicModelPara[2])
                                                          
        '''                                              
        cmd_run_model = 'mallet  train-topics --input ./tmp/tops.mallet --num-topics %s --num-top-words %s \
                    --num-iterations %s  --num-threads 1  --output-state ./tmp/topicmodel.state.gz \
                    --output-doc-topics ./tmp/outputtopics.txt --topic-word-weights-file ./tmp/wordtopic.txt \
                    --output-topic-keys ./tmp/topic.txt'%(self.TopicModelPara[0],\
                                                          self.TopicModelPara[1],\
                                                          self.TopicModelPara[2])
        '''                                                  
        #print cmd_run_model
        os.system(cmd_run_model)
        print "Modeling is over!"
        
    def getAbstract(self,id):
        Id = id
        absfile = open(self.abstractFile,'r') 
        abslines = absfile.readlines()
        
        for absline in  abslines:
            if string.find(absline,Id)!=-1:
                strall = absline.split('#')
                absstr = "Abstract:    %s"%(strall[1].lstrip())
        absfile.close()
        return absstr
    
    def loadTopic(self):
        """
        load topic txt and create table list/view model dataset
        """
      # if os.access(self.topicTxtFile, os.R_OK):
        topicfile = open(self.topicTxtFile,'r')
        topicList = topicfile.readlines()
        self.listmodel = []
        self.tablemodel = []
        self.topics = []
        
        for topic in topicList:
            """
            remove alpha value
            """
            tmp = topic.split('\t',3)
            tmp.remove(tmp[1])
            topicString = '     '.join(tmp)
            topicString = topicString.rstrip('\n')
            self.listmodel.append(topicString)

            wordTable = topic.split()
            wordTable.remove(wordTable[0])
            wordTable.remove(wordTable[0])
            self.tablemodel.append(wordTable)
      # print "listmodel",self.listmodel,"tablemodel",self.tablemodel
        topicfile.close()
        return self.listmodel,self.tablemodel
        
    def searchPaper(self):
        
        self.topicId = self.SearchTopicPara[0]
        self.threshold = self.SearchTopicPara[1]
        
        self.paperList=[]      
        self.papers=[]
        self.IDList=[]
        
        profile = open(self.documentProfile,'r')
        idtitle = open(self.documentIdFile,'r')
        
        profile.readline()
        prolist = profile.readlines()
        idtitlelist = idtitle.readlines()
        
        count=0
        
        for l in prolist:
            ins = string.split(l)
            array = np.array(ins)
            d = array.reshape((len(array)/2),2)
            for i in d[1:]:
                if i[0]==self.topicId and \
                        i[1]>=self.threshold:
                   count+=1
                   for ii in idtitlelist:
                       if string.find(ii,d[0][1])!=-1:
                          stt = "%s  %s"%(count,ii)
                          self.paperList.append(stt)
                          st = "%s  %s"%(count,ii.rstrip('\n'))
                          self.papers.append(st)
                          IDx = ii.split()
                          self.IDList.append(IDx[0])
        profile.close()
        idtitle.close()
        return self.papers
    

    