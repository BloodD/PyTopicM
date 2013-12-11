# -*- coding: utf-8 -*-
# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#This code is GUI tool for topic modeling and paper recommandation task.
#Author: Dang Xiaobin
#Email:  dangxiaobin@gmail.com
#Date:   20/10/2012
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

# system packages 
import thread 
import os
import sys
import numpy as np
import string
from time import sleep, ctime
import random

# third party packages

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# local packages
from tablemodel import TMTableModel
from listmodel import TMListModel,TMListPaperModel
from datamodel import TMDataModel
from wordpipemodel import TMWordPipeModel
from wordCloudDraw import TMWordCloudDraw

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class TMMainWidget(QMainWindow):
    """
    Main window that display the framework.
    """
    def __init__(self):
        """
        Initial parameters and window.
        """
        super(TMMainWidget, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # work directory 
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
        # initial font
        self.font = QFont('Times New Roman',13)

        # initial global buffer
        self.paperList=[]       
        self.targetfile = ''
        self.wordstream = []

        # initial parameters and enums
        self.stemmers = ['Snowball','Regexp']
        self.colorSchemes = ['oldschool','citrus','goldfish','audacity']

        # initial models       
        self.tmDataModel = TMDataModel()
        self.tmWordPipe = TMWordPipeModel()
        self.wordCloudWidget = TMWordCloudDraw()

        # initial gui
        self.createActions()
        self.createMenu()
        self.createToolbar()
        self._initGUI() 
            
    def _initGUI(self):
        """
        Create main window's layout.
        """
        #topic model parameter defination
        self.topicNum = QLabel('Topic Number: ')
        self.topicWordsNum = QLabel('Topic word Number:')
        self.iterationNum = QLabel('Iteration Number:')
        
        self.topicNumEdit = QLineEdit('30')
        self.topicWordsNumEdit = QLineEdit('20')
        self.iterationNumEdit = QLineEdit('1000')
        self.isStemCheckBox = QCheckBox('Word Stemmer:')
        self.isStemComboBox = QComboBox()
        
        self.runButton = QPushButton("Run")
        self.refreshButton = QPushButton("Show")
        self.displaywordCloudButton = QPushButton("WordCloud")
        self.colorLabel = QLabel('WordCloud:')
        self.cloudWordNum = QLabel(' Size: ')
        self.schemeComboBox = QComboBox()
        self.wordCloudCount = QLineEdit('30')
        
        self.runButton.setIcon(QIcon(os.path.join(self.iconDir,
                                                  'run.png')))
        self.refreshButton.setIcon(QIcon(os.path.join(self.iconDir,
                                                        'display.png')))
        self.runButton.setFixedWidth(60)
        self.refreshButton.setFixedWidth(60)

        self.displaywordCloudButton.setFixedWidth(100)
        self.displaywordCloudButton.setIcon(QIcon(os.path.join(self.iconDir,'cloud.png')))
  
        #topic recommendation parameter defination
        self.topicId = QLabel('Topic ID:')
        self.threshold = QLabel('Threshold:')
        self.paperId = QLabel('Paper ID:')

        self.topicIdEdit = QLineEdit('0')
        self.thresholdEdit =QLineEdit('0.2')
        self.searchButton = QPushButton(self.tr("Search"))
        self.searchButton.setIcon(QIcon(os.path.join(self.iconDir,'search.png')))
        
        #Widget parameters
        self.topicNumEdit.setFixedWidth(75)
        self.topicWordsNumEdit.setFixedWidth(75)
        self.iterationNumEdit.setFixedWidth(75)

        self.wordCloudCount.setFixedWidth(25)
        self.schemeComboBox.addItems(self.colorSchemes)
        self.isStemComboBox.addItems(self.stemmers)
        
        self.topicIdEdit.setFixedWidth(75)
        self.thresholdEdit.setFixedWidth(75)
        self.searchButton.setFixedWidth(75)
    
        # activition connection 
        self.topicNumEdit.editingFinished.connect(self.setTMParameters)
        self.topicWordsNumEdit.editingFinished.connect(self.setTMParameters)
        self.iterationNumEdit.editingFinished.connect(self.setTMParameters)

        self.runButton.clicked.connect(self.runTopicModel)
        self.refreshButton.clicked.connect(self.refreshTopicView)
        self.displaywordCloudButton.clicked.connect(self.wordCloudPaint)
        self.wordCloudCount.editingFinished.connect(self.setWCParameters)
        self.schemeComboBox.currentIndexChanged.connect(self.setWCParameters)
        
        self.searchButton.clicked.connect(self.searchRecommandPapers)

        # construct main view        
        mainSplitter = QSplitter(Qt.Horizontal,self)
        gridP  = QGridLayout()
        buttons = QHBoxLayout()
        cloud = QHBoxLayout()
        BoxT = QVBoxLayout()
        
        gridT  = QGridLayout()
        
        rightWidget = QWidget()
        rightWidget.setMaximumWidth(280)
        rightBox = QVBoxLayout()

        leftSplitter = QSplitter(Qt.Vertical,self)
        
        # set right parameter layoyt
        upGroup = QGroupBox('Topic modeling')
        downGroup = QGroupBox('Paper recommandation')
       
        upGroup.setAlignment(0)
        downGroup.setAlignment(0)

        # main right display layout
        self.wordFreqView = QTableView()
        self.topicTableView = QTableView()
        self.topicListView = QListView()
        self.wordFilterView = QPlainTextEdit()
        
        self.titleListView = QListView()
        self.abstractView = QPlainTextEdit()
        self.wordCloudView = QWidget()
        self.wordCloudLayout = QVBoxLayout()
        self.wordCloudView.setLayout(self.wordCloudLayout)
  
        # initial layouts parameters 
        self.titleListView.setSpacing(2)
        self.topicListView.setIconSize(QSize(16,16))
        self.titleListView.setIconSize(QSize(15,15))

        self.topicListView.setFont(self.font)
        self.titleListView.setFont(self.font)
        self.abstractView.setFont(self.font)
        self.wordFilterView.setFont(self.font)
        
        self.topicListView.setToolTip('Here is the topics in your abstracts!')
        self.titleListView.setToolTip('Here is the paper title recommanded to you!')
        self.abstractView.setToolTip('Here is the abstract of paper IDxxxxx!')
        self.wordFilterView.setToolTip('Input useless words and run topic modeling \
                                        again! e.g abstract research result...')
       
        self.topicListView.doubleClicked.connect(self.showRecommandPapers)
        self.titleListView.doubleClicked.connect(self.displayAbstract)


        gridP.addWidget(self.topicNum,0,0)
        gridP.addWidget(self.topicNumEdit,0,1)
        gridP.addWidget(self.topicWordsNum,1,0)
        gridP.addWidget(self.topicWordsNumEdit,1,1)
        gridP.addWidget(self.iterationNum,2,0)
        gridP.addWidget(self.iterationNumEdit,2,1)
        gridP.addWidget(self.isStemCheckBox,3,0)
        gridP.addWidget(self.isStemComboBox,3,1)

        #buttons.addSpacing(20)
        buttons.addWidget(self.runButton)
        buttons.addWidget(self.refreshButton)
        buttons.addWidget(self.displaywordCloudButton)

        cloud.addSpacing(5)
        cloud.addWidget(self.colorLabel)
        cloud.addWidget(self.wordCloudCount)
        cloud.addWidget(self.schemeComboBox)
        # cloud.addWidget(self.cloudWordNum)
        
        BoxT.addLayout(gridP)
        BoxT.addLayout(cloud)
        BoxT.addLayout(buttons)

        upGroup.setLayout(BoxT)

        gridT.addWidget(self.topicId,0,0)
        gridT.setHorizontalSpacing(50)
        gridT.addWidget(self.topicIdEdit,0,1)
        gridT.addWidget(self.threshold,1,0)
        gridT.setHorizontalSpacing(50)
        gridT.addWidget(self.thresholdEdit,1,1)
        gridT.addWidget(self.searchButton)
       
        downGroup.setLayout(gridT)
        
        rightBox.addWidget(upGroup)
        rightBox.addWidget(downGroup)
        rightBox.addWidget(self.wordFreqView)
        rightWidget.setLayout(rightBox)
        
        # set left parameter layoyt
        icon1 = QIcon(os.path.join(self.iconDir,'table.png'))
        icon2 = QIcon(os.path.join(self.iconDir,'list.png'))
        icon3 = QIcon(os.path.join(self.iconDir,'filter.png'))
        icon4 = QIcon(os.path.join(self.iconDir,'cloud.png'))
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.topicListView,icon2,'List View')
        self.tabWidget.addTab(self.topicTableView,icon1,'Table View')
        self.tabWidget.addTab(self.wordCloudView,icon4,'Word Cloud View')
        self.tabWidget.addTab(self.wordFilterView,icon3,'Filter Editer')
        leftSplitter.addWidget(self.tabWidget)
        
        lSplitter=QSplitter(Qt.Horizontal,self)

        self.tabListWidget = QTabWidget()
        self.tabAbsWidget = QTabWidget()
        self.tabListWidget.addTab(self.titleListView,'Recommanded Papers:')
        self.tabAbsWidget.addTab(self.abstractView,'Abstract:')
        lSplitter.addWidget(self.tabListWidget)
        lSplitter.addWidget(self.tabAbsWidget)
        leftSplitter.addWidget(lSplitter)
        
        mainSplitter.addWidget(leftSplitter)
        mainSplitter.addWidget(rightWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(QHBoxLayout()) 
        centralWidget.layout().addWidget(mainSplitter)   
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(self.tr('PYTM'))    
        self.setWindowState(Qt.WindowMaximized)
        self._center()
        self.show()


#####################################################
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def openFileDialog(self):
        """
        Open a data set file dialog.
        The file should be Endnote exported formation using all field,txt.
        """
        targetFilename = QFileDialog.getOpenFileName(self,'Open abstract file',
                                                     self.datadir,'txt files(*.txt)')
        if not targetFilename.isEmpty(): 
            self.targetfile = str(targetFilename)
            self.tmDataModel.setTargetFileName(self.targetfile)
            return True
        else:
            return False


    def createActions(self):
        """
        create action in main window framework.
        """
        self.actions = {} 

        self.actions['Open'] = QAction(QIcon(os.path.join(self.iconDir,'open.png')),
                                       self.tr("&Open abstracts file"),self)
        self.actions['Open'].setShortcut(self.tr("Ctrl+O"))
        self.actions['Open'].triggered.connect(self.openFileDialog)
        
        self.actions['SaveTopics'] = QAction(QIcon(os.path.join(self.iconDir,'savet.png')),
                                             self.tr("&Save Topics"),self)
        self.actions['SaveTopics'].setShortcut(self.tr("Ctrl+S"))
        self.actions['SaveTopics'].triggered.connect(self.saveTopicsDialog)
        
        self.actions['SavePaperList'] = QAction(QIcon(os.path.join(self.iconDir,'savep.png')),
                                                self.tr("&Save Paper list"),self)
        self.actions['SavePaperList'].setShortcut(self.tr("Ctrl+W"))
        self.actions['SavePaperList'].triggered.connect(self.savePaperListDialog)
        
        self.actions['Exit'] = QAction(QIcon(os.path.join(self.iconDir,'exit.png')),
                                       self.tr("&exit"),self)
        self.actions['Exit'].setShortcut(self.tr("Ctrl+E"))
        self.actions['Exit'].triggered.connect(self.close)
        
        self.actions['RunModeling'] = QAction(QIcon(os.path.join(self.iconDir,'run.png')),
                                              self.tr("&Run Modeling"),self)
        self.actions['RunModeling'].setShortcut(self.tr("Ctrl+R"))
        self.actions['RunModeling'].triggered.connect(self.runTopicModel)
       
        self.actions['DisplayTopic'] = QAction(QIcon(os.path.join(self.iconDir,'display.png')),
                                               self.tr("&Display Topics"),self)
        self.actions['DisplayTopic'].setShortcut(self.tr("Ctrl+D"))
        self.actions['DisplayTopic'].triggered.connect(self.refreshTopicView)

        self.actions['WordCloud'] = QAction(QIcon(os.path.join(self.iconDir,'cloud.png')),
                                            self.tr("&Word Cloud"),self)
        self.actions['WordCloud'].setShortcut(self.tr("Ctrl+K"))
        self.actions['WordCloud'].triggered.connect(self.wordCloudPaint)

        self.actions['SearchPaper'] = QAction(QIcon(os.path.join(self.iconDir,'search.png')),
                                              self.tr("&Search Papers"),self)
        self.actions['SearchPaper'].setShortcut(self.tr("Ctrl+Q"))
        self.actions['SearchPaper'].triggered.connect(self.showRecommandPapers)
   
        self.actions['Font'] = QAction(QIcon(os.path.join(self.iconDir,'font.png')),
                                       self.tr("&Change font"),self)
        self.actions['Font'].setShortcut(self.tr("Ctrl+F"))
        self.actions['Font'].triggered.connect(self.fontDialog)
    
        self.actions['About PYTM'] = QAction(QIcon(os.path.join(self.iconDir,'help.png')),
                                             self.tr("&About PYTM"),self)
        self.actions['About PYTM'].setShortcut(self.tr("Ctrl+H"))
        self.actions['About PYTM'].triggered.connect(self._aboutPYTM)


    def createMenu(self):
        """
        Create main menu.
        """
        self.menuFile = self.menuBar().addMenu(self.tr("File"))
        
        self.menuFile.addAction(self.actions['Open'])
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actions['SaveTopics'])
        self.menuFile.addAction(self.actions['SavePaperList'])
        self.menuFile.addSeparator() 
        self.menuFile.addAction(self.actions['Exit'])
        
        self.menuTool = self.menuBar().addMenu(self.tr("Tool"))
        self.menuTool.addAction(self.actions['RunModeling'])
        self.menuTool.addAction(self.actions['DisplayTopic'])
        self.menuTool.addAction(self.actions['WordCloud'])
        self.menuTool.addSeparator() 
        self.menuTool.addAction(self.actions['SearchPaper'])
        self.menuTool.addSeparator()
        self.menuTool.addAction(self.actions['Font'])

        self.menuHelp = self.menuBar().addMenu(self.tr("Help"))
        self.menuHelp.addAction(self.actions ['About PYTM'])


    def createToolbar(self):
        """
        Create main tool bar.
        """
        self.toolbar = QToolBar()
        
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actions['Open'])
        self.toolbar.addAction(self.actions['SaveTopics'])
        self.toolbar.addAction(self.actions['SavePaperList'])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actions['RunModeling'])
        self.toolbar.addAction(self.actions['DisplayTopic'])
        self.toolbar.addAction(self.actions['WordCloud'])
        self.toolbar.addAction(self.actions['SearchPaper'])
        self.toolbar.addSeparator() 
        self.toolbar.addAction(self.actions['Font'])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actions['About PYTM'])
        self.toolbar.addSeparator()

        self.addToolBar(self.toolbar)


    def fontDialog(self):
        """
        Font set dialog.
        """
        self.font, ok = QFontDialog.getFont()
        if ok:
            self.topicListView.setFont(self.font)
            self.titleListView.setFont(self.font)
            self.abstractView.setFont(self.font)
            self.extraWordsView.setFont(self.font)
            self.topicTableView.setFont(self.font)


    def setTMParameters(self):
        """
        Set topic modeling parameters.
        """
        parameter = [int(self.topicNumEdit.text()),\
                     int(self.topicWordsNumEdit.text()),\
                     int(self.iterationNumEdit.text())]
        self.tmDataModel.setTopicModelParameter(parameter)


    def setWCParameters(self):
        """
        Set word cloud parameters.
        """
        parameter = [int(self.wordCloudCount.text()),\
                     int(self.schemeComboBox.currentIndex())]
        self.wordCloudWidget.setWordCloudParameter(parameter)


    def runTopicModel(self):
        """
        Open message dialog for noting run modal...
        """
        self._saveExtraWords()
        self.tmDataModel.runModel(True) 
        

    def refreshTopicView(self,listView):
        """
        When topic modeling is over, then refresh Topic views.
        """
        listModel = []
        tableModel = []
        tmptableline = []
        wordstream = []
       
        listmodel,tablemodel = self.tmDataModel.loadTopic()
        self.topicnum = len(listmodel)
        self.topicword = len(listmodel[0].split())
        #print self.topicnum, self.topicword
        
        self.topicNumEdit.setText(str(self.topicnum))
        self.topicWordsNumEdit.setText(str(self.topicword))
        self.setTMParameters()
        
        # word pipe
        if self.isStemCheckBox.isChecked(): 
            index = self.isStemComboBox.currentIndex() 
            self.tmWordPipe.setStemmer(index)
            
            for singleLine in listmodel:
                nonIdline, withIdline = self.tmWordPipe.stemTopicWordLine(singleLine)
                listModel.append(withIdline)
                wordstream.append(nonIdline)
                
            for singleWordLine in tablemodel:
                tmptableline = []
                for singleWord in singleWordLine:
                    tmptableline.append(self.tmWordPipe.stemTopicWord(singleWord))
                tableModel.append(tmptableline)
           
            wordstream = ' '.join(wordstream)
            self.wordstream = wordstream
            
            freqTableModel = self.tmWordPipe.topicWordFreq(wordstream)
            
            self._refreshTopicList(listModel)
            self._refreshTopicTable(tableModel)
            self._refreshWordFreqTable(freqTableModel)
        else:
            self._refreshTopicList(listmodel)
            self._refreshTopicTable(tablemodel)
            
            for singleLine in listmodel:
                wordline = singleLine.split()                        
                wordline.remove(wordline[0])
                wordstream.append(' '.join(wordline))
            wordstream = ' '.join(wordstream)
            self.wordstream = wordstream
            
            freqTableModel = self.tmWordPipe.topicWordFreq(wordstream)
            
            self._refreshWordFreqTable(freqTableModel)
            
            
    def _refreshTopicList(self,listmodel):
        """
        Set the list view
        """
        listModel = TMListModel(listmodel)
        self.topicListView.setModel(listModel)
        self.topicListView.reset()

        # set view property
        self.topicListView.setSpacing(2)

    def _refreshTopicTable(self,tablemodel):
        """
        Set the table view
        """
        tableDataset = np.array(tablemodel).T
        header = ["Topic %s"%i for i in range(0,self.tmDataModel.getTopicModelParameter()[0])]
        tableModel = TMTableModel(tableDataset.tolist(), header, self) 
        self.topicTableView.setModel(tableModel)
   
        # hide grid
        self.topicTableView.setShowGrid(True)

        # set the font'Times New Roman',16
        self.topicTableView.setFont(self.font)

        # hide vertical header
        vh = self.topicTableView.verticalHeader()
        vh.setVisible(True)

        # set horizontal header properties
        hh =self.topicTableView.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.topicTableView.resizeColumnsToContents()

        # set row height
        nrows = tableDataset.shape[0]
        
        # print nrows
        for row in xrange(nrows):
            self.topicTableView.setRowHeight(row, 25)
            
        # enable sorting
        self.topicTableView.setSortingEnabled(True)
        self.topicTableView.reset()


    def _refreshWordFreqTable(self,tablemodel):
        """
        Set the table view
        """
        header = ['Word','Count','Frequency']
        tableModel = TMTableModel(tablemodel, header, self) 
        self.wordFreqView.setModel(tableModel)
   
        # hide grid
        self.wordFreqView.setShowGrid(True)

        # set the font'Times New Roman',16
        #self.wordFreqView.setFont(self.font)

        # hide vertical header
        vh = self.wordFreqView.verticalHeader()
        vh.setVisible(True)

        # set horizontal header properties
        hh =self.wordFreqView.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.wordFreqView.resizeColumnsToContents()

        # set row height
        nrows = len(tablemodel)
        
        # print nrows
        for row in xrange(nrows):
            self.wordFreqView.setRowHeight(row, 25)
            
        # enable sorting
        self.wordFreqView.setSortingEnabled(False)
        self.wordFreqView.reset()


    def searchRecommandPapers(self):
        """
        Rearch paper that most relative to topic user chosen.
        """
        #set recommand parameter
        parameter = [self.topicIdEdit.text(),self.thresholdEdit.text()] 
        self.tmDataModel.setSearchParameter(parameter)
        #search papers
        papers = self.tmDataModel.searchPaper()
        self.paperList = papers
        titlemodel=TMListModel(papers)
        self.titleListView.setModel(titlemodel)


    def showRecommandPapers(self): 
        """
        Show relative paper when double click the topic list.
        """
        index = self.topicListView.currentIndex()
        id = index.row()
        
        self.topicIdEdit.setText(str(id))

        #set recommand parameter
        parameter = [self.topicIdEdit.text(),self.thresholdEdit.text()] 
        self.tmDataModel.setSearchParameter(parameter)
        #search papers
        papers = self.tmDataModel.searchPaper()
        self.paperList = papers
        #print papers
        titlemodel=TMListModel(papers)
        self.titleListView.setModel(titlemodel)


    def displayAbstract(self):
        """
        Display the choosed paper in Recommand result set.
        """
        index = self.titleListView.currentIndex()
        id = self.tmDataModel.getIDList()[index.row()]
        
        if len(id)==0:
            self.abstractView.setPlainText('')
            return 'Parameter error!'

        str = '%s Abstract:'%id
        self.tabAbsWidget.setTabText(0,QString(str))
        absContent = self.tmDataModel.getAbstract(id)

        if absContent != '':
            self.abstractView.setPlainText(absContent)
        else:
            self.abstractView.setPlainText('Please input right paper ID number,e.g. ID100123.')


    def showAbstract(self):    
        """
        When input the paper ID,display the abstract. e.g. ID100123
        """
        Id = self.paperIdEdit.text() 
        if len(Id)==0:
            self.abstractView.setPlainText('')
            return 'emtpy parameter!'

        absContent = self.tmDatamodel.getAbstract(Id)

        if absContent != '':
            self.abstractView.setPlainText(absContent)
        else:
            self.abstractView.setPlainText('Please input right paper ID number,e.g. ID100123.')
            

    def _saveExtraWords(self):
        """
        Save the extra words or stop words.
        """
        try:
            extFile = open(os.path.join(self.srcDir,'tmp\\extra.txt'),'w')       
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        else:
            extWord = self.wordFilterView.toPlainText()
            extFile.write(str(extWord))
            extFile.close()


    def saveTopicsDialog(self):
        """
        Save the topics to file.
        """
        savepath = QFileDialog.getSaveFileName(self,'Save topic as...',
                                               self.datadir,'txt files(*.txt)')
        topicfile = self.srcDir+'\\tmp\\topic.txt'
        
        fc = open(topicfile,'r')
        cn = fc.readlines()
        wc = open(savepath,'w')
        wc.writelines(cn)
        fc.close()
        wc.close()
        return True


    def savePaperListDialog(self):
        """
        Save the papers recommanded result.
        """
        savepath = QFileDialog.getSaveFileName(self,'Save paper list as...',
                                               self.datadir,'txt files (*.txt)')
        if not savepath.isEmpty():
            tmpfile = open(savepath,'w')
            tmpline = 'Num----ID----------Year-Journal-Topic Words-----------------\
                        ---------------------------------\n'
            tmpfile.write(tmpline)
            
            for line in self.paperList:
                line = line.replace('#      ',' \n')
                line = line.lstrip(' ')
                tmpfile.write(line)
            tmpfile.close()
        return True

    def wordCloudPaint(self):
        """
        Word cloud draw on widget.
        
        """
        wordline = '  '.join(self.wordstream)
        #print self.wordstream
        self.wordCloudWidget.createTagCloud(self.wordstream)
        self.wordCloudLayout.addWidget(self.wordCloudWidget)
        self.wordCloudWidget.update()
        
####################################################
   
    def _informationBox(self):
        QMessageBox.information(self,"Information",
                                self.tr("Model is running!"))
        self.label.setText("Information MessageBox")

    def _warningBox(self):
        button = QMessageBox.warning(self,"Warning",
                                   self.tr("Model is running!"),
                                   QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel,
                                   QMessageBox.Save)
        if button==QMessageBox.Save:
            self.label.setText("Warning button/Save")
        elif button==QMessageBox.Discard:
            self.label.setText("Warning button/Discard")
        elif button==QMessageBox.Cancel:
            self.label.setText("Warning button/Cancel")
        else:
            return

    def _aboutPYTM(self):
        QMessageBox.about(self,\
                          self.tr("About PYTM"),\
                          self.tr("<p>the <b>PYTM</b> could model the topics in the corpus.</p>"))
        #self.aboutQT()
        return True

    def aboutQT(self):
        QtBox = QMessageBox.aboutQt(self,"About Qt")
        QtBox.setText("About Qt")

'''
def main():
    """
    Main runtine to run software.
    """
    workpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
    #print workpath
    workpath = workpath.split('\\')
    workpath.pop()
    workpath.append('icon')
    iconDir = '\\'.join(workpath)
    #print iconDir
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap(os.path.join(iconDir,'tm.png')))
    splash.show()  
    app.processEvents()  
    sleep(1)    
    TMWindows = TMMainWidget()
    splash.finish(TMWindows)  
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
'''