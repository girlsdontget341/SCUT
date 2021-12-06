import datetime
from PyQt5.QtCore import QPointF, Qt, QDateTime
from PyQt5.QtWidgets import QGraphicsView
from dbcontroller.dbcontroller import  dbcontrolle
from PyQt5.QtChart import QChartView, QLineSeries, QChart, QDateTimeAxis, QValueAxis

X_MAX_NUM=6
Y_MAX_NUM=6
class line_chart(QChartView):
    #是否选择时间
    is_selected=False
    #x轴起始时间  终止时间
    start_time=None
    end_time=None
    #chart()子对象
    pchart=None
    #已经加入折线的id
    id_list=[]
    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        #抗锯齿
        self.setRenderHint(True)
        self.pchart=QChart()
        self.pchart.setAnimationOptions(QChart.SeriesAnimations)
        self.setChart(self.pchart)

        self.start_time="1970-01-01"
        self.end_time="2030-01-01"
        #设置x轴
        self.x_axis=x_axis()
        self.x_axis.set_property(self.start_time,self.end_time)
        self.pchart.setAxisX(self.x_axis)
        #设置y轴
        self.y_axis=y_axis()
        self.y_axis.set_property(0.5,3.5)
        self.pchart.setAxisY(self.y_axis)

        self.init_ui()

    def add_new_series(self,id):
        self.pchart.zoomReset()
        #导入数据库
        db = dbcontrolle()
        if(self.is_selected):
            data_list=db.get_old_history_message(id,self.start_time,self.end_time)
            #增加折线
            series=pseries(id)
            series.set_point(data_list)

            #增加曲线 增加x轴 增加y轴 为了使坐标轴和点对齐
            self.pchart.addSeries(series)
            self.pchart.setAxisX(self.x_axis,series)
            self.pchart.setAxisY(self.y_axis,series)

            message_data={
                'ID':id,
                'series':series
            }
            #id
            for message in self.id_list:
                if(id==message['ID']):
                    message['series']=series
                    return
            self.id_list.append(message_data)
        else:
            #这里没有选择日期 所以以格林日期为准确
            data_list=db.get_old_history_message(id,"1970-01-01",datetime.datetime.now())
            #开始寻找日期
            start_datetime=datetime.datetime(int(self.start_time[0:4]),int(self.start_time[5:7]),int(self.start_time[8:10]))

            #结束寻找日期
            end_datetime=datetime.datetime(int(self.end_time[0:4]),int(self.end_time[5:7]),int(self.end_time[8:10]))

            #first_time 旧日期
            first_time = data_list[0]['date']
            first_datetime = datetime.datetime(int(first_time[0:4]), int(first_time[5:7]), int(first_time[8:10]))

            #last_time 新日期
            last_time=data_list[len(data_list)-1]['date']
            last_datetime= datetime.datetime(int(last_time[0:4]), int(last_time[5:7]), int(last_time[8:10]))

            #没有曲线时的显示
            if(self.start_time=="1970-01-01"):
                #开始时间
                self.start_time=first_time
                self.end_time=last_time

                print(self.start_time,last_time)
                #改变坐标轴
                self.change_x_axis(self.start_time,self.end_time)
                series = pseries(id)
                series.set_point(data_list)
                self.pchart.addSeries(series)
                self.pchart.setAxisX(self.x_axis, series)
                self.pchart.setAxisY(self.y_axis, series)


                message_data = {
                    'ID': id,
                    'series': series
                }
                # id

                self.id_list.append(message_data)
                return

            else:
                if(len(self.id_list)!=0):
                    if(first_datetime<start_datetime):
                        self.start_time=first_time
                    if(last_datetime>end_datetime):
                        self.end_time=last_time
                else:
                    print(self.start_time, last_time)
                    self.start_time = first_time
                    self.end_time = last_time


                self.change_x_axis(self.start_time,self.end_time)
                self.pchart.removeAllSeries()

                # 增加折线
                series = pseries(id)
                series.set_special_point(data_list,self.start_time)
                self.pchart.addSeries(series)
                self.pchart.setAxisX(self.x_axis, series)
                self.pchart.setAxisY(self.y_axis, series)

                message_data = {
                    'ID': id,
                    'series': series
                }
                #将旧的曲线标准化
                for message in self.id_list:
                    ID=message['ID']
                    data_list = db.get_old_history_message(ID, self.start_time, self.end_time)
                    series = pseries(ID)
                    message['series']=series
                    series.set_special_point(data_list, self.start_time)
                    self.pchart.addSeries(series)
                    self.pchart.setAxisX(self.x_axis, series)
                    self.pchart.setAxisY(self.y_axis, series)


                # id
                self.id_list.append(message_data)


    def get_id(self,id):
        print("折线图"+id)
        for message in self.id_list:
            if(id==message['ID']):
                self.pchart.removeSeries(message['series'])
                self.id_list.remove(message)
                return
        if(len(self.id_list)<=3):
            self.add_new_series(id)

    def get_time(self,start_time,end_time):
        self.change_x_axis(start_time,end_time)
        self.is_selected=True
        self.pchart.removeAllSeries()
        for message in self.id_list:
            self.add_new_series(message['ID'])

    def change_x_axis(self,start_time,end_time):
        self.start_time=start_time
        self.end_time=end_time
        self.pchart.removeAxis(self.x_axis)
        self.x_axis=x_axis()
        self.x_axis.set_property(start_time,end_time)
        self.pchart.setAxisX(self.x_axis)


    def change_y_axis(self):
        pass

    def init_ui(self):
        self.resize(1200,700)

    # def mouseMoveEvent(self, event):
    #     s = event.windowPos()
    #     self.setMouseTracking(True)
    #     x = s.x()
    #     y = s.y()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Space:
            self.pchart.zoomIn()
        elif event.key() == Qt.Key_Escape:
            self.pchart.zoomReset()
        elif event.key() == Qt.Key_Left:
            self.pchart.scroll(-10, 0)
        elif event.key() == Qt.Key_Right:
            self.pchart.scroll(10, 0)
        elif event.key() == Qt.Key_Up:
            self.pchart.scroll(0, 10)
        elif event.key() == Qt.Key_Down:
            self.pchart.scroll(0, -10)
        else:
            QGraphicsView.keyPressEvent(self, event)


class x_axis(QDateTimeAxis):

    def __init__(self):
        super(x_axis, self).__init__()

    #dict=[{'date':'','change':''}]
    def set_property(self,start_time,end_time):
        first_datetime = QDateTime.fromString(start_time, "yyyy-MM-dd")
        last_datetime = QDateTime.fromString(end_time, "yyyy-MM-dd")
        # day=(last_datetime-first_datetime).days
        #设置x轴最大值 以及最小值
        self.setMin(first_datetime)
        self.setMax(last_datetime)
        self.setTickCount(X_MAX_NUM)
        self.setFormat("yyyy-MM-dd")
    
class y_axis(QValueAxis):
    
    def __init__(self):
        super(y_axis, self).__init__()
        # self.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)

    def set_property(self,min,max):
        self.setMin(min)
        self.setMax(max)
        self.setMinorTickCount(4)
        self.setTickCount(7)

class pseries(QLineSeries):

    def __init__(self,id):
        super(pseries, self).__init__()
        self.setName(id)

    def set_point(self,data_list):
        if(data_list==[]):
            return
        point_list=[]
        for item in data_list:
           time= QDateTime.fromString(item['date'], "yyyy-MM-dd")
           point=QPointF(time.toMSecsSinceEpoch(),item['net_worth'])
           point_list.append(point)

        self.append(point_list)

    def set_special_point(self,data_list,first_time):
        point_list = []
        for item in data_list:
            time = QDateTime.fromString(item['date'], "yyyy-MM-dd")
            point = QPointF(time.toMSecsSinceEpoch(), item['net_worth'])
            point_list.append(point)

            point_list.append(point)
        self.append(point_list)



