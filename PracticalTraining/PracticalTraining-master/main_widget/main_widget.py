import datetime
import json
import uuid
from os.path import dirname, abspath
from PyQt5.QtCore import QBasicTimer, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QProgressBar, QLabel
from dbcontroller.dbcontroller import dbcontrolle
from main_widget.calendar_widget import MyDayCalendar
from visualization.line_chart import line_chart
from visualization.data_form import data_form
from main_widget.listbox import ListBox
from grabqieman.Grab import  MultiGrab
from grabdanjuan.Grab import MultiGrabDJ
PATH=dirname(dirname(abspath(__file__))) +"/data/time.json"

class main_widget(QFrame):
    height=900
    width=1600

    pcalendar=None
    pline_chart=None
    plist_box=None
    data_form=None

    def __init__(self):
        super(main_widget, self).__init__()
        self.pcalendar=MyDayCalendar()
        self.pline_chart=line_chart(self)
        self.data_form=data_form(self)
        self.plist_box=ListBox(self,self.pline_chart,self.data_form)
        self.calendar_button=calendar_button(self)
        self.ok_button=ok_button(self)

        #绑定槽函数
        self.calendar_button.clicked.connect(self.pcalendar.show)
        self.ok_button.clicked.connect(self.update_message)
        self.pcalendar._select_datetime_signal.connect(self.pline_chart.get_time)
        self.pcalendar._select_datetime_signal.connect(self.data_form.get_time)
        self.init_ui()

        self.init_data()

        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
        mac_address = '-'.join([mac_address[i:i + 2] for i in range(0, 11, 2)])
        dbcontrolle().insert_into_user(mac_address)
        self.show()

    def update_message(self):
        self.updwidget = UpdWidget()
        MultiGrab( self.updwidget).start()
        MultiGrabDJ( self.updwidget).start()

        # mythread = MyThread()
        # mythread.start()



    def init_data(self):
        now=datetime.datetime.now()
        nowtime=datetime.datetime(now.year,now.month,now.day)
        nowtime_str=nowtime.strftime("%Y-%m-%d")


        try:
            with open(PATH, 'r') as fp:
                data = json.load(fp)
                time=data['time']

                time=datetime.datetime.strptime(time, '%Y-%m-%d')
                print(time)
        except:
            data = {
                'time': nowtime_str
            }
            try:
                with open(PATH, 'w') as pf:
                    json.dump(data, pf)
            except IOError as e:
                pass
            return
        if((nowtime-time).days>0):
            self.update_message()
        data={
            'time':nowtime_str
        }
        try:
            with open(PATH, 'w') as pf:
                json.dump(data, pf)
        except IOError as e:
            pass

    def init_ui(self):
        self.calendar_button.move(1200,0)
        self.ok_button.move(1400,0)
        self.data_form.move(0,700)
        self.plist_box.move(1200,50)
        self.resize(self.width,self.height)
        self.setWindowTitle("投资组合评比器")

    def __del__(self):
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
        mac_address = '-'.join([mac_address[i:i + 2] for i in range(0, 11, 2)])
        for i in self.plist_box.pid_list:
            dict_list = {
                'M_ID': mac_address,
                'PID':i
            }
            print(dict_list)
            dbcontrolle().insert_into_user_record(dict_list)




class calendar_button(QPushButton):

    def __init__(self,parent):
        super(calendar_button, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.resize(200,50)
        self.setText('日历')


class ok_button(QPushButton):

    def __init__(self,parent):
        super(ok_button, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.resize(200,50)
        self.setText('更新')


# 更新进度条窗口
class UpdWidget(QWidget):
    def __init__(self):
        super(UpdWidget, self).__init__()
        self.pbar = QProgressBar(self)
        self.info = QLabel(self)
        self.timer = QBasicTimer()
        self.step = 0
        self.signal = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(500, 180)
        self.setWindowTitle('正在更新')
        self.info.setGeometry(165, 30, 200, 30)
        self.info.setText("正在更新数据，请稍等...")
        self.pbar.setGeometry(100, 90, 330, 30)
        self.timer.start(100, self)
        self.show()

    def add_signal(self):
        self.signal+=1

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            print('更新已经全部完成')
            self.close()
        if self.signal < 6 and self.step < 99:
            self.step = self.step + 0.05
            self.pbar.setValue(self.step)
        if self.signal >= 6:
            self.step = 100
            self.pbar.setValue(self.step)







