# -*- coding: utf-8 -*-
# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#This code is GUI tool for topic modeling and paper recommandation task.
#Author: Dang Xiaobin
#Email:  dangxiaobin@gmail.com
#Date:   20/10/2012
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
import sys
import os
from time import sleep, ctime
from src.main import TMMainWidget
from PyQt4.QtGui import QApplication,QSplashScreen,QPixmap

def main():
    """
    Main runtine to run software.
    """
    workpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
    #print workpath
    workpath = workpath.split('\\')
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
