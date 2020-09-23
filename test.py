import sys
import os
import time
# import cv2
import traceback
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
import test


# def numpy2QPixmap(img):
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     qimage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
#     pixmap = QPixmap(qimage)
#     return pixmap


# class PredictionWorker(QThread):
#     signal = pyqtSignal(int)
#
#     def __init__(self, MainWidget):
#         super(PredictionWorker, self).__init__()
#         self.MainWidget = MainWidget
#         self.Detector = test.Detector()
#
#     def run(self):
#         try:
#             if self.MainWidget.isPic:
#                 RunTime = time.time()
#                 resultPic, resultBoxInfo, label = self.Detector.detection(self.MainWidget.FileName)
#                 RunTime = time.time() - RunTime
#                 self.MainWidget.resultList.append([resultPic, resultBoxInfo, label, RunTime,
#                                                    self.MainWidget.FileName.split('/')[
#                                                        -1]])  # [图像,[[bndbox],[label],[scores]]]
#                 self.MainWidget.LeftText_1.setText("类别:" + label)
#                 self.MainWidget.LeftText_3.setText("耗时:" + str(RunTime) + 's')
#             else:
#                 if self.MainWidget.FileName is None:
#                     tempList = list()
#                     for i in range(len(self.MainWidget.PicPath)):
#                         self.signal.emit(int((i + 1) / len(self.MainWidget.PicPath) * 100))
#                         RunTime = time.time()
#                         resultPic, resultBoxInfo, label = self.Detector.detection(self.MainWidget.PicPath[i])
#                         RunTime = time.time() - RunTime
#                         tempList.append(
#                             [resultPic, resultBoxInfo, label, RunTime, self.MainWidget.PicPath[i].split('/')[-1]])
#                     self.MainWidget.resultList = tempList
#                 else:  # 视频的处理分路
#                     tempList = list()
#                     for i in range(len(self.MainWidget.FrameList)):
#                         self.signal.emit(int((i + 1) / len(self.MainWidget.FrameList) * 100))
#                         RunTime = time.time()
#                         resultPic, resultBoxInfo, label = self.Detector.detection(self.MainWidget.FrameList[i][1])
#                         RunTime = time.time() - RunTime
#                         tempList.append(
#                             [resultPic, resultBoxInfo, label, RunTime, self.MainWidget.FrameList[i][0] + '.jpg'])
#                     self.MainWidget.resultList = tempList
#         except:
#             self.MainWidget.resultList.clear()
#
#
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
        self.upperWidget.LeftText_1.setText("类别:")
        self.upperWidget.LeftText_2.setText("置信度:")
        # self.upperWidget.LeftText_3.setText("耗时:")
        self.setMouseTracking(False)

    def mouseMoveEvent(self, QMouseEvent):
        self.upperWidget.LeftText_1.setText("类别:")
        self.upperWidget.LeftText_2.setText("置信度:")
        # self.upperWidget.LeftText_3.setText("耗时:")
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


class Test(QMainWindow):  # 主窗口类
    signal = pyqtSignal()

    def __init__(self):
        super(Test, self).__init__()
        self.setWindowTitle("Network Eval Module")
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
        # self.PredictionWorker = PredictionWorker(self)
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
        self.pbtn.clicked.connect(self.save)  # 关联保存按钮到save函数
        self.LeftButton_3.clicked.connect(self.closeALL)  # 关联推出按钮到程序推出函数
        self.TableWidget.cellDoubleClicked.connect(self.TableDoubleClick)
        # self.PredictionWorker.finished.connect(self.workerFinished)
        # self.FrameWorker.finished.connect(self.workerFinished)
        # self.PredictionWorker.signal.connect(self.pbarProcess)
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
        self.LeftLabel_1 = QLabel("获取数据结果:")
        self.LeftLabel_11 = QLabel("数据评价指标：")
        # self.LeftLabel_111 = QLabel("：")
        self.LeftLabel_2 = QLabel("日志输出:")

        # 设置左侧上半部分
        self.PicType = QRadioButton("图片文件")
        # self.VideoType = QRadioButton("视频文件")
        self.DirType = QRadioButton("图片目录")
        self.DateType1 = QCheckBox("Sensitive")
        # self.VideoType = QRadioButton("视频文件")
        self.DateType2 = QCheckBox("Specificity")
        self.DateType3 = QCheckBox("Accuracy")
        self.DateType4 = QCheckBox("AUC")
        self.DateType5 = QCheckBox("Dice")
        self.DateType6 = QCheckBox("Jaccard")
        self.PicType.setChecked(True)
        self.AddressShow = QLineEdit("")
        self.AddressShow.setReadOnly(False)
        self.AddressShow1 = QLineEdit("")
        self.AddressShow1.setReadOnly(False)
        self.numberinput = QLineEdit("")
        self.AddressShow4 = QLineEdit("")
        self.AddressShow7 = QLineEdit("")
        self.AddressShow5 = QLineEdit("")
        self.AddressShow6 = QLineEdit("")
        self.LeftButton_1 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择数据")
        self.AddressShow5.setReadOnly(False)
        self.LeftButton_5 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择网络配置")
        self.LeftButton_6 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择网络权重")
        self.AddressShow6.setReadOnly(False)
        self.LeftButton_7 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择基础网络文件")
        self.AddressShow7.setReadOnly(False)

        self.LeftButton_2 = QPushButton(qtawesome.icon('fa.sellsy', color='black'), "运行")
        self.LeftButton_4 = QPushButton(qtawesome.icon('fa.file', color='black'), "保存")
        self.AddressShow4.setReadOnly(False)
        self.TextEdit = QTextEdit()
        self.LeftButton_2.setEnabled(False)
        # self.LeftButton_3.setEnabled(False)
        self.pbar = QProgressBar()  # 进度条
        self.pbar.setTextVisible(False)
        self.pbtn = QPushButton('保存')
        self.pbtn.setEnabled(False)

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
        # self.Frame1Layout.addWidget(self.LeftLabel_111, 6, 0, 2, 2)
        # self.Frame1Layout.addWidget(self.numberinput, 6, 1, 2, 1)
        self.Frame1Layout.addWidget(self.PicType, 2, 0, 2, 1)
        # self.Frame1Layout.addWidget(self.VideoType, 2, 1, 2, 1)
        self.Frame1Layout.addWidget(self.DirType, 2, 2, 2, 1)
        self.Frame1Layout.addWidget(self.DateType1, 4, 0, 2, 1)
        self.Frame1Layout.addWidget(self.DateType2, 4, 1, 2, 1)
        self.Frame1Layout.addWidget(self.DateType3, 4, 2, 2, 1)
        self.Frame1Layout.addWidget(self.DateType4, 5, 0, 2, 1)
        self.Frame1Layout.addWidget(self.DateType5, 5, 1, 2, 1)
        self.Frame1Layout.addWidget(self.DateType6, 5, 2, 2, 1)

        self.Frame1Layout.addWidget(self.AddressShow5, 7, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_5, 7, 2, 2, 2)


        self.Frame1Layout.addWidget(self.LeftButton_6, 9, 2, 2, 2)
        self.Frame1Layout.addWidget(self.AddressShow6,9,0,2,2)

        self.Frame1Layout.addWidget(self.LeftButton_7, 11, 2, 2, 2)
        self.Frame1Layout.addWidget(self.AddressShow7, 11, 0, 2, 2)

        self.Frame1Layout.addWidget(self.AddressShow, 13, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_1, 13, 2, 2, 2)
        self.Frame1Layout.addWidget(self.AddressShow1, 13, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_4, 15, 2, 2, 2)
        self.Frame1Layout.addWidget(self.AddressShow4, 15, 0, 2, 2)

        self.Frame1Layout.addWidget(self.LeftButton_2, 17, 0, 2, 4)
        # self.Frame1Layout.addWidget(self.pbar, 16, 0, 2, 2)
        # self.Frame1Layout.addWidget(self.pbtn, 14, 2, 5, 2)
        self.Frame2Layout.addWidget(self.LeftLabel_2, 0, 0, 2, 1)
        # self.Frame2Layout.addWidget(self.TextFrame1, 2, 0, 1, 1)
        # self.Frame2Layout.addWidget(self.TextFrame2, 3, 0, 1, 1)
        # self.Frame2Layout.addWidget(self.TextFrame3, 4, 0, 1, 1)
        self.Frame2Layout.addWidget(self.LeftButton_3, 5, 0, 2, 2)
        self.Frame2Layout.addWidget(self.TextEdit, 2, 0, 2, 2)

        self.LeftLayout.addWidget(self.Frame1, 0, 0, 7, 2)
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
        # 图片变换函数
        def shrinkImage(self, path, width, height, width_scale=1, height_scale=1):
            img = QImage(path)  # 创建图片实例
            mgnWidth = int(width * width_scale)
            mgnHeight = int(height * height_scale)  # 缩放宽高尺寸
            size = QSize(mgnWidth, mgnHeight)

            pixImg = QPixmap.fromImage(
                img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中

            return pixImg, mgnWidth, mgnHeight

        # 往表中加入图像数据
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

        # 往表中加入帧数据
        def addFrame2Table(self, FrameList=None):
            for i in range(len(FrameList)):
                self.TableWidget.insertRow(i)
                item = QTableWidgetItem()
                item.setText(str(FrameList[i][0]))
                item.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 0, item)

        # 对不同目标类型分别编写对应函数
        def ShowImage(self, filename):
            TabCount = self.TabWidget.count()
            if TabCount > 0:  # 清除目前的控件组
                for _ in range(TabCount):
                    self.TabWidget.removeTab(0)
            icon = QIcon()
            icon.addPixmap(QPixmap(".//icon//image.png"), QIcon.Normal, QIcon.Off)
            self.TabWidget.addTab(self.Tab_1, icon, '显示图片')
            pixmap, w, h = shrinkImage(self, filename, self.RightLabel_1.width(), self.RightLabel_1.height())
            self.RightLabel_1.setPixmap(pixmap)

        def ShowTable(self, files):
            TabCount = self.TabWidget.count()
            if TabCount > 0:
                for _ in range(TabCount):
                    self.TabWidget.removeTab(0)
            for _ in range(self.TableWidget.rowCount()):
                self.TableWidget.removeRow(0)
            addPic2Table(self, files)
            icon = QIcon()
            icon.addPixmap(QPixmap(".//icon//table.png"), QIcon.Normal, QIcon.Off)
            self.TabWidget.addTab(self.Tab_2, icon, '显示表格')

        def ShowFrame(self, filename, FrameSpace):
            TabCount = self.TabWidget.count()
            if TabCount > 0:
                for _ in range(TabCount):
                    self.TabWidget.removeTab(0)
                for _ in range(self.TableWidget.rowCount()):
                    self.TableWidget.removeRow(0)
            self.FrameList = list()
            # self.LeftButton_1.setEnabled(False) #使选择按钮无效
            self.FrameWorker.setValue(filename, FrameSpace)
            self.FrameWorker.start()
            # cap = cv2.VideoCapture(filename)
            # Frame = 0
            # while(True):
            #    Frame = Frame + 1
            #    res, image = cap.read()
            #    if (not res) or (len(self.FrameList) == 50):
            #        break
            #    if Frame%FrameSpace == 0:
            #        self.pbar.setValue((Frame/FrameSpace)/50*100)#进度条展示
            #        self.FrameList.append([Frame,image])
            # addFrame2Table(self,self.FrameList)
            # self.TabWidget.addTab(self.Tab_2,qtawesome.icon('fa5s.video', color='black'),'显示帧')
            # QMessageBox.information(self,'通知','提帧完成')#提帧完成的提醒
            # self.pbar.setValue(0)#进度条归零
            # self.LeftButton_1.setEnabled(True) #恢复选择按钮

        self.ShowWidget.close()
        # 判断选择的目标类型，并执行相应函数
        if (self.PicType.isChecked()):
            fname, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image files(*.jpg *.png)')
            if fname:
                self.pbtn.setEnabled(False)
                self.LeftButton_2.setEnabled(False)
                self.LeftText_1.setText("类别")
                self.LeftText_2.setText("置信度")
                # self.LeftText_3.setText("耗时")
                ShowImage(self, fname)
                self.FileName = fname
                self.FileDir = None
                self.isOneFile = True
                self.isPic = True
                self.FrameList = list()
                self.PicPath = {}
                self.pbar.setValue(0)
                self.resultList = list()
                self.LeftButton_2.setEnabled(True)
                self.AddressShow.setText(fname)
        # elif (self.VideoType.isChecked()):
        #     fname, _ = QFileDialog.getOpenFileName(self, '选择视频', '', 'Video Files(*.mp4 *.AVI)')
        #     if fname:
        #         FrameSpace, _ = QInputDialog.getInt(self, '帧间隔', '输入帧间隔', 10, 10, 100, 5)
        #         if FrameSpace:
        #             self.pbtn.setEnabled(False)
        #             self.LeftButton_2.setEnabled(False)
        #             self.TableWidget.setHorizontalHeaderLabels(['帧号'])
        #             self.LeftText_1.setText("类别")
        #             self.LeftText_2.setText("置信度")
        #             self.LeftText_3.setText("耗时")
        #             ShowFrame(self, fname, FrameSpace)
        #             self.FileName = fname
        #             self.FileDir = None
        #             self.isOneFile = False
        #             self.isPic = False
        #             self.PicPath = {}
        #             self.pbar.setValue(0)
        #             self.resultList = list()
        #             self.LeftButton_2.setEnabled(True)
        #             self.AddressShow.setText(fname)
        elif (self.DirType.isChecked()):
            dir = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
            if dir:
                self.pbtn.setEnabled(False)
                self.LeftButton_2.setEnabled(False)
                self.TableWidget.setHorizontalHeaderLabels(['文件名','Se','Sp','AUC'])
                self.LeftText_1.setText("类别")
                self.LeftText_2.setText("置信度")
                # self.LeftText_3.setText("耗时")
                files = os.listdir(dir)
                files = [dir + '/' + x for x in files]
                ShowTable(self, files)
                self.isOneFile = False
                self.FileDir = files
                self.FileName = None
                self.isPic = False
                self.FrameList = list()
                self.pbar.setValue(0)
                self.resultList = list()
                self.LeftButton_2.setEnabled(True)
                self.AddressShow.setText(dir)

    def predict(self):
        self.LeftButton_2.setText('计算中')
        self.LeftButton_1.setEnabled(False)
        self.PredictionWorker.start()

    def save(self):
        dir = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
        if dir:
            if self.resultList:
                if not os.path.exists(dir + '//safe'):
                    os.makedirs(dir + '//safe')
                if not os.path.exists(dir + '//dangerous'):
                    os.makedirs(dir + '//dangerous')
                for i in range(len(self.resultList)):
                    if self.resultList[i][2] == 'safe':
                        cv2.imwrite(dir + '//safe' + '//' + self.resultList[i][4], self.resultList[i][0])
                    else:
                        cv2.imwrite(dir + '//dangerous' + '//' + self.resultList[i][4], self.resultList[i][0])
            else:
                QMessageBox.information(self, '通知', '没有结果')  # 提帧完成的提醒

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