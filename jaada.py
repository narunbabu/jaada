from PyQt5.QtCore import QDate, QFile, Qt, QTextStream,QSize
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PyQt5.QtGui import QPixmap,QImage,QPainter,QColor,QBrush,QMouseEvent,QPen
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget,QWidgetItem,
        QScrollArea,QVBoxLayout,QHBoxLayout,QToolBar,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit,QLabel,QWidget)
# import pyqtgraph as pg
import numpy as np
import os
from PIL.ImageQt import ImageQt
from scipy.misc.pilutil import toimage
import dockwidgets_rc
import segyio


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100,100, 800,500)
        self.set_toolbar()


        self.centralWidget = QWidget()
        layout = QHBoxLayout(self.centralWidget)
        
        self.scrollArea = QScrollArea(self)

        self.gwidget=GraphicsWidget()

        self.scrollArea.setWidget(self.gwidget)
        layout.addWidget(self.scrollArea)

        self.setCentralWidget(self.centralWidget)
        self.createDockWindows()
        

        self.setWindowTitle("Dock Widgets")

        # self.newLetter()
    def set_toolbar(self):
        tb = QToolBar('Seismic')
        tb.setIconSize(QSize(25, 25))
        self.addToolBar(tb)
		# QIcon(os.path.join('ves_imgs', 'invert-tool.png')
        prev = QAction(QIcon(os.path.join('images', 'arr_b_thin.png')),"prev",self)
        next = QAction(QIcon(os.path.join('images', 'arr_f_thin.png')),"next",self)
        pause= QAction(QIcon(os.path.join('images', '17270.png')),"pause",self)
        
        tb.addAction(prev)
        tb.addAction(pause)
        tb.addAction(next)
            
        # open = QAction(QIcon("open.bmp"),"open",self)
        # tb.addAction(open)
        # save = QAction(QIcon("save.bmp"),"save",self)
        # tb.addAction(save)
        tb.actionTriggered[QAction].connect(self.toolbtnpressed)
        # self.setLayout(layout)
        # self.setWindowTitle("toolbar demo")
		
    def toolbtnpressed(self,a):
        print ("pressed tool button is",a.text())
        if(a.text()=='next'):            
            self.gwidget.presentline += self.gwidget.linestep
        elif(a.text()=='prev'):            
            self.gwidget.presentline -= self.gwidget.linestep
        self.gwidget.pixmap=self.gwidget.getnextSeispixmap()
        self.gwidget.update()
        # self.gwidget.qp.drawPixmap(0,0,self.gwidget.pixmap)
        # self.gwidget.paintEvent(self.gwidget, event)

    def createDockWindows(self):
        dock = QDockWidget("Customers", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems(('Hello','How are you'))
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Paragraphs", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems(('Good morning','Hope you are doing well'))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        # self.customerList.currentTextChanged.connect(self.insertCustomer)
        # self.paragraphsList.currentTextChanged.connect(self.addParagraph)

class GraphicsWidget(QWidget):

    def __init__(self):
        super(GraphicsWidget, self).__init__()
        self.initUI()
        # self.pixmap=QPixmap("screenshot-camera.jpg")
        self.pixmap=self.getnextSeispixmap()
		
    def initUI(self):
        self.text = "hello world"
        self.setGeometry(0,0, 400,400)
        self.setWindowTitle('Draw Demo')
        self.center = None
        self.horx=[]
        self.hory=[]
        self.get_sismic()
    #   self.show()
    def mousePressEvent(self, event):
        self.horx.append(event.pos().x())
        self.hory.append(event.pos().y())
        print('event',event.pos().x(),event.pos().y())
        if event.button() == QtCore.Qt.LeftButton:
            event = QMouseEvent(QtCore.QEvent.MouseButtonRelease, event.pos(), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            # if (abs(event.pos().x())<=self.rect().width()): 
            self.center = event.pos()
            self.update()
            QtWidgets.QWidget.mousePressEvent(self, event)
    def paintEvent(self, event):
        self.qp = QPainter()
        self.qp.begin(self)
        # qp.setPen(QColor(Qt.red))
        # qp.setFont(QFont('Arial', 20))
            
        # qp.drawText(10,50, "hello Python")
        # qp.setPen(QColor(Qt.blue))
        # qp.drawLine(10,100,100,100)
        # qp.drawRect(10,150,150,100)
            
        # qp.setPen(QColor(Qt.yellow))
        # qp.drawEllipse(100,50,100,50)
        
        self.qp.drawPixmap(0,0,self.pixmap)
        if (self.center):
        #     qp.drawEllipse(self.center, 24, 24)  
        # qp.fillRect(200,175,150,100,QBrush(Qt.SolidPattern))
            self.drawPoints( self.qp)
        self.qp.end()
        self.resize(self.pixmap.width(),self.pixmap.height())
    def get_sismic(self):
        folder=r'D:\Arun\Blade_project\Seismic data\\'
        filename = folder+'RTM_uncalibrated_DTC.sgy'
        self.src=segyio.open(filename)
        # with segyio.open(filename) as src:
        self.ilines = self.src.ilines[:500]
        self.xlines = self.src.xlines[:500]
        self.presentline=0
        self.getnextSeispixmap()
        self.linestep=10
    def getnextSeispixmap(self):
        
        print(self.presentline,self.ilines[self.presentline])
        self.scaleFactor_x=4
        self.scaleFactor_y=0.3
                
        # image_data =  np.random.randint(255, size=(200, 400))
        
        
        image_data = self.src.iline[self.ilines[self.presentline]]
        print(np.sum(image_data))
        pilImage = toimage(image_data.T)
        qtImage = ImageQt(pilImage)
        # print(image_data)
        image = QImage(qtImage)
        image = image.scaled(self.scaleFactor_x*image.width(), self.scaleFactor_y*image.height())
        return QPixmap.fromImage(image)
    def drawPoints(self,qp):          
        
        pen=QPen(Qt.green, 3, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin);
        qp.setPen(pen)
        # pen.setStyle(Qt.DashDotLine);
        # pen.setWidth(3);
        # pen.setBrush(Qt.green);
        # pen.setCapStyle(Qt.RoundCap);
        # pen.setJoinStyle(Qt.RoundJoin);
        size = self.size()
        
        for x,y in zip(self.horx,self.hory):
            # x = np.random.randint(1, size.width()-1)
            # y = np.random.randint(1, size.height()-1)
            print(x,y,end='; ')
            qp.drawPoint(x, y)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
