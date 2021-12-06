# 更新进度条窗口
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel
class UpdWidget(QWidget):
    def __init__(self):
        super(UpdWidget, self).__init__()
        self.info = QLabel(self)
        self.step = 0
        self.signal = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(500, 180)
        self.setWindowTitle('正在更新')
        self.info.setGeometry(165, 30, 200, 30)
        self.info.setText("更新完成")
        self.show()
