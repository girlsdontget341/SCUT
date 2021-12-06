import sys
from dbcontroller.dbcontroller import dbcontrolle
from Tool.Tool import Tool
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QDateTimeEdit, QComboBox, QSpinBox, \
    QApplication, QHeaderView
from PyQt5.QtCore import *
#只会向这个类传入 id
#通过id去获取比较数据 显示在表格上面
#表格中要有的信息 有 基金id  基金名字  基金的涨幅/年化收益率, 最大回撤, 夏普比, 年化波动率.
#然后数据来源是通过数据库下载过来的
#里面有个判断字段 就是说如果用户未选择时间 从pro***那个表获取数据显示  如果用户选择了时间 就必须载入数据使用tool中的数据去计算
class data_form(QWidget):
    c = dbcontrolle()
    is_select_time = False
    start_time = None
    end_time = None
    pid_list = []
    orderType=Qt.DescendingOrder

    def __init__(self,parent):
        super(data_form, self).__init__(parent)
        self.hhbox = QHBoxLayout()  # 横向布局
        self.tableWidget = QTableWidget()

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["名称", "涨跌幅", "年波动率", "最大回撤", "净值", "夏普比"])
        self.tableWidget.cellClicked.connect(self.sort_by_message)
        self.init_ui()
        self.show()

    def table_sitting(self):
        self.tableWidget.verticalHeader().setVisible(False)

        if (self.is_select_time == False):
            i=0
            for pid in self.pid_list:
               data_list2 = self.c.get_message(pid)
               self.tableWidget.setHorizontalHeaderLabels(["名称", "涨跌幅",  "年波动率", "最大回撤", "净值", "夏普比"])

               item = QTableWidgetItem(data_list2[0]['name'])
               item.setFlags(Qt.ItemIsEditable)
               self.tableWidget.setItem(i, 0, item)
               item = QTableWidgetItem(str(data_list2[0]['change'])+'%')
               item.setFlags(Qt.ItemIsEditable)
               self.tableWidget.setItem(i, 1, item)
               item = QTableWidgetItem(str(data_list2[0]['annualized-volatility'])+'%')
               item.setFlags(Qt.ItemIsEditable)
               self.tableWidget.setItem(i, 2, item)
               item = QTableWidgetItem(str(data_list2[0]['max_drawdown'])+'%')
               item.setFlags(Qt.ItemIsEditable)
               self.tableWidget.setItem(i, 3, item)
               item = QTableWidgetItem(str(data_list2[0]['net_worth']))
               item.setFlags(Qt.ItemIsEditable)
               self.tableWidget.setItem(i, 4, item)
               item = QTableWidgetItem(str(data_list2[0]['sharpe_ratio']))
               item.setFlags(Qt.ItemIsEditable)
               self.tableWidget.setItem(i, 5, item)
               i= i+1
        if (self.is_select_time):
            annualized_yield = []
            annualized_volatility = []
            max_drawdown = []
            sharpe_ratio = []
            self.tableWidget.setHorizontalHeaderLabels(["名称", "年收益率", "年波动率", "最大回撤", "净值", "夏普比"])
            i=0
            for pid in self.pid_list:
                data_list2 = self.c.get_message(pid)
                item = QTableWidgetItem(data_list2[0]['name'])
                item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(i, 0, item)
                i = i+1

            j=0
            for pid in self.pid_list:
                    datalist = self.c.get_history_message(pid, self.start_time, self.end_time)
                    annualized_yield.append(Tool(datalist).calculate_annualized_yield())
                    annualized_volatility.append(Tool(datalist).calculate_annualized_volatility())
                    max_drawdown.append(Tool(datalist).calculate_max_drawdown())
                    sharpe_ratio.append(Tool(datalist).calculate_sharpe_ratio())
                    item = QTableWidgetItem(str(datalist[j]['net_worth']))
                    item.setFlags(Qt.ItemIsEditable)
                    self.tableWidget.setItem(j, 4, item)
                    j =j+1

            for j in range(0, len(self.pid_list)):
                item = QTableWidgetItem(str(annualized_yield[j])+'%')
                item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(j, 1, item)
                item = QTableWidgetItem(str(annualized_volatility[j])+'%')
                item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(j, 2, item)
                item = QTableWidgetItem(str(max_drawdown[j]))
                item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(j, 3, item)
                item = QTableWidgetItem(str(sharpe_ratio[j]))
                item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(j, 5, item)

    def sort_by_message(self,row, column):
        print(row, column)
        name_list1=["名称", "涨跌幅", "年波动率", "最大回撤", "净值", "夏普比"]
        name_list2=["名称", "年收益率", "年波动率", "最大回撤", "净值", "夏普比"]

        if self.orderType == Qt.DescendingOrder:
            self.orderType = Qt.AscendingOrder
            if self.is_select_time==0:
                name_list1[column]+='↑'
                self.tableWidget.setHorizontalHeaderLabels(name_list1)
            else:
                name_list1[column]+='↑'
                self.tableWidget.setHorizontalHeaderLabels(name_list2)
        else:
            self.orderType = Qt.DescendingOrder
            if self.is_select_time==0:
                name_list1[column]+='↓'
                self.tableWidget.setHorizontalHeaderLabels(name_list1)
            else:
                name_list1[column]+='↓'
                self.tableWidget.setHorizontalHeaderLabels(name_list2)


        self.tableWidget.sortItems(column, self.orderType)

    def get_id(self,id):
        print("表格图"+id)
        if id in self.pid_list:
            self.pid_list.remove(id)
            self.tableWidget.setRowCount(len(self.pid_list))
            self.table_sitting()
        else:
            if(len(self.pid_list)<=3):
                self.pid_list.append(id)
                self.tableWidget.setRowCount(len(self.pid_list))
                self.table_sitting()

    def get_time(self,start_time,end_time):
        self.is_select_time= True
        self.tableWidget.setColumnCount(6)
        self.start_time =start_time
        self.end_time = end_time
        self.table_sitting()
        self.init_ui()

    def init_ui(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hhbox.addWidget(self.tableWidget)  # 把表格加入布局
        self.setLayout(self.hhbox)  # 创建布局
        self.setWindowTitle("投资组合数据一览")
        self.resize(1600, 200)