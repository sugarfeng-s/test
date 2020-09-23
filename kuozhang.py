# -*- coding: utf-8 -*-
import sys
import os
import time
# import cv2
import traceback
# import numpy as np
import glob as gl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
from Data_aug import  Data_aug
#
# def numpy2QPixmap(img):
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     qimage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
#     pixmap = QPixmap(qimage)
#     return pixmap


class PredictionWorker(QThread):
    signal = pyqtSignal(int)

    def __init__(self, MainWidget):
        super(PredictionWorker, self).__init__()
        self.MainWidget = MainWidget
    def run(self):
        while 1:
            for i in range(100):
                self.MainWidget.pbar.setValue(i)
                time.sleep(0.1)
            self.MainWidget.pbar.setValue(0)
# class FrameWorker(QThread):
#     signal = pyqtSignal(int)
#
#     def __init__(self, upperWidget):
#         super(FrameWorker, self).__init__()
#         self.filename = None
#         self.FrameSpace = None
#         self.upperWidget = upperWidget
#
#     def setValue(self, FileName, FrameSpace):
#         self.filename = FileName
#         self.FrameSpace = FrameSpace
#
#     def run(self):
#         try:
#             self.upperWidget.LeftButton_1.setEnabled(False)  # 使选择按钮无效
#             cap = cv2.VideoCapture(self.filename)
#             Frame = 0
#             while (True):
#                 Frame = Frame + 1
#                 res, image = cap.read()
#                 if (not res) or (len(self.upperWidget.FrameList) == 50):
#                     break
#                 if Frame % self.FrameSpace == 0:
#                     # self.upperWidget.pbar.setValue(int((Frame/self.FrameSpace)/50*100))#进度条展示
#                     self.signal.emit(int((Frame / self.FrameSpace) / 50 * 100))
#                     self.upperWidget.FrameList.append([Frame, image])
#             # self.upperWidget.addFrame2Table(self,self.upperWidget.FrameList)
#             for i in range(len(self.upperWidget.FrameList)):
#                 self.upperWidget.TableWidget.insertRow(i)
#                 item = QTableWidgetItem()
#                 item.setText(str(self.upperWidget.FrameList[i][0]))
#                 item.setTextAlignment(Qt.AlignCenter)
#                 self.upperWidget.TableWidget.setItem(i, 0, item)
#             self.upperWidget.TabWidget.addTab(self.upperWidget.Tab_2, qtawesome.icon('fa5s.video', color='black'),
#                                               '显示帧')
#             self.upperWidget.LeftButton_1.setEnabled(True)
#             self.upperWidget.LeftButton_2.setEnabled(True)
#             self.upperWidget.AddressShow.setText(self.filename)
#         except:
#             TabCount = self.upperWidget.TabWidget.count()
#             if TabCount > 0:
#                 for _ in range(TabCount):
#                     self.upperWidget.TabWidget.removeTab(0)
#                 for _ in range(self.upperWidget.TableWidget.rowCount()):
#                     self.upperWidget.TableWidget.removeRow(0)
#             self.upperWidget.FrameList.clear()


class RightLabel(QLabel):  # 用于展示图片用的Label类
    def __init__(self, upperWidget):
        super(RightLabel, self).__init__()
        self.upperWidget = upperWidget

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.upperWidget.RightText.clear()
        if self.upperWidget.resultList:
            for i in (range(len(self.upperWidget.resultList[0][1][0]))):  # 往细节展示中加入信息
                self.upperWidget.RightText.append(
                    'xmin:' + str(self.upperWidget.resultList[0][1][0][i][0]) + ' ' + 'xmax' + str(
                        self.upperWidget.resultList[0][1][0][i][2]))
                self.upperWidget.RightText.append(
                    'ymin:' + str(self.upperWidget.resultList[0][1][0][i][1]) + ' ' + 'ymax' + str(
                        self.upperWidget.resultList[0][1][0][i][3]))
                self.upperWidget.RightText.append('Label:' + str(self.upperWidget.resultList[0][1][1][i]))
                self.upperWidget.RightText.append('confidence:' + str(self.upperWidget.resultList[0][1][2][i]))
                self.upperWidget.RightText.append(' ')

            self.upperWidget.RightDock.show()
            self.upperWidget.ShowWidget = ShowWidget(upperWidget=self.upperWidget)
            # self.upperWidget.ShowWidget.setParent(self.upperWidget)
            self.upperWidget.ShowWidgetLayout = QGridLayout()
            self.upperWidget.ShowWidget.setLayout(self.upperWidget.ShowWidgetLayout)
            self.upperWidget.ShowWidget.setWindowOpacity(1)
            self.upperWidget.ShowWidget.setAttribute(Qt.WA_TranslucentBackground, True)
            self.upperWidget.ShowWidget.setWindowFlags(Qt.WindowCloseButtonHint)
            self.upperWidget.ShowWidget.setWindowTitle(self.upperWidget.FileName)
            icon = QIcon()
            icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
            self.upperWidget.ShowWidget.setWindowIcon(icon)
            pixmap = QPixmap(numpy2QPixmap(self.upperWidget.resultList[0][0]))
            self.upperWidget.ShowWidget.setFixedSize(pixmap.width(), pixmap.height())
            tmpLabel = QLabel()
            tmpLabel.setPixmap(pixmap)
            self.upperWidget.ShowWidgetLayout.addWidget(tmpLabel)
            self.upperWidget.ShowWidget.show()
        else:
            self.upperWidget.RightDock.show()
            self.upperWidget.ShowWidget = ShowWidget(upperWidget=self.upperWidget)
            # self.upperWidget.ShowWidget.setParent(self.upperWidget)
            self.upperWidget.ShowWidgetLayout = QGridLayout()
            self.upperWidget.ShowWidget.setLayout(self.upperWidget.ShowWidgetLayout)
            self.upperWidget.ShowWidget.setWindowOpacity(1)
            self.upperWidget.ShowWidget.setAttribute(Qt.WA_TranslucentBackground, True)
            self.upperWidget.ShowWidget.setWindowFlags(Qt.WindowCloseButtonHint)
            self.upperWidget.ShowWidget.setWindowTitle(self.upperWidget.FileName)
            icon = QIcon()
            icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
            self.upperWidget.ShowWidget.setWindowIcon(icon)
            pixmap = QPixmap(self.upperWidget.FileName)
            self.upperWidget.ShowWidget.setFixedSize(pixmap.width(), pixmap.height())
            tmpLabel = QLabel()
            tmpLabel.setPixmap(pixmap)
            self.upperWidget.ShowWidgetLayout.addWidget(tmpLabel)
            self.upperWidget.ShowWidget.show()


class ShowWidget(QDialog):
    def __init__(self, upperWidget):
        super(ShowWidget, self).__init__()
        self.upperWidget = upperWidget

    def closeEvent(self, QCloseEvent):
        self.upperWidget.RightText.clear()
        self.upperWidget.RightDock.hide()


class TableWidget(QTableWidget):
    def __init__(self, upperWidget):
        super(TableWidget, self).__init__()
        self.upperWidget = upperWidget

    def enterEvent(self, QMouseEvent):
        self.setMouseTracking(True)

    def leaveEvent(self, QMouseEvent):
        # self.upperWidget.LeftText_1.setText("类别:")
        # self.upperWidget.LeftText_2.setText("置信度:")
        # self.upperWidget.LeftText_3.setText("耗时:")
        self.setMouseTracking(False)

    def mouseMoveEvent(self, QMouseEvent):
        # self.upperWidget.LeftText_1.setText("类别:")
        # self.upperWidget.LeftText_2.setText("置信度:")
        # # self.upperWidget.LeftText_3.setText("耗时:")
        Item = {}
        point = QPoint(QMouseEvent.pos())
        currentItem = self.itemAt(point)
        if currentItem is not None:
            rowNumber = currentItem.row()
            # print(rowNumber)
            # print(self.item(rowNumber,0).text())
            for i in range(3):
                if self.item(rowNumber, i + 1) is not None:
                    Item[i + 1] = self.item(rowNumber, i + 1)
                    # print(self.itemAt(rowNumber,i+1).text())
        if Item:
            self.upperWidget.LeftText_1.setText("类别:" + Item[1].text())
            # self.upperWidget.LeftText_2.setText("置信度:"+Item[2].text())
            # self.upperWidget.LeftText_3.setText("耗时:" + Item[3].text())


class Aug(QMainWindow):  # 主窗口类
    signal = pyqtSignal()

    def __init__(self):
        super(Aug, self).__init__()
        self.setWindowTitle("Data Augmented Module")
        # self.setWindowIcon(qtawesome.icon('fa5s.bus', color='black'))
        self.setFixedSize(1000, 700)
        self.move(400, 200)

        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground, False)  # 设置窗口背景透明
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口取消边框

        self.FileName = None  # 文件名变量
        self.FileDir = None  # 目录名变量
        self.isOneFile = True  # 单个文件或是一组文件
        self.isPic = True  # 是否是图片
        self.FrameList = list()  # 用于存放帧
        self.PicPath = {}  # 用于存放图片地址列表

        self.ShowWidget = ShowWidget(upperWidget=self)  # 展示图像用的窗口
        self.resultList = list()  # 预测结果存储位置
        self.PredictionWorker = PredictionWorker(self)
        # self.FrameWorker = FrameWorker(self)

        self.init_UI()

    def init_UI(self):
        # 设置窗口主布局
        Main_Ui = QWidget()
        self.setCentralWidget(Main_Ui)
        self.MainLayout = QGridLayout()
        Main_Ui.setLayout(self.MainLayout)
        self.init_LeftUI()  # 初始化左侧布局
        self.init_RightUI()  # 初始化右侧布局

        self.LeftButton_1.clicked.connect(self.selectTarget)  # 关联目标选择按钮到selectTarget函数
        self.LeftButton_2.clicked.connect(self.predict)  # 关联开始按钮到predict函数
        self.LeftButton_4.clicked.connect(self.save)  # 关联保存按钮到save函数
        self.LeftButton_3.clicked.connect(self.closeALL)  # 关联推出按钮到程序推出函数
        self.TableWidget.cellDoubleClicked.connect(self.TableDoubleClick)
        # self.PredictionWorker.finished.connect(self.workerFinished)
        # self.FrameWorker.finished.connect(self.workerFinished)
        self.PredictionWorker.signal.connect(self.pbarProcess)
        # self.FrameWorker.signal.connect(self.pbarProcess)

    def init_LeftUI(self):
        # 设置窗口左侧布局
        self.LeftWidget = QWidget()
        self.LeftLayout = QGridLayout()
        self.LeftWidget.setLayout(self.LeftLayout)

        # 设置左侧窗口分块
        self.Frame1 = QFrame()
        self.Frame2 = QFrame()
        self.Frame1.setFrameShape(QFrame.StyledPanel)
        self.Frame2.setFrameShape(QFrame.StyledPanel)
        self.Frame1.setFrameShadow(QFrame.Sunken)
        self.Frame2.setFrameShadow(QFrame.Sunken)
        self.Frame1Layout = QGridLayout()
        self.Frame2Layout = QGridLayout()
        self.Frame1.setLayout(self.Frame1Layout)
        self.Frame2.setLayout(self.Frame2Layout)

        # 设置左侧标签
        self.LeftLabel_1 = QLabel("医学数据扩张:")
        self.LeftLabel_11 = QLabel("数据扩张方法：")
        self.LeftLabel_111 = QLabel("数据扩张量：")
        self.LeftLabel_2 = QLabel("扩张结果:")

        # 设置左侧上半部分
        self.PicType = QRadioButton("图片文件")
        # self.VideoType = QRadioButton("视频文件")
        self.DirType = QRadioButton("图片目录")
        # self.group_parse =  QButtonGroup()
        self.DateType1 = QCheckBox("平移")
        # self.VideoType = QRadioButton("视频文件")
        self.DateType2 = QCheckBox("旋转")
        self.DateType3 = QCheckBox("错切")
        self.DateType4 = QCheckBox("缩放")
        self.DateType5 = QCheckBox("扭曲")
        self.DateType6 = QCheckBox("投影")
        # self.group_parse.addButton(self.DateType1,id=1)
        # self.group_parse.addButton(self.DateType2,id=2)
        # self.group_parse.addButton(self.DateType3,id=3)
        # self.group_parse.addButton(self.DateType4,id=4)
        # self.group_parse.addButton(self.DateType5,id=5)
        # self.group_parse.addButton(self.DateType6,id=6)

        self.PicType.setChecked(True)
        self.AddressShow = QLineEdit("")
        self.AddressShow.setReadOnly(True)
        self.AddressShow1 = QLineEdit("")
        self.AddressShow1.setReadOnly(True)
        self.numberinput = QLineEdit("")
        self.LeftButton_1 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择目标")
        self.LeftButton_2 = QPushButton(qtawesome.icon('fa.sellsy', color='black'), "运行")
        self.LeftButton_4 = QPushButton(qtawesome.icon('fa.file', color='black'), "保存")
        self.LeftButton_2.setEnabled(False)
        # self.LeftButton_3.setEnabled(False)
        self.pbar = QProgressBar()  # 进度条
        self.pbar.setTextVisible(False)
        # 设置左侧下半部分
        self.TextFrame1 = QFrame()
        self.TextFrame2 = QFrame()
        self.TextFrame3 = QFrame()
        self.TextFrame1Layout = QGridLayout()
        self.TextFrame2Layout = QGridLayout()
        self.TextFrame3Layout = QGridLayout()
        self.TextFrame1.setFrameShape(QFrame.Panel)
        self.TextFrame2.setFrameShape(QFrame.Panel)
        # self.TextFrame3.setFrameShape(QFrame.Panel)
        self.TextFrame1.setFrameShadow(QFrame.Raised)
        self.TextFrame2.setFrameShadow(QFrame.Raised)
        # self.TextFrame3.setFrameShadow(QFrame.Raised)
        self.TextFrame1.setLineWidth(1)
        self.TextFrame2.setLineWidth(1)
        self.TextFrame3.setLineWidth(1)
        self.TextFrame1.setLayout(self.TextFrame1Layout)
        self.TextFrame2.setLayout(self.TextFrame2Layout)
        # self.TextFrame3.setLayout(self.TextFrame3Layout)
        self.LeftText_1 = QLabel("总张数")
        self.LeftText_2 = QLabel("总耗时")
        # self.LeftText_3 = QLabel("平均耗时")
        self.TextFrame1Layout.addWidget(self.LeftText_1)
        self.TextFrame2Layout.addWidget(self.LeftText_2)
        # self.TextFrame3Layout.addWidget(self.LeftText_3)
        self.LeftButton_3 = QPushButton("退出")

        # 添加所有控件至左侧布局
        self.Frame1Layout.addWidget(self.LeftLabel_1, 1, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftLabel_11, 3, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftLabel_111, 6, 0, 2, 2)
        self.Frame1Layout.addWidget(self.numberinput, 6, 1, 2, 1)
        self.Frame1Layout.addWidget(self.PicType, 2, 0, 2, 1)
        # self.Frame1Layout.addWidget(self.VideoType, 2, 1, 2, 1)
        self.Frame1Layout.addWidget(self.DirType, 2, 2, 2, 1)
        self.Frame1Layout.addWidget(self.DateType1, 4, 0, 2, 1)
        self.Frame1Layout.addWidget(self.DateType2, 4, 1, 2, 1)
        self.Frame1Layout.addWidget(self.DateType3, 4, 2, 2, 1)
        self.Frame1Layout.addWidget(self.DateType4, 5, 0, 2, 1)
        self.Frame1Layout.addWidget(self.DateType5, 5, 1, 2, 1)
        self.Frame1Layout.addWidget(self.DateType6, 5, 2, 2, 1)
        self.Frame1Layout.addWidget(self.AddressShow, 8, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_1, 8, 2, 2, 1)
        self.Frame1Layout.addWidget(self.AddressShow1, 10, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_4, 10, 2, 2, 1)
        self.Frame1Layout.addWidget(self.LeftButton_2, 11, 2, 5, 2)
        self.Frame1Layout.addWidget(self.pbar, 11, 0, 5, 2)
        # self.Frame1Layout.addWidget(self.pbtn, 7, 2, 5, 2)
        self.Frame2Layout.addWidget(self.LeftLabel_2, 0, 0, 2, 1)
        self.Frame2Layout.addWidget(self.TextFrame1, 2, 0, 1, 1)
        self.Frame2Layout.addWidget(self.TextFrame2, 3, 0, 1, 1)
        self.Frame2Layout.addWidget(self.TextFrame3, 4, 0, 1, 1)
        self.Frame2Layout.addWidget(self.LeftButton_3, 5, 0, 2, 2)

        self.LeftLayout.addWidget(self.Frame1, 0, 0, 5, 2)
        self.LeftLayout.addWidget(self.Frame2, 7, 0, 5, 2)
        # 添加至窗口主布局
        self.MainLayout.addWidget(self.LeftWidget, 0, 0, 25, 3)

    def init_RightUI(self):
        # 设置窗口右侧布局
        self.RightWidget = QWidget()
        self.RightLayout = QGridLayout()
        self.RightWidget.setLayout(self.RightLayout)

        # 设置图片组所用的表控件
        self.RightLabel_1 = RightLabel(upperWidget=self)  # 特殊定义的展示用Label类
        self.RightLabel_1.setText('')  # 将Label类的文本展示归为空
        # self.TableWidget = QTableWidget(0,4)
        self.TableWidget = TableWidget(self)
        self.TableWidget.setRowCount(0)
        self.TableWidget.setColumnCount(1)
        self.TableWidget.setHorizontalHeaderLabels(['文件名'])
        self.TableWidget.horizontalHeader().setStretchLastSection(True)
        self.TableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设定表格不可编辑

        # 设置用于展示的空控件
        self.TabWidget = QTabWidget()

        # 设置用于展示表格的空控件，并暂时使其不加入窗口布局
        self.Tab_1 = QWidget()
        self.Tab_2 = QWidget()
        self.Tab_1Layout = QGridLayout()
        self.Tab_2Layout = QGridLayout()
        self.Tab_1.setLayout(self.Tab_1Layout)
        self.Tab_2.setLayout(self.Tab_2Layout)
        self.Tab_1Layout.addWidget(self.RightLabel_1)
        self.Tab_2Layout.addWidget(self.TableWidget)

        # 设置堆叠控件以展示详细的信息
        self.RightDock = QDockWidget()
        self.RightDock.setFixedSize(300, 200)
        self.RightDock.move(1100, 300)
        # self.RightDock.setWindowFlags(Qt.FramelessWindowHint|Qt.CustomizeWindowHint )
        self.RightDock.setAllowedAreas(Qt.NoDockWidgetArea)
        self.RightDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.RightDock.setFloating(True)
        self.RightDock.setWindowTitle("详细信息")
        self.RightText = QTextEdit()
        self.RightText.setReadOnly(True)
        self.RightText.setText("")
        self.RightDock.setWidget(self.RightText)
        self.RightDock.raise_()
        self.RightDock.hide()
        # self.addDockWidget(Qt.NoDockWidgetArea,self.RightDock)

        # 将右侧控件加入布局
        self.RightLayout.addWidget(self.TabWidget)

        self.MainLayout.addWidget(self.RightWidget, 0, 3, 25, 5)

    def selectTarget(self):
        print("xxxxxxxxxx")
        # 判断选择的目标类型，并执行相应函数
        if (self.PicType.isChecked()):
            fname, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image files(*.jpg *.png)')
            # print(fname)
            if fname:
                self.FileName = fname
                self.FileDir = None
                self.isOneFile = True
                self.isPic = True
                self.PicPath = {}
                self.AddressShow.setText(fname)
        elif (self.DirType.isChecked()):
            dir = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
            if dir:
                self.isOneFile = False
                files = os.listdir(dir)
                files = [dir + '/' + x for x in files]
                self.FileDir = files
                self.FileDir = dir
                self.FileName = None
                self.isPic = False
                self.AddressShow.setText(dir)

    def addPic2Table(self, files):
        self.PicPath = {}
        for d, filename in enumerate(files):
            if os.path.isdir(filename):
                continue
            if filename.split('.')[-1] != 'jpg' and filename.split('.')[-1] != 'png':
                continue
            self.TableWidget.insertRow(d)
            item = QTableWidgetItem()
            self.PicPath[d] = filename
            item.setText(filename.split('/')[-1])
            item.setTextAlignment(Qt.AlignCenter)
            self.TableWidget.setItem(d, 0, item)

    def ShowTable(self, files):
        TabCount = self.TabWidget.count()
        if TabCount > 0:
            for _ in range(TabCount):
                self.TabWidget.removeTab(0)
        for _ in range(self.TableWidget.rowCount()):
            self.TableWidget.removeRow(0)
        self.addPic2Table(files)
        icon = QIcon()
        icon.addPixmap(QPixmap(".//icon//table.png"), QIcon.Normal, QIcon.Off)
        self.TabWidget.addTab(self.Tab_2, icon, '显示表格')
    def predict(self):
        flag=0
        aug_method_list = []
        if self.PicType.isChecked() or self.DirType.isChecked():
            # print(self.AddressShow.text())
            if not self.numberinput.text()=="":
                if not self.AddressShow.text()=="":
                    if not self.AddressShow1.text()=="":
                        if self.DateType1.isChecked():
                            aug_method_list.append('transform')
                        if self.DateType2.isChecked():
                            aug_method_list.append('rotate')
                        if self.DateType3.isChecked():
                            aug_method_list.append('shear')
                        if self.DateType4.isChecked():
                            aug_method_list.append('zoom')
                        if self.DateType5.isChecked():
                            aug_method_list.append('warp')
                        if len(aug_method_list):
                            flag=1
        if flag:
            print(aug_method_list)
            start = time.time()
            self.pbar.setValue(0)
            self.PredictionWorker.start()
            self.aug_server = Data_aug(aug_method_list,self.numberinput.text(),self.FileDir,
                                           self.savePath)
            self.aug_server.select_aug()
            self.PredictionWorker.terminate()
            self.pbar.setValue(100)
            all = time.time() - start
            filenum = len(gl.glob(self.savePath + '/*'))
            print(all)
            print(filenum)
            files = os.listdir(self.savePath)
            files = [self.savePath + '/' + x for x in files]
            self.ShowTable(files)
            self.LeftText_1.setText("总耗时    " + str(all)[:6])
            self.LeftText_2.setText("总张数    " + str(filenum))
            # print(id)
        else:
            QMessageBox.information(self, '通知', 'complete your param')

    def save(self):
        dir = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
        # print(dir)
        self.AddressShow1.setText(dir)
        self.LeftButton_2.setEnabled(True)
        self.savePath = dir

    def pbarProcess(self, number):
        self.pbar.setValue(number)

    def workerFinished(self):
        try:
            if not (self.FrameList or self.resultList):
                QMessageBox.information(self, '通知', '有一些错误发生了，请重新尝试')
                self.PredictionWorker.quit()
                self.PredictionWorker.wait()
                self.LeftButton_2.setText('运行')
                self.pbar.setValue(0)
                self.pbtn.setEnabled(True)
                self.LeftButton_1.setEnabled(True)
                self.ShowWidget.close()
            else:
                if self.resultList:
                    for i in range(len(self.resultList)):
                        item_Label = QTableWidgetItem()
                        item_Time = QTableWidgetItem()
                        item_Label.setText(self.resultList[i][2])
                        item_Time.setText(str(self.resultList[i][3]))
                        item_Label.setTextAlignment(Qt.AlignCenter)
                        item_Time.setTextAlignment(Qt.AlignCenter)
                        self.TableWidget.setItem(i, 1, item_Label)
                        self.TableWidget.setItem(i, 3, item_Time)
                QMessageBox.information(self, '通知', '任务完成')  # 提帧完成的提醒
                self.PredictionWorker.quit()
                self.PredictionWorker.wait()
                self.LeftButton_2.setText('运行')
                self.pbar.setValue(0)
                self.pbtn.setEnabled(True)
                self.LeftButton_1.setEnabled(True)
        except:
            pass
            # exType,exValue,exTrace = sys.exc_info()
            # print(exType,exValue,sep = '\n')
            # for trace in traceback.extract_tb(exTrace):
            #    print(trace)

    def TableDoubleClick(self, r, c):
        self.RightText.clear()
        if self.resultList:  # 有预测结果的分路
            if self.FileName is None:
                for i in (range(len(self.resultList[r][1][0]))):  # 往细节展示中加入信息
                    self.RightText.append('xmin:' + str(self.resultList[r][1][0][i][0]) + ' ' + 'xmax' + str(
                        self.resultList[r][1][0][i][2]))
                    self.RightText.append('ymin:' + str(self.resultList[r][1][0][i][1]) + ' ' + 'ymax' + str(
                        self.resultList[r][1][0][i][3]))
                    self.RightText.append('Label:' + str(self.resultList[r][1][1][i]))
                    self.RightText.append('confidence:' + str(self.resultList[r][1][2][i]))
                    self.RightText.append(' ')

                self.RightDock.show()
                self.ShowWidget = ShowWidget(upperWidget=self)
                self.ShowWidgetLayout = QGridLayout()
                self.ShowWidget.setLayout(self.ShowWidgetLayout)
                self.ShowWidget.setWindowOpacity(1)
                self.ShowWidget.setAttribute(Qt.WA_TranslucentBackground, True)
                self.ShowWidget.setWindowFlags(Qt.WindowCloseButtonHint)
                self.ShowWidget.setWindowTitle(self.PicPath[r])
                icon = QIcon()
                icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
                self.ShowWidget.setWindowIcon(icon)
                pixmap = QPixmap(numpy2QPixmap(self.resultList[r][0]))
                self.ShowWidget.setFixedSize(pixmap.width(), pixmap.height())
                tmpLabel = QLabel()
                tmpLabel.setPixmap(pixmap)
                self.ShowWidgetLayout.addWidget(tmpLabel)
                self.ShowWidget.show()
            else:
                for i in (range(len(self.resultList[r][1][0]))):  # 往细节展示中加入信息
                    self.RightText.append('xmin:' + str(self.resultList[r][1][0][i][0]) + ' ' + 'xmax' + str(
                        self.resultList[r][1][0][i][2]))
                    self.RightText.append('ymin:' + str(self.resultList[r][1][0][i][1]) + ' ' + 'ymax' + str(
                        self.resultList[r][1][0][i][3]))
                    self.RightText.append('Label:' + str(self.resultList[r][1][1][i]))
                    self.RightText.append('confidence:' + str(self.resultList[r][1][2][i]))
                    self.RightText.append(' ')

                self.RightDock.show()
                self.ShowWidget = ShowWidget(upperWidget=self)
                self.ShowWidgetLayout = QGridLayout()
                self.ShowWidget.setLayout(self.ShowWidgetLayout)
                self.ShowWidget.setWindowOpacity(1)
                self.ShowWidget.setAttribute(Qt.WA_TranslucentBackground, True)
                self.ShowWidget.setWindowFlags(Qt.WindowCloseButtonHint)
                self.ShowWidget.setWindowTitle(str(self.FrameList[r][0]))
                icon = QIcon()
                icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
                self.ShowWidget.setWindowIcon(icon)
                pixmap = QPixmap(numpy2QPixmap(self.resultList[r][0]))
                self.ShowWidget.setFixedSize(pixmap.width(), pixmap.height())
                tmpLabel = QLabel()
                tmpLabel.setPixmap(pixmap)
                self.ShowWidgetLayout.addWidget(tmpLabel)
                self.ShowWidget.show()
        else:  # 无预测结果的分路
            self.RightDock.show()
            if self.FileName is None:
                self.ShowWidget = ShowWidget(upperWidget=self)
                self.ShowWidgetLayout = QGridLayout()
                self.ShowWidget.setLayout(self.ShowWidgetLayout)
                self.ShowWidget.setWindowOpacity(1)
                self.ShowWidget.setAttribute(Qt.WA_TranslucentBackground, True)
                self.ShowWidget.setWindowFlags(Qt.WindowCloseButtonHint)
                self.ShowWidget.setWindowTitle(self.PicPath[r])
                icon = QIcon()
                icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
                self.ShowWidget.setWindowIcon(icon)
                pixmap = QPixmap(self.PicPath[r])
                self.ShowWidget.setFixedSize(pixmap.width(), pixmap.height())
                tmpLabel = QLabel()
                tmpLabel.setPixmap(pixmap)
                self.ShowWidgetLayout.addWidget(tmpLabel)
                self.ShowWidget.show()
            else:
                self.ShowWidget = ShowWidget(upperWidget=self)
                self.ShowWidgetLayout = QGridLayout()
                self.ShowWidget.setLayout(self.ShowWidgetLayout)
                self.ShowWidget.setWindowOpacity(1)
                self.ShowWidget.setAttribute(Qt.WA_TranslucentBackground, True)
                self.ShowWidget.setWindowFlags(Qt.WindowCloseButtonHint)
                self.ShowWidget.setWindowTitle(str(self.FrameList[r][0]))
                icon = QIcon()
                icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
                self.ShowWidget.setWindowIcon(icon)
                pixmap = QPixmap(numpy2QPixmap(self.FrameList[r][1]))
                self.ShowWidget.setFixedSize(pixmap.width(), pixmap.height())
                tmpLabel = QLabel()
                tmpLabel.setPixmap(pixmap)
                self.ShowWidgetLayout.addWidget(tmpLabel)
                self.ShowWidget.show()

    def closeALL(self):
        self.ShowWidget.close()
        self.RightDock.close()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainUI()
    MainWindow.show()
    sys.exit(app.exec_())