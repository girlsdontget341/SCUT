import pymysql
import datetime

class dbcontrolle():
    #数据库连接
    conn=None
    #操作光标
    cur=None
    def __init__(self):
        # self.conn = pymysql.connect(host='121.5.167.31', port=3306, user='vulclone', passwd='1234', db='pt')
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='ssqssq', db='pt')
        self.cur = self.conn.cursor()

    def insert_data_into_record(self,data_dict_list):
        print("插入数据库的历史记录",len(data_dict_list))
        if(len(data_dict_list)==0):
            return
        for data_dict in data_dict_list:
            sql = "INSERT INTO record(PID,`date`, net_worth, `change`) VALUES (%s, %s, %s, %s)"
            data =(data_dict['ID'], data_dict['date'], data_dict['net_worth'], data_dict['change'])

            #
            try:
                # 执行sql语句
                self.cur.execute(sql,data)
                self.conn.commit()
                print("插入历史记录语句执行成功")
            except:
                # 发生错误时回滚
                self.conn.rollback()
                print("插入历史记录语句执行失败")

    def insert_data_into_portfolio(self,data_dict):
        sql = "INSERT INTO portfolio(PID,`name`,sharpe_ratio,annualized_volatility,max_drawdown,net_worth,`change`,annualized_yield) VALUES (%s, %s, %s, %s,%s, %s,%s,%s)"
        data = (data_dict['ID'], data_dict['name'],data_dict["sharpe_ratio"],data_dict["annualized_volatility"],data_dict["max_drawdown"], data_dict["net_worth"], data_dict["change"],data_dict["annualized_yield"])
        try:
        # 执行sql语句
            self.cur.execute(sql, data)
            # 提交到数据库执行
            self.conn.commit()
            print("插入投资组合成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("插入投资组合失败")

    #返回该ID的最新日期
    def get_new_date(self,id):
        sql="SELECT MAX(`date`)FROM record WHERE PID=%s"
        try:
            self.cur.execute(sql, id)
            # 获取所有记录列表
            results =  self.cur.fetchone()
            for date in results:
                print("获取数据成功",date)
                return date
        except:
            print("获取数据失败")

    def update_portfolio(self,data_dict):
        sql = "UPDATE portfolio SET sharpe_ratio=%s,annualized_volatility=%s,max_drawdown=%s,net_worth=%s,`change`=%s ,`annualized_yield`=%s WHERE PID=%s"
        data = (data_dict["sharpe_ratio"],data_dict["annualized_volatility"],data_dict["max_drawdown"], data_dict["net_worth"], data_dict["change"],data_dict['annualized_yield'],data_dict['ID'] )
        print(data)
        try:
        # 执行sql语句
            self.cur.execute(sql, data)
            # 提交到数据库执行
            self.conn.commit()
            print("更新成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("更新失败")

    #模仿上面语句 载入持仓数据
    def insert_into_position(self,data_dict_list):
        print("数据库那边", len(data_dict_list))
        for data_dict in data_dict_list:
            sql = "INSERT INTO `position`(ID,PID,`name`,`percents`) VALUES (%s, %s, %s,%s)"
            data = (data_dict['ID'], data_dict["PID"],data_dict['name'], data_dict['percent'])

            try:
            # 执行sql语句
                self.cur.execute(sql, data)
                self.conn.commit()
                print("sql语句执行成功")
            except:
                # 发生错误时回滚
                self.conn.rollback()
                print("sql语句执行失败")

    #模仿上面语句 更新持仓
    def update_position(self,data):
        sql = "UPDATE `position` SET `percents`=%s WHERE ID=%s"
        data = (data["percent"], data['ID'])
        try:
            # 执行sql语句
            self.cur.execute(sql, data)
            # 提交到数据库执行
            self.conn.commit()
            print(data)
            print("更新成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("更新失败")

    #根据 根据传入的id 以及时间 返回指定时间内的历史记录 start_time 和end_time是str型 但是 不妨碍直接使用
    #返回的是列表 这种形式的 #dict=[{'date':'','change':''}，{'date':'','change':''}]
    def get_old_history_message(self,id,start_time,end_time):
        sql = "select `date`,net_worth from record where `date` between %s and %s and PID=%s"
        data = (start_time, end_time, id)
        data_list=[]
        try:
            # 执行sql语句
            self.cur.execute(sql, data)
            for item in self.cur.fetchall():
                data_dict={
                    'date':item[0].strftime('%Y-%m-%d'),
                    'net_worth':item[1]
                }
                data_list.append(data_dict)
            return data_list
            print("获取成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("更新失败")

    def get_history_message(self,id,start_time,end_time):
        # self.is_select_time = True
        data_list = []
        sql = "select `date`,`change`,net_worth from record where `date` between %s and %s and PID=%s"
        data = (start_time, end_time, id)
        try:
            # 执行sql语句
            self.cur.execute(sql, data)
            if('CSI' in id):
                for item in self.cur.fetchall():
                    data_dict={
                        'date':item[0].strftime('%Y-%m-%d'),
                        'change': item[1],
                        'net_worth':item[2]
                    }
                    data_list.append(data_dict)
            else:
                for item in self.cur.fetchall():
                    data_dict={
                        'date':item[0].strftime('%Y-%m-%d'),
                        'change': item[1]*100,
                        'net_worth':item[2]
                    }
                    data_list.append(data_dict)
            return data_list
            print("获取成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("更新失败")

    #获取投资组合信息
    def get_portfolio_info(self):
        sql = "SELECT * FROM portfolio"
        try:
            self.cur.execute(sql)
            # 获取所有记录列表
            results = self.cur.fetchall()
            return results
        except:
            print("获取数据失败")

    def get_message(self,pid):
        data_list2=[]
        sql = "select `name`, `change`, annualized_yield, annualized_volatility, max_drawdown, net_worth, sharpe_ratio from portfolio where PID= %s"
        data = pid
        # self.get_name(id)
        try:
            self.cur.execute(sql, data)
            item = self.cur.fetchone()
            message = {
                'name': item[0],
                'change': item[1],
                'annualized_yield': item[2],
                'annualized-volatility': item[3],
                'max_drawdown': item[4],
                'net_worth': item[5],
                'sharpe_ratio': item[6]
            }
            data_list2.append(message)
            return data_list2
        except:
            print("获取数据失败")

    def get_name(self,pid):
        sql = "select `name` from portfolio where PID= %s"
        data = pid
        name_list=[]
        self.cur.execute(sql, data)
        item = self.cur.fetchone()
        name_dict = {
            'name': item[0]

        }
        name_list.append(name_dict)
        return name_list


    def get_user_record(self,M_ID):
        pid_list=[]
        sql = "SELECT * FROM user_record WHERE M_ID=%s"
        try:
            self.cur.execute(sql,M_ID)
            # 获取所有记录列表
            results = self.cur.fetchall()
            for i in results:
                pid_list.append(i[1])
            print(pid_list)
            return pid_list
        except:
            print("获取数据失败")

    def insert_into_user_record(self,data_dict):
        sql = "INSERT INTO `user_record`(M_ID,PID) VALUES (%s, %s)"
        data = (data_dict['M_ID'], data_dict['PID'])
        try:
            # 执行sql语句
            self.cur.execute(sql, data)
            self.conn.commit()
            print("sql语句执行成功")
            print(data)
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("sql语句执行失败")
            print(data)

    def delete_user_record(self,M_ID):
        sql = "DELETE FROM user_record WHERE M_ID= %s"

        try:
            # 执行sql语句
            self.cur.execute(sql, M_ID)
            self.conn.commit()
            print("删除语句执行成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("删除语句执行失败")

    def insert_into_user(self,M_ID):
        sql = "INSERT INTO `user`(ID) VALUES (%s)"
        try:
            # 执行sql语句
            self.cur.execute(sql, M_ID)
            self.conn.commit()
            print("sql语句执行成功")
        except:
            # 发生错误时回滚
            self.conn.rollback()
            print("sql语句执行失败")

    def get_all_id(self):
        PID_list=[]
        sql="SELECT PID FROM portfolio"

        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for item in results:
              if("ZH" in item[0]):
                  PID_list.append(item[0])
            return PID_list
            print("获取ID成功")
        except:
            print("获取ID失败")

    def get_dj_id(self):
        PID_list=[]
        sql="SELECT PID FROM portfolio"

        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for item in results:
              if("CSI" in item[0]):
                  PID_list.append(item[0])
            return PID_list
            print("获取ID成功")
        except:
            print("获取ID失败")
    def get_position(self,id):
        sql = "select `name`,`percents` from position where PID= %s"
        self.cur.execute(sql,id)
        items = self.cur.fetchall()
        print(items)
        return items

    def pid_is_in_list(self,PID):
        sql="SELECT COUNT(*) FROM portfolio WHERE PID=%s "

        try:
            self.cur.execute(sql,PID)
            results = self.cur.fetchone()
            if(results[0]!=0):
                return True
            return  False
        except:
            print("获取失败")
            return  False

    def __del__(self):
        self.conn.close()
        self.cur.close()
