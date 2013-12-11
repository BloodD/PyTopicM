# -*- coding: utf-8 -*-
# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#List view model
#Author: Dang Xiaobin
#Email:  dangxiaobin@gmail.com
#Date:   20/10/2012
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class TMListModel(QAbstractListModel):
    """
    List view class defination. showing the topics in list.
    """
    def __init__(self,tplist=[],parent=None):
        super(TMListModel,self).__init__(parent)
        self._data= tplist
        self.colors= self.randomColors()
        
    def rowCount(self,parent=QModelIndex()):
        return len(self._data)
   
    def flags(self, index):
        flag = super(TMListModel, self).flags(index)
        return flag | Qt.ItemIsEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable \
               | Qt.ItemIsEditable
    
    def data(self,index,role=Qt.DisplayRole):
        if not index.isValid() or \
           not 0<=index.row()< self.rowCount():
            return QVariant()
        
        row = index.row()
    
        color = self.colors.get(index.row() + 1, Qt.red)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(self._data[row])
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft))
        elif role == Qt.DecorationRole:    
            pixmap = QPixmap(16,16)
            pixmap.fill(color)
            return QVariant(pixmap)
        else:
            return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        """
        Set the data line.
        """
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()
    
        row = index.row()
        if role == Qt.EditRole:
            valueStr = value.toPyObject()
            
            if not valueStr == '':
                if not self._data[row] == valueStr:
                    self._data[row] = valueStr
                    return True
                else:
                    return False
        else:
            return False

    def randomColors(self):
        """
        Dummy function used for sample data generation, used by BarGraphModel
        """
        num=self.rowCount()
        colors = {}
        random.__all__
        random.choice('abcde')
        [colors.__setitem__(index + 1,random.choice(\
            (Qt.black, Qt.yellow, Qt.red, Qt.darkRed, Qt.green, Qt.darkGreen, \
             Qt.blue, Qt.darkBlue, Qt.cyan, Qt.darkCyan, Qt.magenta,\
             Qt.darkMagenta, Qt.darkYellow, Qt.gray,\
             Qt.darkGray, Qt.lightGray))) for index in range(num)]
        
        return colors

class TMListPaperModel(QAbstractListModel):
    """
    List view class defination. showing the topics in list.
    """
    def __init__(self,tplist=[],parent=None):
        super(TMListModel,self).__init__(parent)
        self._data= tplist
        self.colors= self.randomColors()
    def rowCount(self,parent=QModelIndex()):
        return len(self._data)

    def flags(self, index):
        flag = super(TMListModel, self).flags(index)
        return flag | Qt.ItemIsEnabled | Qt.ItemIsEnabled \
                    | Qt.ItemIsSelectable | Qt.ItemIsEditable
    
    def data(self,index,role=Qt.DisplayRole):
        if not index.isValid() or \
           not 0<=index.row()< self.rowCount():
            return QVariant()
        
        row = index.row()
    
        color = self.colors.get(index.row() + 1, Qt.red)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(self._data[row])
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft))
        else:
            return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        """
        Set the data line.
        """
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()
    
        row = index.row()
        if role == Qt.EditRole:
            valueStr = value.toPyObject()
            
            if not valueStr == '':
                if not self._data[row] == valueStr:
                    self._data[row] = valueStr
                    return True
                else:
                    return False
        else:
            return False

