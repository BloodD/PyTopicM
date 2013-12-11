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
import re
import operator

# third party packages
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class TMTableModel(QAbstractTableModel): 
    """
    Table view class defination. showing the topics along table columns.
    """
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
        
        
    def index(self, row, column, parent):
        data = self.arraydata[row][column]
        return self.createIndex(row, column, data)
    
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0])
    
    def flags(self, index):
        flag = super(TMTableModel, self).flags(index)
        return flag | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled |\
               Qt.ItemIsEditable
    
    def data(self, index, role):
        if not index.isValid(): 
            return QVariant() 
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return QVariant(self.arraydata[index.row()][index.column()])
    
    def setData(self, index, value, role):
        """
        Set data cell
        """
        if not index.isValid():
            return QVariant()   
        if role == Qt.EditRole:
            valueStr = value.toPyObject()
    
            if not valueStr == '':
                if not self.arraydata[index.row()][index.column()] == valueStr:
                    self.arraydata[index.row()][index.column()] = valueStr
                    return True
                else:
                    return False
        else:
            return False
    
    def headerData(self, col, orientation, role):
        """
        Set the table header.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """
        Sort table content by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata,
                                key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

