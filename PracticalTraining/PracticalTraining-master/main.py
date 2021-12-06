import multiprocessing
import sys
from PyQt5.QtWidgets import QApplication
from main_widget.main_widget import main_widget, UpdWidget

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    mainwindow = main_widget()
    mainwindow.show()
    sys.exit(app.exec_())