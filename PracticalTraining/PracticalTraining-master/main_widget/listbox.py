from functools import partial
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QPieSeries, QChartView, QChart, QPieSlice
from PyQt5.QtWidgets import QScrollArea, QFrame, QPushButton, QDialog, QLabel, QLineEdit, QMainWindow, QMessageBox
from dbcontroller.dbcontroller import dbcontrolle
from grabdanjuan.Grab import  MultiGrabDJ
from grabqieman.Grab import MultiGrab
import re
import uuid
from main_widget.upwidget import UpdWidget

class ListBox(QScrollArea):
    l_width = 1000
    l_height = 2000

    line_chart=None
    data_form=None
    is_search=False
    upwidget=None
    pid_list=[]

    def __init__(self,parent,line_chart,data_form):
        super(ListBox, self).__init__(parent)


        self.line_chart=line_chart
        self.data_form=data_form
        # 为scrollArea添加 widget
        self.scrollarea_widget_contents = QFrame(self)
        self.search_area = QLineEdit(self)
        self.setWidget(self.scrollarea_widget_contents)

        # 创建按钮列表以及信息
        self.bar = None
        self.bar_list = []
        self.results_list = []

        # 初始化界面
        self.init_ui()
        self.init_data()

    def init_ui(self):
        db = dbcontrolle()
        allinfo = db.get_portfolio_info()
        self.setFixedSize(400, 650)
        self.scrollarea_widget_contents.setFixedSize(400, 40 + len(allinfo) * 110)

        self.search_area.move(10, 10)
        self.search_area.setFixedSize(300, 25)
        self.search_area.setPlaceholderText("根据名字或ID搜索")

        self.confirm = QPushButton(self)
        self.confirm.move(310, 10)
        self.confirm.setFixedSize(50, 25)
        self.confirm.setText("搜索")
        self.confirm.clicked.connect(self.search)

        self.add_button=QPushButton(self)
        self.add_button.move(360,10)
        self.add_button.setFixedSize(40,25)
        self.add_button.setText("添加")
        self.add_button.clicked.connect(self.add_new_source)

        for i in range(len(allinfo)):
            single = bar(allinfo[i], i, self.scrollarea_widget_contents)
            self.bar_list.append(single)
            # single.det.clicked.connect(lambda:self.line_chart.get_id(single.ID))
            single.det.clicked.connect(partial(self.line_chart.get_id,single.ID))
            single.det.clicked.connect(partial(self.data_form.get_id,single.ID))
            single.det.clicked.connect(partial(self.add_id,single.ID))

            single.setFixedSize(380, 100)
            single.move(10, 40 + i * 110)
            single.setStyleSheet("background-color: #dddddd")

        self.setObjectName("list_box")
        self.setStyleSheet(
            "#list_box QScrollBar{"
            "max-width:0px;"
            "}"
        )

    def add_id(self,ID):
        if(ID not in self.pid_list):
            if(len(self.pid_list)<=3):
                self.pid_list.append(ID)
            else:
                for bar in self.bar_list:
                    if(bar.ID==ID):
                        bar.change_add_sub()
        else:
            self.pid_list.remove(ID)

    def init_data(self):
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
        mac_address = '-'.join([mac_address[i:i + 2] for i in range(0, 11, 2)])
        result=dbcontrolle().get_user_record(mac_address)
        dbcontrolle().delete_user_record(mac_address)
        for PID in result:
            for bar in self.bar_list:
                if(PID==bar.ID):
                    bar.det.clicked.emit()

    # 点击搜索按钮后进行搜索
    def search(self):
        self.results_list.clear()
        search_key = self.search_area.text()
        self.search_area.setText("")

        if(search_key=='' and self.is_search==False):
            return

        if self.is_search==True:
            for i in range(len(self.bar_list)):
                self.bar_list[i].show()
                self.bar_list[i].move(10, 40 + i * 110)
            self.scrollarea_widget_contents.setFixedSize(400, 40 + len(self.bar_list) * 110)
            self.is_search=False
            self.confirm.setText("搜索")
        else:
            for i in range(len(self.bar_list)):
                if re.search(search_key, self.bar_list[i].ID) is not None:
                    self.results_list.append(self.bar_list[i])
                    self.bar_list[i].hide()
                    continue
                if re.search(search_key, self.bar_list[i].name) is not None:
                    self.results_list.append(self.bar_list[i])
                    self.bar_list[i].hide()
                    continue
                self.bar_list[i].hide()

            for i in range(len(self.results_list)):
                self.results_list[i].show()
                self.results_list[i].move(10, 40 + i * 110)

            self.scrollarea_widget_contents.setFixedSize(400, 40 + len(self.results_list) * 110)

            self.is_search=True
            self.confirm.setText("复原")

    def add_new_source(self):
        self.results_list.clear()
        search_key = self.search_area.text()
        self.search_area.setText("")

        if(search_key==''):
            return

        else:
            if('CSI' in search_key):
                if not dbcontrolle().pid_is_in_list(search_key):
                    self.upwidget = UpdWidget()
                    if MultiGrabDJ().add_new_jj(search_key):
                        message = dbcontrolle().get_message(search_key)
                        info = [search_key, message[0]['name']]
                        single = bar(info, len(self.bar_list), self.scrollarea_widget_contents)
                        self.bar_list.append(single)
                        # single.det.clicked.connect(lambda:self.line_chart.get_id(single.ID))
                        single.det.clicked.connect(partial(self.line_chart.get_id, single.ID))
                        single.det.clicked.connect(partial(self.data_form.get_id, single.ID))
                        single.det.clicked.connect(partial(self.add_id, single.ID))
                        self.scrollarea_widget_contents.setFixedSize(400, 40 + len(self.bar_list) * 110)
                        single.setFixedSize(380, 100)
                        single.move(10, 40 + (len(self.bar_list)-1) * 110)
                        single.setStyleSheet("background-color: #dddddd")
                        single.show()
                        self.show()
                else:
                    msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '该投资组合已经存在')
                    msg_box.exec_()
                    self.show()
            elif('ZH'in search_key):
                if not dbcontrolle().pid_is_in_list(search_key):
                    self.upwidget = UpdWidget()
                    if MultiGrab().add_new_jj(search_key):

                        message = dbcontrolle().get_message(search_key)
                        info = [search_key, message[0]['name']]
                        single = bar(info, len(self.bar_list), self.scrollarea_widget_contents)
                        self.bar_list.append(single)
                        # single.det.clicked.connect(lambda:self.line_chart.get_id(single.ID))
                        single.det.clicked.connect(partial(self.line_chart.get_id, single.ID))
                        single.det.clicked.connect(partial(self.data_form.get_id, single.ID))
                        single.det.clicked.connect(partial(self.add_id, single.ID))
                        self.scrollarea_widget_contents.setFixedSize(400, 40 + len(self.bar_list) * 110)
                        single.setFixedSize(380, 100)
                        single.move(10, 40 + (len(self.bar_list)-1) * 110)
                        single.setStyleSheet("background-color: #dddddd")
                        single.show()
                        self.show()
                else:
                    msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '该投资组合已经存在')
                    msg_box.exec_()

            else:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '输入不符合规范 添加失败')
                msg_box.exec_()

class bar(QFrame):
    is_add=True
    info=None
    det=None

    def __init__(self, oneinfo, no, frame):
        super(bar, self).__init__(frame)
        self.ID = oneinfo[0]
        self.name = oneinfo[1]
        # sharpe_ratio = oneinfo[2]
        # annualized_yield = oneinfo[3]
        # annualized_volatility = oneinfo[4]
        # max_drawdown = oneinfo[5]
        # net_worth = oneinfo[6]
        # change = oneinfo[7]

        self.info = QPushButton(self)
        self.det = QPushButton(self)


        self.det.clicked.connect(self.change_add_sub)
        self.info.clicked.connect(self.show_detail)

        self.init_ui()


    # 点击每个bar的名字&ID按钮，显示持仓占比
    def show_detail(self):
        self.pie_chart=PieChart(self.ID)
        self.pie_chart.showMaximized()
        self.pie_chart.show()

    def init_ui(self):
        #左边按钮界面初始化
        self.info.setFixedSize(300, 100)
        self.info.move(0, 0)
        self.info.setText(str(self.name) + "\r\nID:" + str(self.ID))
        self.info.setStyleSheet("font-size:20px;"
                           "font-weight:bold;")

        #右边按钮初始化
        self.det.setFixedSize(80, 100)
        self.det.move(300, 0)
        self.det.setText("+")
        self.det.setStyleSheet("font-size:40px;"
                          "font-weight:bold;")

    def change_add_sub(self):
        if self.is_add:
            self.is_add=False
            self.det.setText('-')
        else:
            self.is_add=True
            self.det.setText('+')



class PieChart(QMainWindow):
    pie_chart=None
    ID=None
    position_list =[]
    def __init__(self,id):
        super(PieChart, self).__init__()
        self.ID=id
        self.setWindowTitle("持仓分布")
        #饼状图初始化
        self.pie_chart=QPieSeries()
        self.show_content()
        # self.init_ui()

    #将界面展示 并且通过数据库获取数据初始化饼状图
    def show_content(self):
        c=dbcontrolle()

        position = c.get_position(self.ID)
        for i in position:
            self.pie_chart.append(str(str(i[0])+" "+str(i[1])+"%"),int(i[1]))
        for i in range(0, len(position)):
            slice0 = QPieSlice()
            slice0 = self.pie_chart.slices()[i]
            slice0.setLabelVisible(True)
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(self.pie_chart)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("持仓分布一览")
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartview)


