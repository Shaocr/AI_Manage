import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
import os
#编辑节点的html文件位置
html_path = os.path.dirname(os.path.realpath(__file__))+'\\dag\\page\\main.html'
#导入主控制台
from control.main_control import console
#主窗口
class Ui_Nodes_Edit(QWidget):
    #给以后留的接口
    #向html发送数据用的信号
    SigSendMessageToJS = pyqtSignal(str)
    def __init__(self):
        super(Ui_Nodes_Edit,self).__init__()
        self.resize(720,480)
        #浏览器
        self.browser = QWebEngineView(self)
        #前端与后端交互的类
        self.pInteractObj = TInteractObj(self)
        #定义浏览器的通道
        self.pWebChannel = QWebChannel(self.browser)
        #将前后端交互的类在通道上注册
        self.pWebChannel.registerObject('interactObj',self.pInteractObj)
        #将浏览器的通道设置为刚刚定义的通道
        self.browser.page().setWebChannel(self.pWebChannel)
        #加载本地html
        self.browser.load(QUrl.fromLocalFile(html_path))
        #将前后端交互类的信号与接受信号类的函数连接
        self.pInteractObj.SigReceivedMessFromJS.connect(self.OnReceiveMessageFromJS)
        # 将前后端交互类的信号与发送信号类的函数连接
        self.SigSendMessageToJS.connect(self.pInteractObj.SigSendMessageToJS)
        #创建水平布局
        self.layout = QHBoxLayout()
        #添加浏览器
        self.layout.addWidget(self.browser)
        #设置边距全为0
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        #self.browser.load(QUrl('https://www.baidu.com'))
        #self.setCentralWidget(self.browser)

    def OnReceiveMessageFromJS(self, strParameter):
        print('OnReceiveMessageFromJS()')
        if not strParameter:
            return
        console.create_abstract_class(nodes=strParameter)

    def OnSendMessageByInteractObj(self):
        strMessage = self.mpQtSendLineEdit.text()
        if not strMessage:
            return
        self.SigSendMessageToJS.emit(strMessage)

    def OnSendMessageByJavaScript(self):
        strMessage = self.mpQtSendLineEdit.text()
        if not strMessage:
            return
        strMessage = 'Received string from Qt:' + strMessage
        self.mpJSWebView.page().runJavaScript("output(%s)" % strMessage)

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TInteractObj(QObject):
    SigReceivedMessFromJS = pyqtSignal(str)
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('JSSendMessage(%s) from Html' % strParameter)
        self.SigReceivedMessFromJS.emit(strParameter)

    #预留接口
    #本身向js返回数据
    # @pyqtSlot(result=str)
    # def fun(self):
    #     print('TInteractObj.fun()')

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = Ui_Nodes_Edit()
    win.show()
    sys.exit(app.exec_())