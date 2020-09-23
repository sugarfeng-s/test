import sys
import os
import json
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
import requests
# from Net_design import Net_design
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
class choose_ui(QDialog):
    mySignal = pyqtSignal(list)

    def __init__(self):
        super(choose_ui, self).__init__()
        self.setWindowTitle("Network Design Module")
        self.move(400, 200)
        self.resize(200,100)
        self.init_UI()
    def init_UI(self):
        # 设置窗口主布局
        # Main_Ui = QWidget()
        self.MainLayout = QGridLayout()
        # Main_Ui.setLayout(self.MainLayout)
        self.DateType1 = QCheckBox("aspp")
        # self.DateType1.setGeometry(5, 5, 5, 5)
        # self.VideoType = QRadioButton("视频文件")
        self.DateType2 = QCheckBox("resblock")
        self.DateType3 = QCheckBox("attention")
        self.DateType4 = QCheckBox("dense")
        self.DateType5 = QCheckBox("deep")
        # self.DateType6 = QCheckBox("投影")
        self.Finished = QPushButton("完成")
        self.Finished.clicked.connect(self.sendEditContent)
        self.exit = QPushButton("退出")
        self.exit.clicked.connect(self.close)
        self.MainLayout.addWidget(self.DateType1, 4, 0, 2, 1)
        self.MainLayout.addWidget(self.DateType2, 4, 1, 2, 1)
        self.MainLayout.addWidget(self.DateType3, 4, 2, 2, 1)
        self.MainLayout.addWidget(self.DateType4, 5, 0, 2, 1)
        self.MainLayout.addWidget(self.DateType5, 5, 1, 2, 1)
        self.MainLayout.addWidget(self.Finished,8,0,1,1)
        self.MainLayout.addWidget(self.exit, 8, 1, 1, 1)
        # self.MainLayout.addWidget(self.DateType6, 5, 2, 2, 1)
        self.setLayout(self.MainLayout)

    def sendEditContent(self):
        aug_list = []
        if self.DateType1.isChecked():
            aug_list.append('ASPP')
        if self.DateType2.isChecked():
            aug_list.append('RES')
        if self.DateType3.isChecked():
            aug_list.append('SE')
        if self.DateType4.isChecked():
            aug_list.append('IC')
        if self.DateType5.isChecked():
            aug_list.append('DS')
        self.mySignal.emit(aug_list)  # 发射信号
        self.close()


class Design(QMainWindow):  # 主窗口类
    signal = pyqtSignal()

    def __init__(self):
        super(Design, self).__init__()
        self.setWindowTitle("Network Design Module")
        self.setFixedSize(1000, 700)
        self.move(400, 200)
        self.all_aug_list = []
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground, False)  # 设置窗口背景透明
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口取消边框
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
        self.auglist = []
        self.LeftButton_1.clicked.connect(self.selectTarget)  # 关联目标选择按钮到selectTarget函数
        self.LeftButton_2.clicked.connect(self.predict)  # 关联开始按钮到predict函数
        self.LeftButton_4.clicked.connect(self.save)  # 关联保存按钮到save函数
        self.LeftButton_3.clicked.connect(self.closeALL)  # 关联推出按钮到程序推出函数

        self.RightButton_1.clicked.connect(self.go_choose)
        self.RightButton_2.clicked.connect(self.go_choose)
        self.RightButton_3.clicked.connect(self.go_choose)
        self.RightButton_4.clicked.connect(self.go_choose)
        self.RightButton_5.clicked.connect(self.go_choose)
        self.RightButton_6.clicked.connect(self.go_choose)
        self.RightButton_7.clicked.connect(self.go_choose)
        self.RightButton_8.clicked.connect(self.go_choose)
        # self.RightButton_1.clicked.connect(self.write_json1)
        # self.TableWidget.cellDoubleClicked.connect(self.TableDoubleClick)
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
        self.LeftLabel_1 = QLabel("基础网络选择:")
        self.LeftLabel_2 = QLabel("运行日志:")
        # 设置左侧上半部分
        self.PicType = QRadioButton("U-net")
        self.AddressShow = QLineEdit("")
        self.AddressShow.setReadOnly(True)
        self.AddressShow1 = QLineEdit("")
        self.AddressShow1.setReadOnly(True)
        self.numberinput = QLineEdit("")
        self.LeftButton_1 = QPushButton(qtawesome.icon('fa.file', color='black'), "选择基础网络文件")
        self.LeftButton_2 = QPushButton(qtawesome.icon('fa.sellsy', color='black'), "运行")
        self.LeftButton_4 = QPushButton(qtawesome.icon('fa.file', color='black'), "保存新网络配置")
        self.LeftButton_2.setEnabled(False)
        # self.LeftButton_3.setEnabled(False)
        self.pbar = QProgressBar()  # 进度条
        self.pbar.setTextVisible(False)
        # 设置左侧下半部分
        self.TextEdit = QTextEdit()
        self.TextEdit.setText("")
        self.LeftButton_3 = QPushButton("退出")

        # 添加所有控件至左侧布局
        self.Frame1Layout.addWidget(self.LeftLabel_1, 1, 0, 2, 2)
        # self.Frame1Layout.addWidget(self.LeftLabel_11, 3, 0, 2, 2)
        # self.Frame1Layout.addWidget(self.LeftLabel_111, 6, 0, 2, 2)
        # self.Frame1Layout.addWidget(self.numberinput, 6, 1, 2, 1)
        self.Frame1Layout.addWidget(self.PicType, 2, 0, 2, 1)
        # self.Frame1Layout.addWidget(self.VideoType, 2, 1, 2, 1)
        # self.Frame1Layout.addWidget(self.DirType, 2, 2, 2, 1)
        # self.Frame1Layout.addWidget(self.DateType1, 4, 0, 2, 1)
        # self.Frame1Layout.addWidget(self.DateType2, 4, 1, 2, 1)
        # self.Frame1Layout.addWidget(self.DateType3, 4, 2, 2, 1)
        # self.Frame1Layout.addWidget(self.DateType4, 5, 0, 2, 1)
        # self.Frame1Layout.addWidget(self.DateType5, 5, 1, 2, 1)
        # self.Frame1Layout.addWidget(self.DateType6, 5, 2, 2, 1)
        self.Frame1Layout.addWidget(self.AddressShow, 8, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_1, 8, 2, 2, 1)
        self.Frame1Layout.addWidget(self.AddressShow1, 10, 0, 2, 2)
        self.Frame1Layout.addWidget(self.LeftButton_4, 10, 2, 2, 1)
        self.Frame1Layout.addWidget(self.LeftButton_2, 11, 2, 5, 2)
        self.Frame1Layout.addWidget(self.pbar, 11, 0, 5, 2)
        # self.Frame1Layout.addWidget(self.pbtn, 7, 2, 5, 2)
        self.Frame2Layout.addWidget(self.LeftLabel_2, 0, 0, 2, 1)
        self.Frame2Layout.addWidget(self.LeftButton_3, 5, 0, 2, 2)
        # self.Frame2Layout.addWidget(self.TextFrame1, 2, 0, 1, 1)
        # self.Frame2Layout.addWidget(self.TextFrame2, 3, 0, 1, 1)
        # self.Frame2Layout.addWidget(self.TextFrame3, 4, 0, 1, 1)
        self.Frame2Layout.addWidget(self.TextEdit, 2, 0, 2, 2)

        self.LeftLayout.addWidget(self.Frame1, 0, 0, 5, 2)
        self.LeftLayout.addWidget(self.Frame2, 7, 0, 5, 2)
        # 添加至窗口主布局
        self.MainLayout.addWidget(self.LeftWidget, 0, 0, 25, 3)

    def init_RightUI(self):
        # 设置窗口右侧布局
        self.RightWidget = QWidget()
        self.RightLayout = QGridLayout()
        self.RightWidget.setLayout(self.RightLayout)
        url = 'https://img-blog.csdnimg.cn/20181127092719427.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zNzk3MzYxNA==,size_16,color_FFFFFF,t_70'
        req = requests.get(url)
        # print(req.content)
        photo = QPixmap()
        photo.loadFromData(req.content)
        self.bdImg = QLabel()
        self.bdImg.setPixmap(photo)
        self.bdImg.setScaledContents(True)  # 让图片自适应label大小

        self.RightButton_1 = QPushButton("1层添加")
        self.RightButton_2 = QPushButton("8层添加")

        self.RightButton_3 = QPushButton("2层添加")
        self.RightButton_4 = QPushButton("7层添加")

        self.RightButton_5 = QPushButton("3层添加")
        self.RightButton_6 = QPushButton("6层添加")

        self.RightButton_7 = QPushButton("4层添加")
        self.RightButton_8 = QPushButton("5层添加")


        self.RightLayout.addWidget(self.bdImg, 0, 0, 20, 2)
        self.RightLayout.addWidget(self.RightButton_1,5,7,1,1)
        self.RightLayout.addWidget(self.RightButton_2, 6, 7, 1, 1)
        self.RightLayout.addWidget(self.RightButton_3, 11, 7, 1, 1)
        self.RightLayout.addWidget(self.RightButton_4, 12, 7, 1, 1)
        self.RightLayout.addWidget(self.RightButton_5, 14, 7, 1, 1)
        self.RightLayout.addWidget(self.RightButton_6, 15, 7, 1, 1)

        self.RightLayout.addWidget(self.RightButton_7, 17, 7, 1, 1)
        self.RightLayout.addWidget(self.RightButton_8, 18, 7, 1, 1)

        self.MainLayout.addWidget(self.RightWidget, 0, 3, 25, 5)


    def predict(self):
        flag = 0
        if self.PicType.isChecked():
            if not self.AddressShow.text() == "":
                if not self.AddressShow1.text() == "":
                    flag=1
        if flag:
            start = time.time()
            self.pbar.setValue(0)
            self.PredictionWorker.start()
            with open(os.path.join(self.AddressShow1.text(),'design_log.json'),'w') as f:
                json.dump(self.all_aug_list, f)
            self.design_server = Net_design(os.path.join(self.AddressShow1.text(),'design_log.json'))
            self.design_server.build()
            self.PredictionWorker.terminate()
            self.pbar.setValue(100)
            all = time.time() - start
        else:
            QMessageBox.information(self, '通知', 'complete your param')
    def selectTarget(self):
        print("xxxxxxxxxx")
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
        # print(dir)
        self.AddressShow1.setText(dir)
        self.LeftButton_2.setEnabled(True)
        self.savePath = dir

    def pbarProcess(self, number):
        self.pbar.setValue(number)
    def getDialogSignal(self,auglist):
        self.auglist = auglist
        print(self.part,self.auglist)
        add_dict={}
        add_dict[self.part]=self.auglist
        self.all_aug_list.append(add_dict)
        self.TextEdit.moveCursor(QTextCursor.End)
        self.TextEdit.insertPlainText(str(add_dict)+'\n')

    def go_choose(self):
        sender = self.sender()
        clickevent = sender.text()
        if clickevent == u'1层添加':
            self.part = "1"
        if clickevent == u'8层添加':
            self.part = "8"
        if clickevent == u'2层添加':
            self.part = "2"
        if clickevent == u'7层添加':
            self.part = "7"
        if clickevent == u'3层添加':
            self.part = "3"
        if clickevent == u'6层添加':
            self.part = "6"
        if clickevent == u'4层添加':
            self.part = "4"
        if clickevent == u'5层添加':
            self.part = "5"
        uichoose = choose_ui()
        uichoose.mySignal.connect(self.getDialogSignal)
        uichoose.exec_()

    def closeALL(self):
        self.ShowWidget.close()
        self.RightDock.close()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Design()
    MainWindow.show()
    # uichoose = choose_ui()
    # MainWindow.RightButton_1.clicked.connect(uichoose.show)
    sys.exit(app.exec_())