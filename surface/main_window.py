from random import randint

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout,\
    QListWidgetItem, QLabel,QApplication,QPushButton
from surface.ui_nodes_edit import Ui_Nodes_Edit
from surface.data_set_choose import Data_Choose
from surface.dynamic_line import Dynamic_line
import time
class LeftTabWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(LeftTabWidget, self).__init__(*args, **kwargs)
        self.resize(1200, 600)
        #左右布局(左边一个QListWidget + 右边QStackedWidget)
        self.setWindowFlags(Qt.FramelessWindowHint)
        layout = QHBoxLayout(self)
        #布局边距
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        self.listWidget.setStyleSheet(Stylesheet_listwidget)
        layout.addWidget(self.listWidget)
        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setStyleSheet(Stylesheet_stacked)
        layout.addWidget(self.stackedWidget)
        self.initUi()

    def initUi(self):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 这里就用一般的文本配合图标模式了(也可以直接用Icon模式,setViewMode)
        # for i in range(20):
        #     item = QListWidgetItem(
        #         QIcon('Data/0%d.ico' % randint(1, 8)), str('选 项 %s' % i), self.listWidget)
        #     # 设置item的默认宽高(这里只有高度比较有用)
        #     item.setSizeHint(QSize(16777215, 60))
        #     # 文字居中
        #     item.setTextAlignment(Qt.AlignCenter)
        item_node_edit = QListWidgetItem(QIcon('Data/01d.ico'),str('编辑节点'),self.listWidget)
        item_node_edit.setSizeHint(QSize(16777215,60))
        item_node_edit.setTextAlignment(Qt.AlignCenter)
        item_dataset = QListWidgetItem(QIcon('Data/02d.ico'),str('选择数据'),self.listWidget)
        item_dataset.setSizeHint(QSize(16777215,60))
        item_dataset.setTextAlignment(Qt.AlignCenter)
        item_dataset = QListWidgetItem(QIcon('Data/03d.ico'), str('过程可视化'), self.listWidget)
        item_dataset.setSizeHint(QSize(16777215, 60))
        item_dataset.setTextAlignment(Qt.AlignCenter)
        # 左侧的页面

        # 右侧的页面

            # label = QLabel('我是页面 %d' % i, self)
            # label.setAlignment(Qt.AlignCenter)
            # # 设置label的背景颜色(这里随机)
            # # 这里加了一个margin边距(方便区分QStackedWidget和QLabel的颜色)
            # label.setStyleSheet('background: rgb(%d, %d, %d);margin: 50px;' % (
            #     randint(0, 255), randint(0, 255), randint(0, 255)))
        ui_edit_nodes = Ui_Nodes_Edit()
        self.stackedWidget.addWidget(ui_edit_nodes)
        ui_data_choose = Data_Choose()
        self.stackedWidget.addWidget(ui_data_choose)
        ui_line = Dynamic_line()
        self.stackedWidget.addWidget(ui_line)

# 美化样式表
Stylesheet_listwidget = """
/*去掉item虚线边框*/
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
/*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
QListWidget {
    min-width: 120px;
    max-width: 120px;
    color: white;
    background: black;
}
/*被选中时的背景颜色和左边框颜色*/
QListWidget::item:selected {
    background: rgb(52, 52, 52);
    border-left: 2px solid rgb(9, 187, 7);
}
/*鼠标悬停颜色*/
HistoryPanel::item:hover {
    background: rgb(52, 52, 52);
}
"""
Stylesheet_stacked="""
/*右侧的层叠窗口的背景颜色*/
QStackedWidget {
    background: rgb(30, 30, 30);
}
"""

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = LeftTabWidget()
    w.show()
    sys.exit(app.exec_())