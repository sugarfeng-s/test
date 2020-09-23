import sys
import os
import time
import cv2
import traceback
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
# from Net_train import Net_train


def numpy2QPixmap(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    qimage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
    pixmap = QPixmap(qimage)
    return pixmap


class PredictionWorker(QThread):
    signal = pyqtSignal(int)

    def __init__(self, MainWidget):
        super(PredictionWorker, self).__init__()
        self.MainWidget = MainWidget
    def run(self):
        while 1:
        #     print(1111)
            time.sleep(1)
            self.signal.emit(1)
        # self.MainWidget.TextEdit.setText('1')
        # self.MainWidget.LOG.moveCursor(QTextCursor.End)
        # self.MainWidget.LOG.insertPlainText('1111'+ '\n')


class Train(QMainWindow):  # 主窗口类
    signal = pyqtSignal()

    def __init__(self):
        super(Train, self).__init__()
        self.setWindowTitle("Network Training Module")
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

        self.resultList = list()  # 预测结果存储位置
        # self.FrameWorker = FrameWorker(self)
        self.PredictionWorker = PredictionWorker(self)

        self.init_UI()

    def init_UI(self):
        # 设置窗口主布局
        Main_Ui = QWidget()
        self.setCentralWidget(Main_Ui)
        self.MainLayout = QGridLayout()
        Main_Ui.setLayout(self.MainLayout)
        self.init_LeftUI()  # 初始化左侧布局
        self.init_RightUI()  # 初始化右侧布局

        self.LeftButton_1.clicked.connect(self.save)  # 关联目标选择按钮到selectTarget函数
        self.LeftButton_2.clicked.connect(self.predict)  # 关联开始按钮到predict函数
        self.LeftButton_4.clicked.connect(self.save)  # 关联保存按钮到save函数
        self.LeftButton_5.clicked.connect(self.save)  # 关联保存按钮到save函数
        self.LeftButton_6.clicked.connect(self.save)  # 关联保存按钮到save函数
        self.LeftButton_3.clicked.connect(self.closeALL)  # 关联推出按钮到程序推出函数

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
        self.LeftLabel_1 = QLabel("基础网络选择:")
        self.LeftLabel_11 = QLabel("数据路径导入：")
        self.LeftLabel_111 = QLabel("配置文件导入：")
        self.LeftLabel_2 = QLabel("                 参数设置:")

        # 设置左侧下标签
        self.LeftLabel_d1 = QLabel("训练轮数：")
        self.LeftT_d1 = QLineEdit()

        self.LeftLabel_d2 = QLabel("学习率：")
        self.LeftT_d2 = QLineEdit()

        self.LeftLabel_d3 = QLabel("优化器类型：")
        self.group_opt = QButtonGroup()
        self.d3_1 = QRadioButton("SDG")
        self.d3_2 = QRadioButton("Adam")
        self.d3_3 = QRadioButton("Momentum")
        self.group_opt.addButton(self.d3_1,id=1)
        self.group_opt.addButton(self.d3_2,id=2)
        self.group_opt.addButton(self.d3_3,id=3)
        self.LeftLabel_d4 = QLabel("损失函数类型:")
        self.d4_1 = QRadioButton("CE")
        self.d4_2 = QRadioButton("Dice")

        self.LeftLabel_d5 = QLabel("批次大小：")
        self.d5 = QLineEdit()

        # 设置左侧上半部分
        self.PicType = QRadioButton("U-net")
        # self.VideoType = QRadioButton("视频文件")
        self.DirType = QRadioButton("ResNet")


        self.PicType.setChecked(False)
        self.AddressShow = QLineEdit("")
        self.AddressShow.setReadOnly(False)
        self.AddressShow1 = QLineEdit("")
        self.AddressShow1.setReadOnly(False)
        self.AddressShow2 = QLineEdit("")
        self.AddressShow2.setReadOnly(False)
        self.numberinput = QLineEdit("")
        self.AddressShow5 = QLineEdit("")
        self.AddressShow6 = QLineEdit("")
        self.LeftButton_1 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择基础网络文件")
        self.LeftButton_5 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择数据集路径")
        self.LeftButton_6 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择网络配置文件")
        self.LeftButton_2 = QPushButton(qtawesome.icon('fa.sellsy', color='black'), "运行")


        self.LeftButton_4 = QPushButton(qtawesome.icon('fa.file', color='black'), "保存训练权重")
        self.LeftButton_2.setEnabled(True)

        self.pbar = QProgressBar()  # 进度条
        self.pbar.setTextVisible(False)

        # 设置左侧下半部分
        self.TextEdit = QTextEdit("")

        self.LeftButton_3 = QPushButton("退出")

        # 添加所有控件至左侧布局
        self.Frame1Layout.addWidget(self.LeftLabel_1, 1, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftLabel_11, 3, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftLabel_111, 5, 0, 2, 2)

        self.Frame1Layout.addWidget(self.AddressShow, 2, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_1, 2, 2, 2, 2)

        self.Frame1Layout.addWidget(self.LeftButton_5, 4, 2, 2, 2)
        self.Frame1Layout.addWidget(self.AddressShow5, 4, 0, 2, 2)

        self.Frame1Layout.addWidget(self.LeftButton_6, 6, 2, 2, 2)
        self.Frame1Layout.addWidget(self.AddressShow6, 6, 0, 2, 2)

        self.Frame1Layout.addWidget(self.AddressShow1, 10, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_4, 10, 2, 2, 2)

        self.Frame2Layout.addWidget(self.LeftLabel_2, 0, 0, 1, 1)
        self.Frame2Layout.addWidget(self.LeftButton_3, 9, 0, 2, 2)

        self.Frame2Layout.addWidget(self.LeftButton_2, 8, 0, 2, 2)
        self.Frame2Layout.addWidget(self.LeftLabel_d1, 1, 0, 1, 1)
        self.Frame2Layout.addWidget(self.LeftT_d1, 1, 1, 1, 1)

        self.Frame2Layout.addWidget(self.LeftLabel_d2, 2, 0, 1, 2)
        self.Frame2Layout.addWidget(self.LeftT_d2, 2, 1, 1, 1)

        self.Frame2Layout.addWidget(self.LeftLabel_d3, 3, 0, 1, 1)
        self.Frame2Layout.addWidget(self.d3_1, 4, 0, 1, 1)
        self.Frame2Layout.addWidget(self.d3_2, 4, 1, 1, 1)
        self.Frame2Layout.addWidget(self.d3_3, 4, 2, 1, 1)

        self.Frame2Layout.addWidget(self.LeftLabel_d4, 5, 0, 1, 2)
        self.Frame2Layout.addWidget(self.d4_1, 6, 0, 1, 1)
        self.Frame2Layout.addWidget(self.d4_2, 6, 1, 1, 1)


        self.Frame2Layout.addWidget(self.LeftLabel_d5, 7, 0, 1, 2)
        self.Frame2Layout.addWidget(self.d5, 7, 1, 1, 1)
        self.LeftLayout.addWidget(self.Frame1, 0, 0, 3, 2)
        self.LeftLayout.addWidget(self.Frame2, 5, 0, 5, 2)
        # 添加至窗口主布局
        self.MainLayout.addWidget(self.LeftWidget, 0, 0, 25, 3)

    def init_RightUI(self):
        # 设置窗口右侧布局
        self.RightWidget = QWidget()
        self.RightLayout = QGridLayout()
        self.RightWidget.setLayout(self.RightLayout)
        self.LOG = QLineEdit("运行日志")
        self.RightLayout.addWidget(self.LOG)
        self.RightLayout.addWidget(self.TextEdit)
        self.PredictionWorker.signal.connect(self.textChange)
        self.MainLayout.addWidget(self.RightWidget, 0, 3, 25, 5)
    def textChange(self):
        self.TextEdit.setText("")
        with open(os.path.join(self.AddressShow1.text(),'train_log.txt')) as f:
            text = f.read()
            self.TextEdit.setText(text)
    def selectTarget(self):
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

    def save(self):
        dir = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
        sender = self.sender()
        clickevent = sender.text()
        if clickevent == u'选择基础网络文件':
        # print(dir)
            self.AddressShow.setText(dir)
        if clickevent == u'选择数据集路径':
            self.AddressShow5.setText(dir)
        if clickevent == u'选择网络配置文件':
            self.AddressShow6.setText(dir)
        if clickevent == u'保存训练权重':
            self.AddressShow1.setText(dir)
        # self.LeftButton_2.setEnabled(True)
        # self.savePath = dir

    def predict(self):
        flag = 1
        if not self.AddressShow.text() == "":
            if not self.AddressShow1.text() == "":
                if not self.AddressShow5.text() == "":
                    if not self.AddressShow6.text() == "":
                        if not self.LeftT_d2.text() == "":
                            if not self.LeftT_d1.text() == "":
                                if self.group_opt.checkedButton():
                                    if not self.LeftLabel_d5.text() == "":
                                        if self.d4_1.isChecked() or self.d4_2.isChecked():
                                            flag = 1
        if flag:
            id = self.group_opt.checkedId()
            # print(id)
            if id == 1:
                self.opt = 'SGD'
            if id == 2:
                self.opt = 'Adam'
            if id == 3:
                self.opt = 'Momentum'
            if self.d4_1.isChecked():
                self.loss_func='CE'
            if self.d4_2.isChecked():
                self.loss_func='Dice'
            self.train_server = Net_train(self.AddressShow6.text(),self.LeftT_d2.text(),self.LeftT_d1.text(),
                      self.opt,self.loss_func,self.LeftLabel_d5.text(),self.AddressShow5.text(),
                      self.AddressShow1.text())
            self.PredictionWorker.start()
            self.train_server.train()
            self.PredictionWorker.terminate()

        else:
            QMessageBox.information(self, '通知', 'complete your param')

    def pbarProcess(self, number):
        self.pbar.setValue(number)

    def closeALL(self):
        self.ShowWidget.close()
        self.RightDock.close()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainUI()
    MainWindow.show()
    sys.exit(app.exec_())