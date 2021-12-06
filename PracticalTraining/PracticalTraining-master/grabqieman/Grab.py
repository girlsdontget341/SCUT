import threading
from os.path import dirname, abspath
from PyQt5.QtWidgets import QMessageBox
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dbcontroller.dbcontroller import dbcontrolle
import json
import time
import datetime

#模仿browsermob-proxy.bat代理的路径
# PROXY_ADDRESS_PATh="../browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
# PROXY_ADDRESS="F:\PracticalTraining\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat"
PROXY_ADDRESS=dirname(dirname(abspath(__file__))) +"/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
#chromedriver可执行的浏览器的放置位置
# EXECUTABLE_PATH="F:\PracticalTraining\chromedriver.exe"
# EXECUTABLE_PATH="..\chromedriver.exe"



class GrabQM():
    def __init__(self,url_list):
        self.url_list=url_list

    def get_one_history_message(self,url):
        # 开启代理
        BMPserver = Server(PROXY_ADDRESS)
        BMPserver.start()
        BMPproxy = BMPserver.create_proxy()

        # 配置代理启动webdriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--proxy-server={}'.format(BMPproxy.proxy))
        brosver = webdriver.Chrome( options=chrome_options)

        BMPproxy.new_har("lagou", options={'captureContent': True, 'captureContent': True})

        try:
            print('现在'+url)
            data_dict_list = []
            # 模拟浏览器
            brosver.get(url)
            id=url[30:]
            # find_url = re.compile('https://qieman.com/pmdj/v1/pomodels/(.*?)/nav-history')
            result = BMPproxy.har
            time.sleep(2)
            for entry in result['log']['entries']:
                entry_url = entry['request']['url']
                if entry_url == 'https://qieman.com/pmdj/v1/pomodels/'+id+'/nav-history':
                # if find_url.findall(entry_url) !=[]:
                    # 获取接口返回内容
                    _response = entry['response']
                    _content = _response['content']
                    try:
                        content=json.loads(_content['text'])
                        for item in content:
                            data_dict = {
                                'ID': '',
                                'date': '',
                                'change': '',
                                'net_worth': ''
                            }
                            timeStamp = int(item['navDate'])
                            timeStamp /= 1000.0
                            timearr = time.localtime(timeStamp)
                            otherStyleTime = time.strftime("%Y-%m-%d", timearr)
                            data_dict['ID']=id
                            data_dict['date']=otherStyleTime
                            data_dict['change']=item["dailyReturn"]
                            data_dict['net_worth']=item["nav"]
                            if(data_dict not in data_dict_list):
                                data_dict_list.append(data_dict)
                    except Exception:
                        print('')
            return data_dict_list
        except Exception:
            print("爬取且慢历史记录错误")

    def update_one_history_message(self,url,new_date):
        BMPserver = Server(PROXY_ADDRESS)
        BMPserver.start()
        BMPproxy = BMPserver.create_proxy()

        # 配置代理启动webdriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--proxy-server={}'.format(BMPproxy.proxy))
        brosver = webdriver.Chrome(options=chrome_options)

        BMPproxy.new_har("lagou", options={'captureContent': True, 'captureContent': True})

        try:
            print('现在' + url)
            data_dict_list = []
            # 模拟浏览器
            brosver.get(url)
            id = url[30:]
            # find_url = re.compile('https://qieman.com/pmdj/v1/pomodels/(.*?)/nav-history')
            result = BMPproxy.har
            time.sleep(2)
            for entry in result['log']['entries']:
                entry_url = entry['request']['url']
                if entry_url == 'https://qieman.com/pmdj/v1/pomodels/' + id + '/nav-history':
                    # if find_url.findall(entry_url) !=[]:
                    # 获取接口返回内容
                    _response = entry['response']
                    _content = _response['content']
                    try:
                        content = json.loads(_content['text'])
                        content.reverse()
                        for item in content:
                            data_dict = {
                                'ID': '',
                                'date': '',
                                'change': '',
                                'net_worth': ''
                            }
                            timeStamp = int(item['navDate'])
                            timeStamp /= 1000.0
                            timearr =  datetime.datetime.fromtimestamp(timeStamp)
                            otherStyleTime =timearr.strftime('%Y-%m-%d')
                            data_dict['ID'] = id
                            data_dict['date'] = otherStyleTime
                            data_dict['change'] = item["dailyReturn"]
                            data_dict['net_worth'] = item["nav"]
                            if (data_dict not in data_dict_list and timearr>new_date):
                                data_dict_list.append(data_dict)
                            else:
                                return data_dict_list
                    except Exception:
                        print('爬取历史记录错误')
            return data_dict_list
        except Exception:
            print("爬取且慢历史记录错误")


    def get_one_base_message(self,url):
        #隐藏浏览器启动
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(url)
    # 获取基金信息
        data_dict={
            "ID":'',
            "name":'',
            "change":0,
            "net_worth":0,
            "max_drawdown":0,
            "annualized_yield": 0,
            "annualized_volatility":0,
            "sharpe_ratio":0
        }
    # 获取基金名字
        time.sleep(0.5)
        try:
            name = driver.find_element_by_xpath('//div[@class="qm-header qm-header-1"]').text
            data_dict['name']=name
        except Exception:
            print("爬取且慢基金信息错误")

        # 获取基金ID
        try:
            id = driver.find_element_by_xpath('//span[@class="item"]').text
            data_dict['ID']=id
        except Exception:
            print("爬取基金ID错误")

        try:
            net_worth=driver.find_element_by_xpath('//span[@class="qm-amount qm-amount-std"]').text
            data_dict["net_worth"]=float(net_worth)
        except:
            print("爬取基金净值错误")


        try:
            change=driver.find_element_by_xpath('//div[@class="daily-profilt"]//span[@class="qm-percent qm-percent-std qm-up"]').text
            data_dict["change"]=float(change.strip('%'))
            data_dict["annualized_yield"] = data_dict["change"] * 365
        except:
            try:
                change = driver.find_element_by_xpath('//div[@class="daily-profilt"]//span[@class="qm-percent qm-percent-std qm-down"]').text
                data_dict["change"] = float(change.strip('%'))
                data_dict["annualized_yield"] = data_dict["change"] * 365
            except:
                print("爬取基金涨跌错误")

        try:
            i = 0
            for data in driver.find_elements_by_xpath('//div[@class="label-data"]//span[@class="qm-percent qm-percent-std"]'):
                # 获取最大回撤
                if (i == 0):
                    #.strip('%')
                    max_drawdown = data.text
                    data_dict["max_drawdown"]=float(max_drawdown.strip('%'))
                # 获取年华波动率
                if (i == 1):
                    annualized_volatility = data.text
                    data_dict["annualized_volatility"]=float(annualized_volatility.strip('%'))
                i+=1
        except Exception:
            print("爬取最大回撤或者年化波动率错误")


        try:
            # 获取夏普比率
            sharpe_ratio =driver.find_element_by_xpath('//div[@class="label-data"]//span[@class="qm-amount qm-amount-std"]').text
            data_dict["sharpe_ratio"]=float(sharpe_ratio)
        except Exception:
            print("爬取夏普比率错误")
        return data_dict

    def update_base_message(self):
        db=dbcontrolle()
        for url in self.url_list:
            db.update_portfolio(self.get_one_base_message(url))


    def get_base_message(self):
        db=dbcontrolle()
        for url in self.url_list:
            message=self.get_one_base_message(url)
            if(message['name']==''):
                return False
            db.insert_data_into_portfolio(self.get_one_base_message(url))
        return True


    def get_history_message(self):
        c = dbcontrolle()
        for url in self.url_list:
            c.insert_data_into_record(self.get_one_history_message(url))

    def update_history_message(self):
        db=dbcontrolle()
        for url in self.url_list:
            new_date = db.get_new_date(url[30:])
            db.insert_data_into_record(self.update_one_history_message(url,new_date))

    #需要持仓库的ID,所占比例 以及名字
    def get_one_position(self,url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(url)
        # 获取基金信息
        data=[]

        time.sleep(0.5)

        try:
            id_list = driver.find_elements_by_xpath('//span[@class="text-muted"]')
            for id in id_list:
                data_dict = {
                    "PID":url[30:],
                    "ID": '',
                    "name": '',
                    "percent": 0
                }
                data_dict['ID']=id.text
                data.append(data_dict)
        except Exception:
            print("爬取且慢基金信息错误")


        try:
            name_list = driver.find_elements_by_xpath('//span[@class="text-muted"]/../span[2]')
            i=0
            for name in name_list:
                data[i]['name']=name.text
                i+=1
                # data_dict['name']=name.text
        except Exception:
            print("爬取且慢基金名字错误")


        try:
            percent_list = driver.find_elements_by_xpath('//div[@class="comp-item clearfix"]//p[@class="percent"]//span')
            i=0
            for percent in percent_list:
                data[i]['percent'] = float(percent.text)
                i += 1
                # data_dict['name']=name.text
        except Exception:
            print("爬取且慢基金比率错误")

        return data


    def get_position(self):
        db=dbcontrolle()
        for url in self.url_list:
            db.insert_into_position(self.get_one_position(url))


class Grap_Thread(threading.Thread):
    count=0
    def __init__(self,url_list,thread_id,upwidget):
        super(Grap_Thread, self).__init__()
        self.grap=GrabQM(url_list)
        self.ID=thread_id
        self.url_list=url_list
        self.upwidget=upwidget


    def run(self):
        try:
            print(self.ID,"线程开始")
            self.grap.update_base_message()
            self.grap.update_history_message()
            self.upwidget.signal += 1
            print(self.ID,"线程结束",self.upwidget.signal)
        except:
            print("更新失败")


class MultiGrab():
    base_url='https://qieman.com/portfolios/'
    url_list=[]

    THREAD_NUM=14
    thread_list=[]
    def __init__(self,updwidget=None):
        if updwidget !=None:
            self.upwidget=updwidget

    def start(self):
        self.init_url_list()
        cha= len(self.url_list)/self.THREAD_NUM
        for i in range(0,self.THREAD_NUM):
            if(i==(self.THREAD_NUM-1)):
                thread=Grap_Thread(self.url_list[int(i*cha):],i,self.upwidget)
                self.thread_list.append(thread)
            else:
                thread=Grap_Thread(self.url_list[int(i*cha):int((i+1)*cha)],i,self.upwidget)
                self.thread_list.append(thread)
        for i in self.thread_list:
            i.start()

    def init_url_list(self):
        id_list=dbcontrolle().get_all_id()
        for id in id_list:
            self.url_list.append(self.base_url+id)

    def add_new_jj(self,PID):
        url_list=[]
        url_list.append(self.base_url+PID)
        try:
            grab=GrabQM(url_list)
            if not grab.get_base_message():
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '输入不符合规范 添加失败')
                msg_box.exec_()
                return False
            grab.get_history_message()
            grab.get_position()
        except:
            # print("添加失败")
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '输入不符合规范 添加失败')
            msg_box.exec_()
            return False
        return  True


