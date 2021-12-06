from PyQt5.QtWidgets import QCalendarWidget, QWidget, QFrame, QPushButton, QGridLayout, QLabel, QMessageBox
from PyQt5.QtCore import  pyqtSignal, Qt
from datetime import datetime
from Tool.date_control import DateController
from PyQt5.QtGui import *
import copy

week_info_list = ['一', '二', '三', '四', '五', '六', '日']

class MyDayCalendar(QFrame):
    _select_datetime_signal = pyqtSignal(str,str)
    h_width=None
    h_height=None

    background_label=None
    calendar=None
    time_interval={
        'start_time':'',
        'end_time':''
    }
    count=0

    def __init__(self):
        super(MyDayCalendar, self).__init__()
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setWindowModality(Qt.ApplicationModal)

        self.background_label = QLabel(self)
        self.calendar=CalendarWidget(self)

        self.h_width=self.calendar.h_width
        self.h_height=self.calendar.h_height

        self.calendar._close_widget_signal.connect(self.select_and_close)

        self.init_ui()

    def init_ui(self):
        self.resize(self.h_width,self.h_height)
        self.background_label.resize(self.h_width,self.h_height)
        self.background_label.setObjectName("calendar_background")
        self.background_label.setGeometry(0,0,self.h_width,self.h_height)


    def select_and_close(self,date):
        now = datetime.now()

        if(self.count==0):
            self.time_interval['start_time']=date
        if(self.count==1):
            start_time=self.time_interval['start_time']
            if(date<start_time):
                self.time_interval['start_time'] = date
                self.time_interval['end_time']=start_time
            else:
                self.time_interval['end_time']=date
        self.count += 1
        if(self.count==2):
            cha=(self.time_interval['end_time']-self.time_interval["start_time"]).days
            if(cha>=5):
                if(self.time_interval['end_time']>now):
                    self.count=0
                    self.calendar.calendar.change_chosen()
                    msg_box = QMessageBox(QMessageBox.Warning, '警告', '不能选择大于当前日期的时间')
                    msg_box.exec_()
                else:
                    self._select_datetime_signal.emit(self.time_interval["start_time"].strftime('%Y-%m-%d'),self.time_interval["end_time"].strftime('%Y-%m-%d'))
                    self.count=0
                    self.calendar.calendar.change_chosen()
                    self.close()
            else:
                self.count=0
                self.calendar.calendar.change_chosen()
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '选择的两个日期差不能小于6天')
                msg_box.exec_()


# 此类为总的日历控件，包含日历和切换按钮等
class CalendarWidget(QFrame):
    _close_widget_signal=pyqtSignal(datetime)
    # 基础属性
    h_height = 500
    h_width = 600

    # 控件
    calendar = None
    select_date_widget = None
    week_info_bar = None
    date_controller = None

    count=0

    def __init__(self, parent):
        super().__init__()
        # 初始化日历控件
        self.setParent(parent)

        # 初始化日历

        # 获取当前时间
        current_date = datetime.today()

        self.date_controller = DateController(current_date.year,current_date.month,current_date.day)
        self.calendar = Calendar(self, self.date_controller)
        self.select_date_widget = SelectDateWidget(self, self.date_controller)
        self.week_info_bar = WeekInfoBar(self)



        # 绑定信号槽
        self.select_date_widget.add_button.clicked.connect(self.calendar.increase_month)
        self.select_date_widget.subtract_button.clicked.connect(self.calendar.decrease_month)
        self.select_date_widget.add_button.clicked.connect(self.select_date_widget.refresh_date_info)
        self.select_date_widget.subtract_button.clicked.connect(self.select_date_widget.refresh_date_info)
        self.calendar.date_selected.connect(self.date_selected_exec)

        # 初始化ui
        self.init_ui()

    # 接受来自calendar的date_selected信号的槽函数
    def date_selected_exec(self, date):
        year = date.year
        month = date.month
        day = date.day
        select_time=datetime(year,month,day)

        self._close_widget_signal.emit(select_time)

    def init_ui(self):

        # 设定id
        self.resize(self.h_width, self.h_height)

        self.setObjectName('calendar_widget')

        # 控件的垂直高度
        y_position_week_info_bar = 20
        y_position_calendar = 70
        y_position_select_date_widget = 400


        # 将控件水平居中
        x_space_calendar = int((self.h_width-self.calendar.h_width)/2)
        self.calendar.move(x_space_calendar,y_position_calendar)

        x_space_week_info_bar = int((self.h_width-self.week_info_bar.h_width)/2)
        self.week_info_bar.move(x_space_week_info_bar, y_position_week_info_bar)

        x_space_select_date_widget = int((self.h_width-self.select_date_widget.h_width)/2)
        self.select_date_widget.move(x_space_select_date_widget, y_position_select_date_widget)


class Calendar(QFrame):
    to_tag=False

    # 基础属性
    h_height = 350
    h_width = 500

    layout_space = None

    date_controller = None

    # 控件列表
    date_weight_list = None

    # 自定义信号
    date_selected = pyqtSignal(DateController)

    selected_date = None

    def __init__(self,parent, date_controller):
        super().__init__()


        # 初始化calendar及成员
        self.setParent(parent)
        self.cal=QCalendarWidget(self)
        self.date_controller = date_controller

        self.count=0

        self.selected_date = copy.deepcopy(self.date_controller)

        self.date_weight_list=[]

        # 初始化布局
        self.grid=QGridLayout()
        self.setLayout(self.grid)

        # 初始化ui
        self.init_ui()
        # self.show()
        self.cal.hide()

        # 初始化日历参数
        self.refresh_calendar()

    # 初始化布局
    def init_ui(self):
        # 设定id
        self.setObjectName('calendar_background')
        # 调整自己控件大小
        self.resize(self.h_width,self.h_height)

        # 布局35个按钮
        count=42
        while(count>0):#放入35个块
            date_block=DateWidget(self)
            # 绑定信号
            date_block.h_date_button.button_clicked.connect(self.refresh_date_controller)
            date_block.h_date_button.clicked.connect(self.refresh_selected_button)
            self.date_weight_list.append(date_block)
            count-=1
        positions = [(i, j) for i in range(6) for j in range(7)]
        for position,date in zip(positions,self.date_weight_list):  # 在两个序列按顺序取出，然后组合
            self.grid.addWidget(date, *position)

        self.layout_space = self.grid.spacing()

        # 布局后刷新按钮大小
        self.refresh_date_widget_size()

    # 槽函数
    def refresh_date_controller(self, day):
        if day != 0:
            self.date_controller.day = day
            date = datetime.date(datetime(year=self.date_controller.year,month=self.date_controller.month,day=day))
            self.date_controller.weekday =  date.weekday()
            self.selected_date = copy.deepcopy(self.date_controller)
            self.emit_date_selected()


    def emit_date_selected(self):
        self.date_selected.emit(self.date_controller)

    def refresh_date_widget_size(self):
        button_width = self.h_width/7 - self.layout_space*2
        button_height = self.h_height/6 - self.layout_space*2

        for temp_date_widget in self.date_weight_list:
            temp_date_widget.refresh_size(button_width, button_height)

    # 刷新日历
    def refresh_calendar(self):

        # 清空所有按钮中的文字
        for button in self.date_weight_list:
            button.h_date_button.text_label.setText('')
            button.h_date_button.day = 0

        # 判断当前年月的1号是周几，确定日历的起始位置
        date = datetime.date(datetime(year=self.date_controller.year,month=self.date_controller.month,day=1))
        week_number = date.weekday()  # 0-6

        # 获取当前年月的天数
        days = self.month_to_days()

        for i in range(week_number,week_number+days):
            self.date_weight_list[i].h_date_button.text_label.setText(str(i+1-week_number))
            self.date_weight_list[i].h_date_button.day = i+1-week_number
            self.date_weight_list[i].h_date_button.month = self.date_controller.month
            self.date_weight_list[i].h_date_button.year = self.date_controller.year

        # 标出选中的日期
        self.refresh_selected_button()

    def refresh_selected_button(self):
        for button in self.date_weight_list:
            if button.h_date_button.day == self.selected_date.day and button.h_date_button.month == self.selected_date.month and button.h_date_button.year == self.selected_date.year:
                if (not self.to_tag):
                    self.to_tag = True
                    return
                button.h_date_button.chosen()
            else:
                button.h_date_button.not_chosen()

    def change_chosen(self):
        for button in self.date_weight_list:
            if button.h_date_button.day == self.selected_date.day and button.h_date_button.month == self.selected_date.month and button.h_date_button.year == self.selected_date.year:
                button.h_date_button.not_chosen()
                self.to_tag=False

    def is_leap_year(self):
        if self.date_controller.year%4==0 and self.date_controller.year%100!=0:
            return True
        else:
            return False

    # 判断一个月有多少天。
    def month_to_days(self):
        if self.date_controller.month== 1 or self.date_controller.month == 3 or self.date_controller.month == 5 or self.date_controller.month == 7 or self.date_controller.month == 8 or self.date_controller.month == 10 or self.date_controller.month == 12:
            return 31
        elif self.date_controller.month == 4 or self.date_controller.month == 6 or self.date_controller.month == 9 or self.date_controller.month == 11:
            return 30
        elif self.is_leap_year():
            return 29
        else:
            return 28

    def increase_month(self):
        self.date_controller.month+=1
        if self.date_controller.month == 13:
            self.date_controller.month = 1
            self.date_controller.year+=1
        self.refresh_calendar()

    def decrease_month(self):
        self.date_controller.month-=1
        if self.date_controller.month == 0:
            self.date_controller.month = 12
            self.date_controller.year-=1
        self.refresh_calendar()


class DateButton(QPushButton):

    date_info = None # 用于保存时间信息
    year = None
    month = None
    day = None

    button_clicked = pyqtSignal(int)

    image_path = 'data/ui/habit/calendar_selected.png'
    transport_image_path = 'data/ui/habit/calendar_not_selected.png'

    text_label = None
    image_label = None
    image_button = None

    def __init__(self):
        super().__init__()

        # 初始化控件
        self.image_label = QLabel(self)
        self.text_label = QLabel(self)
        self.image_button = QLabel(self)

        self.clicked.connect(self.button_clicked_function)

        self.init_ui()

    def init_ui(self):
        # self.show()

        # 设定id
        self.image_label.setObjectName('calendar_date_image_label')
        self.text_label.setObjectName('calendar_date_text_label')
        self.text_label.setProperty('class','calendar_date_font')
        self.image_button.setObjectName('calendar_date_image_button')

        # 调整大小
        self.image_label.resize(40,40)
        self.image_button.resize(40,40)
        self.text_label.resize(20,40)

        # 调整布局
        self.text_label.move(15,0)

    def button_clicked_function(self):
        self.button_clicked.emit(self.day)


    def chosen(self):
        self.image_label.show()
        self.image_label.setText('√')

    def not_chosen(self):
        self.image_label.hide()
        self.image_label.setText('')



class DateWidget(QFrame):
    # widget内部的button
    h_date_button = None

    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        # 初始化widget的属性
        self.show()

        # 初始化button
        self.h_date_button = DateButton()
        self.h_date_button.setParent(self)

        # 舒适化ui
        self.init_ui()

    def init_ui(self):
        # 设定id
        self.setObjectName('calendar_date_widget')
        self.h_date_button.setObjectName('calendar_date_button')

    def refresh_size(self, width, height):

        self.h_date_button.resize(width, height)


class SelectButton(QPushButton):
    # 基础属性
    h_height = 60
    h_width = 60

    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.resize(self.h_width, self.h_height)
        # self.show()


class DateInfoButton(QPushButton):

    # 基础属性
    h_width = 80
    h_height = 60

    info_type = None
    info_value = None

    def __init__(self,parent,info_type,info_value):
        super().__init__()

        #初始化按钮
        self.setParent(parent)
        self.info_type = info_type
        self.info_value = info_value

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.resize(self.h_width,self.h_height)
        # self.show()

        self.setProperty('class','calendar_selected_info_font')

    def refresh_info(self, info_value):
        self.info_value = info_value
        self.setText(str(self.info_value)+str(self.info_type))


class SelectDateWidget(QFrame):

    # 基础属性
    h_height = 120
    h_width = 500

    date_controller = None

    # 基础控件
    add_button = None
    subtract_button = None
    year_button = None
    month_button = None

    def __init__(self, parent, date_controller):
        super().__init__()
        self.setParent(parent)
        self.date_controller = date_controller

        # 初始化控件
        self.add_button = SelectButton(self)
        self.subtract_button = SelectButton(self)
        self.add_button.setText('>')
        self.subtract_button.setText('<')
        self.year_button = DateInfoButton(self,'年',self.date_controller.year)
        self.month_button = DateInfoButton(self, '月', self.date_controller.month)

        # 初始化ui
        self.init_ui()
        self.refresh_date_info()

    def init_ui(self):
        self.resize(self.h_width, self.h_height)
        self.show()

        # 设定id
        self.setObjectName('calendar_select_date_widget')
        self.add_button.setObjectName('calendar_select_date_widget_add_button')
        self.subtract_button.setObjectName('calendar_select_date_widget_subtract_button')
        self.year_button.setObjectName('calendar_select_date_widget_year_button')
        self.month_button.setObjectName('calendar_select_date_widget_month_button')

        # 布局
        x_space = int((self.h_width - 2*self.year_button.h_width - 2*self.add_button.h_width)/7)
        y_space = int(( self.h_height - self.add_button.h_height)/2)

        self.add_button.move(6*x_space+self.add_button.h_width+2*self.year_button.h_width, y_space)
        self.subtract_button.move(x_space,y_space)

        self.year_button.move(3*x_space+self.add_button.h_width,y_space)
        self.month_button.move(4*x_space+self.add_button.h_width+self.year_button.h_width,y_space)

    def refresh_date_info(self):
        self.year_button.refresh_info(self.date_controller.year)
        self.month_button.refresh_info(self.date_controller.month)


class WeekLabel(QLabel):
    # 基础属性
    h_width = 40
    h_height = 40

    def __init__(self, parent, week_info):
        super().__init__()
        self.setParent(parent)

        # 初始化属性
        self.week_info = week_info

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.resize(self.h_width, self.h_height)
        self.setText(self.week_info)
        # self.show()

        # 设定id
        self.setObjectName('calendar_week_label')
        self.setProperty('class','calendar_week_info_font')


class WeekInfoBar(QFrame):
    # 基础属性
    h_height = 40
    h_width = 500

    label_list = None

    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        self.label_list=[]

        # 初始化标签
        for i in range(7):
                self.label_list.append(WeekLabel(self, week_info_list[i]))

        # 初始化ui
        self.init_ui()

    def init_ui(self):


        x_space = int((self.h_width-7*self.label_list[0].h_width)/8)
        y_space = int((self.h_height-self.label_list[0].h_height)/2)

        for i in range(7):
            self.label_list[i].move(x_space+i*(x_space+self.label_list[0].h_width),y_space)

        # self.show()

        # 设定id
        self.setObjectName('calendar_week_info_bar')