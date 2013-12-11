# -*- coding: utf-8 -*-
# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#This code is for word tag cloud.
#Author: Dang Xiaobin
#Email:  dangxiaobin@gmail.com
#Date:   20/10/2012
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

# system packages 
import os

# third party packages
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pytagcloud import create_tag_image, create_html_data, make_tags,LAYOUT_HORIZONTAL,LAYOUT_MOST_HORIZONTAL,LAYOUT_MIX
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts
from nltk.tokenize import WhitespaceTokenizer

color = [((255, 165, 0), (218, 165, 32), (34, 139, 34), (0, 191, 255), (0, 0, 0)),
        ((255 ,255, 0), (255, 215, 0), (205, 155, 29))]
        

class TMWordCloudDraw(QWidget):
    def __init__(self):
        super(TMWordCloudDraw,self).__init__()
        self.image = QImage()
        self.workpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
        self.workpath = self.workpath.split('\\')
        self.workpath.pop()
        self.workpath.append('src\\tmp\\tmp_cloud_large.png')
        self.png = '\\'.join(self.workpath)
        #print self.png
        self.colorSchemes = ['oldschool','citrus','goldfish','audacity']
        self.color = 0
        self.wordCount = 30
        #self.show()
        
    def setWordCloudParameter(self,parameter):
        """
        Set model parameters
        """
        self.wordCount = parameter[0]
        self.color = parameter[1]
        
        
    def paintEvent(self,e):
        """
        Draw word cloud
        """
        self.painter = QPainter()
        self.painter.begin(self)
        self._drawWordCloud()
        self.painter.end()

    def drawWordCloud(self):
        """
        Draw pixelmap 
        """
        if self.image.load(self.png):
            pixcloud = QPixmap.fromImage(self.image)
            pixcloud.scaled(pixcloud.size().width(),pixcloud.size().height(),\
                             Qt.KeepAspectRatioByExpanding, Qt.FastTransformation)
            self.painter.drawPixmap(0, 0, pixcloud, 0, 0,pixcloud.size().width(),\
                                    pixcloud.size().height())

    def _drawWordCloud(self):
        """
        Draw image
        """
        if self.image.load(self.png):
            self.painter.drawImage(QPointF(10,10),self.image)
            
    def createTagCloud(self,wordline):
        """
        Create tag cloud image 
        """
        wordstream = []
        if wordline == '':
            return False
        
        wordsTokens = WhitespaceTokenizer().tokenize(wordline)
        wordsTokens.remove(wordsTokens[0])
        wordstream.append(' '.join(wordsTokens))
        wordstream = ' '.join(wordstream)
        thresh = self.wordCount
        colorS = self.colorSchemes[self.color]
        
        tags = make_tags(get_tag_counts(wordstream)[:thresh],\
                         minsize=3, maxsize=40,\
                         colors = COLOR_SCHEMES[colorS])
        
        create_tag_image(tags, self.png,\
                         size=(960, 400),\
                         background=(255, 255, 255, 255),\
                         layout= LAYOUT_HORIZONTAL,\
                         fontname='Neuton')
        return True