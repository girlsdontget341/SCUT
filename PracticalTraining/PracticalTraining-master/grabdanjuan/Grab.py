import threading
import urllib.request
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
import requests
from  dbcontroller.dbcontroller  import dbcontrolle

#浏览器处于的位置
# EXECUTABLE_PATH="F:\PracticalTraining\chromedriver.exe"


class GrabDJ():

    def __init__(self,url_list,base_url_list,position_url_list):
        self.url_list=url_list
        self.base_url_list=base_url_list
        self.position_url_list=position_url_list

    #获取历史净值以及日涨跌
    def get_history_message(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }

        data_dict_list=[]
        for url in self.url_list:
            data_dict_list.clear()
            i = 1
            #获取id
            id=url[46:]
            while (True):
                curl = url + "?size=500&page=" + str(i)
                req = urllib.request.Request(curl, headers=header)
                res = urllib.request.urlopen(req)
                res.encoding = 'utf-8'
                bs = BeautifulSoup(res, "html.parser")
                message_list = json.loads(bs.text)
                message_list = message_list["data"]["items"]
                if (message_list == []):
                    break
                for message in message_list:
                    try:
                        data_dict = {
                            'ID': '',
                            'date': '',
                            'change': '',
                            'net_worth': ''
                        }
                        data_dict["ID"]=id
                        data_dict["date"]=message["date"]
                        #涨跌幅度
                        data_dict["change"]=float(message["percentage"])
                        #净值
                        data_dict["net_worth"]=float(message["nav"])
                        data_dict_list.append(data_dict)
                    except Exception:
                        print(None)
                i += 1
            c=dbcontrolle()
            c.insert_data_into_record(data_dict_list)

    #获取系统自带的最大回撤 夏普比 以及年化波动率
    #如果出现错误 可能是网络不稳定导致dom 还没执行导致报错
    def get_one_base_message(self,url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        #获取基金信息
        data_dict={
            "ID":'',
            "name":'',
            "change":0,
            "net_worth":0,
            "max_drawdown":0,
            "annualized_yield":0,
            "annualized_volatility":0,
            "sharpe_ratio":0
        }

        time.sleep(1)
        #获取基金名字
        data_dict['name']=driver.find_element_by_xpath('//div[contains(@class, "flex-between")]//span[@class="title"]').text

        #获取基金ID
        data_dict['ID']=driver.find_element_by_xpath('//div[@class="header-code"]').text

        #今日涨跌幅
        change=driver.find_element_by_xpath('//li[@class="box"]//div[contains(@class, "value")]').text
        data_dict["change"]=float(change.strip('%'))
        data_dict["annualized_yield"]=data_dict["change"]*365
        #
        #今日净值
        net_worth=driver.find_element_by_xpath('//li[@class="box"]//div[@class="value"]').text
        data_dict["net_worth"]=float(net_worth)


        i=0
        for data in driver.find_elements_by_xpath('//ul[@class="datas"]//li//div[@class="middle"]'):
            #获取最大回撤
            if(i==0):
                max_drawdown=data.text
                data_dict["max_drawdown"]=float(max_drawdown.strip('%'))
            #获取年化波动率
            if(i==1):
                annualized_volatility=data.text
                data_dict["annualized_volatility"]=float(annualized_volatility.strip('%'))
            #获取夏普比率
            if(i==2):
                sharpe_ratio=data.text
                data_dict["sharpe_ratio"]=float(sharpe_ratio)
            i+=1
        return data_dict

    def update_one_history_message(self,url):
        # 获取id
        id = url[46:]
        db=dbcontrolle()
        new_date=db.get_new_date(id)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        data_dict_list = []
        i = 1


        while (True):
            curl = url + "?size=500&page=" + str(i)
            req = urllib.request.Request(curl, headers=header)
            res = urllib.request.urlopen(req)
            res.encoding = 'utf-8'
            bs = BeautifulSoup(res, "html.parser")
            message_list = json.loads(bs.text)
            message_list = message_list["data"]["items"]
            if (message_list == []):
                break
            for message in message_list:
                try:
                    data_dict = {
                        'ID': '',
                        'date': '',
                        'change': '',
                        'net_worth': ''
                    }
                    data_dict["ID"] = id
                    data_dict["date"] = message["date"]
                    date = datetime.strptime(data_dict["date"], '%Y-%m-%d')
                    # 涨跌幅度
                    data_dict["change"] = float(message["percentage"])
                    # 净值
                    data_dict["net_worth"] = float(message["nav"])
                    if(date>new_date):
                        data_dict_list.append(data_dict)
                    else:
                        db.insert_data_into_record(data_dict_list)
                        return
                except Exception:
                    print(None)
            i += 1

    def update_history_message(self):
        for url in self.url_list:
            self.update_one_history_message(url)

    def update_base_message(self):
        c = dbcontrolle()
        for url in self.base_url_list:
            c.update_portfolio(self.get_one_base_message(url))


    def get_base_message(self):
        c = dbcontrolle()
        for url in self.base_url_list:
            message=self.get_one_base_message(url)
            if(message['name']==''):
                return False
            c.insert_data_into_portfolio(message)
        return True

    #需要持仓库的ID,所占比例 以及名字
    def get_one_position(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37",
            "Accept": "application/json, text/plain, */*",
            "Host": "danjuanapp.com"
        }
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        s = s['data']['items']
        data_list=[]

        for i in range(0, len(s)):
            data_dict = {
                'PID': url[60:],
                'ID': '',
                'name': '',
                'percent': ''
            }
            if str(s[i]['percent']) != '0':
                data_dict['ID']=s[i]['fd_code']
                data_dict['name']=s[i]['fd_name']
                data_dict['percent']=float(s[i]['percent'])
                data_list.append(data_dict)

        return(data_list)

    def get_position(self):
        db = dbcontrolle()
        for url in self.position_url_list:
            db.insert_into_position(self.get_one_position(url))

class Grap_Thread(threading.Thread):
    count=0
    def __init__(self,url_list,base_url_list,position_url_list,thread_id,updwidget):
        super(Grap_Thread, self).__init__()
        self.grab=GrabDJ(url_list,base_url_list,position_url_list)
        self.ID=thread_id
        self.upwidget=updwidget

    def run(self):
        try:
            print(self.ID,"线程开始")
            self.grab.update_base_message()
            self.grab.update_history_message()
            self.upwidget.signal+=1
            print(self.ID,"线程结束",self.upwidget.signal)
        except:
            print("更新失败")



class MultiGrabDJ():
    url_list=[]
    base_url_list=[]
    position_url_list=[]

    history='https://danjuanapp.com/djapi/plan/nav/history/'
    base='https://danjuanapp.com/strategy/'
    position='https://danjuanapp.com/djapi/plan/position/detail?plan_code='

    def __init__(self,updwidget=None):
        if updwidget !=None:
            self.upwidget=updwidget


    def start(self):
        self.init_url()
        self.grab = Grap_Thread(self.url_list, self.base_url_list, self.position_url_list,0,self.upwidget)
        self.grab.start()

    def test(self):
        self.init_url()
        self.grab=GrabDJ(self.url_list,self.base_url_list,self.position_url_list)
        self.grab.get_position()

    def init_url(self):
        pid_list=dbcontrolle().get_dj_id()
        for pid in pid_list:
            self.url_list.append(self.history+pid)
            self.base_url_list.append(self.base+pid)
            self.position_url_list.append(self.position+pid)

    def add_new_jj(self,PID):
        url_list=[]
        base_url_list = []
        position_url_list = []
        url_list.append(self.history + PID)
        base_url_list.append(self.base + PID)
        position_url_list.append(self.position + PID)
        try:
            grab=GrabDJ(url_list,base_url_list,position_url_list)
            if not grab.get_base_message():
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '输入不符合规范 添加失败')
                msg_box.exec_()
                return False
            grab.get_history_message()
            grab.get_position()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '输入不符合规范 添加失败')
            msg_box.exec_()
            return False
        return True