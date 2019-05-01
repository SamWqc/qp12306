from PyQt5.Qt import *
import requests
import json
import re
import os
from urllib.parse import unquote,quote
import datetime
import time

class Config(object):

    #cookie参数

    now=datetime.datetime.now()
    date1=now.strftime('%Y-%m-%d')
    date2=now+datetime.timedelta(days=2)
    date2=date2.strftime('%Y-%m-%d')

    @staticmethod
    def date_form_trans(train_date):
        date_arr=time.strptime(train_date,"%Y%m%d")
        time_tamp=time.mktime(date_arr)
        time_local=time.localtime(time_tamp)
        format='%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)'
        return  time.strftime(format,time_local)

    seat_dic={

            '9': 'business_seat',
            'M': 'st_seat',
            '1': 'hard_seat',
            '6': 'advanced_soft_bed',
            '4': 'soft_bed',
            '3': 'hard_bed',
            'F': 'move_bed',
            'O': 'sec_seat',
            'WZ': 'no_seat'
        }

    seat_name_dic = {

        'business_seat': '商务座/特等座',
        'st_seat': '一等座',
        'hard_seat': '硬座',
        'advanced_soft_bed': '高级软卧',
        'soft_bed': '软卧',
        'hard_bed': '硬卧',
        'move_bed': '动卧',
        'sec_seat': '二等座',
        'no_seat': '无座'
    }

    @staticmethod
    def get_station_file_path():
        current_path = os.path.realpath(__file__)
        current_dic = os.path.split(current_path)[0]
        return current_dic+r'/staions'

    @staticmethod
    def get_curretn_path():
        current_path = os.path.realpath(__file__)
        current_dic = os.path.split(current_path)[0]
        return current_dic

    @staticmethod
    def input_CookieID():
        with open(Config.get_curretn_path() + r'/CookieID', 'r') as f:
            CookieID =json.loads(f.read(),encoding='utf-8')
            RAIL_DEVICED =CookieID['RAIL_DEVICED']
            RAIL_EXPIRATION = CookieID['RAIL_EXPIRATION']
            if len(RAIL_EXPIRATION)==0 or len(RAIL_EXPIRATION)==0:
                print('请输入正确的cookie参数')
                return None
            else:
                return (RAIL_DEVICED,RAIL_EXPIRATION)


class All_url(object):
    check_url='https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'  #验证码图片 GET请求
    check_answer_url='https://kyfw.12306.cn/passport/captcha/captcha-check'#验证码验证 post请求
    #From Data:
    #answer: 108, 55, 108, 108
    #login_site: E
    #rand: sjrand
    login_url='https://kyfw.12306.cn/passport/web/login'#登录验证 post
    #username: asdasdsadad
    #password: asdsadsadsa
    #appid: otn
    user_login='https://kyfw.12306.cn/otn/login/userLogin'
    uamtkclient_url='https://kyfw.12306.cn/otn/uamauthclient' #跳转页面 POST
    uamtk_url='https://kyfw.12306.cn/passport/web/auth/uamtk' #umtk POST
    greeting_url='https://kyfw.12306.cn/otn/index/initMy12306Api' #登录后页面 post
    log_redirect='https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'#获取JESESSIONID GET
    station_name_url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9098' #车站名 get
    ticket_query_url='https://kyfw.12306.cn/otn/leftTicket/query'#车票查询 get
    checkUser_url='https://kyfw.12306.cn/otn/login/checkUser'#检查是否登录 post
    submit_order_request_url='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'#提交订单 post
    initDc_url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'#获取token码 post
    passenger_dtos_url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'#获取乘客信息 post
    check_Order_url='https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'#检查车票信息 post
    # cancel_flag: 2
    # bed_level_order_num: 000000000000000000000000000000
    # passengerTicketStr: O, 0, 1, 陈彦先, 1, 440301199801115410, 15611877910, N
    # oldPassengerStr: 陈彦先, 1, 440301199801115410, 1_
    # tour_flag: dc
    # randCode:
    # whatsSelect: 1
    # _json_att:
    # REPEAT_SUBMIT_TOKEN: 5bcf3350f6a4c3a199fa06fb582c0f3f
    Queue_count_url='https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'# post查询车票余量
    confirm_queue_url='https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'


class APITool(QObject):

    session=requests.session()
    session.headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }

    @classmethod
    def download_check(cls):

        #登录首页
        response = cls.session.get('https://kyfw.12306.cn/otn/login/init')
        response.encoding = "utf-8"
        #获取cookie

        cls.cookies_1 = requests.utils.dict_from_cookiejar(cls.session.cookies)

        #获取验证码
        response=cls.session.get(All_url.check_url)

        cls.cookies_2 = requests.utils.dict_from_cookiejar(cls.session.cookies)

        with open(Config.get_curretn_path()+r'/check.jpg','wb') as f:
            f.write(response.content)
        return Config.get_curretn_path()+r'/check.jpg'

    @classmethod
    def check_yzm(cls,yzm):
        Form_data={
            'answer': yzm,
            'login_site': 'E',
            'rand': 'sjrand'
        }

        response=cls.session.post(All_url.check_answer_url,data=Form_data )
        dic=response.json()
        print(dic['result_message'])

        return dic["result_code"] =='4'

    @classmethod
    def login_check(cls,account,pwd):

        pass_ct = cls.cookies_2['_passport_ct']
        pass_session = cls.cookies_2['_passport_session']
        BIGGip_pass = cls.cookies_2['BIGipServerpool_passport']
        BIGGip_otn = cls.cookies_1['BIGipServerotn']
        route=cls.cookies_2['route']

        RAIL_DEVICED=Config.input_CookieID()[0]
        RAIL_EXPIRATION=Config.input_CookieID()[1]
        my_cookie='_passport_ct='+pass_ct+'; _passport_session='+pass_session+'; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION='+RAIL_EXPIRATION+'; RAIL_DEVICEID='+RAIL_DEVICED+'; route='+route+'; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
        headers = {
            'Cookie': my_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        cls.session.headers = headers
        dic_data = {
            'username': account,
            'password': pwd,
            'appid': 'otn'
        }
        response = cls.session.post(All_url.login_url, data=dic_data)
        try:
            dic=response.json()
            login_result=dic['result_message']
            login_code = dic['result_code']
            uamtk=dic['uamtk']


            if login_code==0:#用户名密码均正确 继续往下
                response = cls.session.post(All_url.user_login, data={'_json_att': ''})


                JSESSIONID_1 = response.headers['Set-Cookie']
                JSESSIONID = re.findall(r"J(.+?);", JSESSIONID_1)
                JSESSIONID = 'J' + JSESSIONID[0]


                my_cookie = '_passport_session=' + pass_session + '; uamtk=' + uamtk + '; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION='+RAIL_EXPIRATION+'; RAIL_DEVICEID='+RAIL_DEVICED+'; route=' + route + '; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
                headers = {
                    'Cookie': my_cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                }
                cls.session.headers = headers
                response = cls.session.post(All_url.uamtk_url, data={'appid': 'otn'})
                cookies_3 = requests.utils.dict_from_cookiejar(cls.session.cookies)
                dic = response.json()

                tk = dic['newapptk']
                print(response.json()['result_message'])

                my_cookie = JSESSIONID + '; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1555842745895; RAIL_DEVICEID='+RAIL_EXPIRATION+'; RAIL_DEVICEID='+RAIL_DEVICED+'; route=' + route + '; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
                headers = {
                    'Cookie': my_cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                }
                cls.session.headers = headers
                response = cls.session.post(All_url.uamtkclient_url, data={'tk': tk})

                my_cookie = JSESSIONID + '; tk=' + tk + '; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1555842745895; RAIL_DEVICEID='+RAIL_EXPIRATION+'; RAIL_DEVICEID='+RAIL_DEVICED+'; route=' + route + '; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
                headers = {
                    'Cookie': my_cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                }
                cls.session.headers = headers
                response = cls.session.post(All_url.greeting_url)
                dic = response.json()
                hello=dic['data']['user_name']+dic['data']['user_regard']
            else:#密码或者用户错误
                return None
            return login_code,hello
        except:
            print('登录失败')

    @staticmethod
    def get_station_name_reverse():
        dic=APITool.get_all_station()
        reverse_dic={value: key for key,value in dic.items()}
        return reverse_dic


    @staticmethod
    def get_all_station():
        if os.path.exists(Config.get_station_file_path()):

            with open(Config.get_station_file_path(),'r',encoding='utf-8') as f:
                station_dic=json.loads(f.read(),encoding='utf-8')

        else:
            print('网络请求下载车站列表')
            station_dic = {}
            response = requests.get(All_url.station_name_url)
            items = response.text.split("@")
            for item in items:
                station_list = item.split('|')
                if len(station_list) != 6:
                    continue
                city_name = station_list[1]
                city_code = station_list[2]
                station_dic[city_name] = city_code

            with open(Config.get_station_file_path(),'w',encoding='utf-8') as f:
                json.dump(station_dic,f)
        return station_dic

    @classmethod
    def ticket_query(cls,train_date,from_station,to_station,purpose_codes,seat_type=None):
        cls.query_dic={
            'train_date':train_date,
            'purpose_codes':purpose_codes,
            'seat_type':seat_type
        }

        reserve_dic=APITool.get_station_name_reverse()
        query_params={
            'leftTicketDTO.train_date':train_date,
            'leftTicketDTO.from_station': from_station,
            'leftTicketDTO.to_station': to_station,
            'purpose_codes':  purpose_codes
        }
        response=cls.session.get(All_url.ticket_query_url,params=query_params)
        result=response.json()
        train_Dicts=[]
        if result['httpstatus']==200:
            items = result['data']['result']
            for item in items:
                train_Dict = {}

                train_info=item.split('|')
                if train_info[11] == "Y":  # 是否可预订
                    train_Dict['secret_str'] = train_info[0]  # 车次密文字符串（下单使用）
                    train_Dict['train_num'] = train_info[2]  # 车次
                    train_Dict['train_name'] = train_info[3]  # 车次名称
                    train_Dict['from_station_code'] = train_info[6]  # 出发地编码
                    train_Dict['to_station_code'] = train_info[7]  # 目的地编码
                    train_Dict['from_station_name'] = reserve_dic[train_info[6]]  # 出发地名称
                    train_Dict['to_station_name'] = reserve_dic[train_info[7]]  # 目的地名称
                    train_Dict['start_time'] = train_info[8]
                    train_Dict['arrive_time'] = train_info[9]
                    train_Dict['total_time'] = train_info[10]
                    train_Dict['left_ticket'] = train_info[12]  # 余票
                    train_Dict['train_date'] = train_info[13]  # 火车日期
                    train_Dict['train_location'] = train_info[15]  # P4
                    train_Dict['advanced_soft_bed'] = train_info[21]
                    train_Dict['other_seat'] = train_info[22]
                    train_Dict['soft_bed'] = train_info[23]
                    train_Dict['no_seat'] = train_info[26]
                    train_Dict['hard_bed'] = train_info[28]
                    train_Dict['hard_seat'] = train_info[29]
                    train_Dict['sec_seat'] = train_info[30]
                    train_Dict['st_seat'] = train_info[31]
                    train_Dict['business_seat'] = train_info[32]
                    train_Dict['move_bed'] = train_info[33]

                    if seat_type==None:
                        train_Dicts.append(train_Dict)
                    else:
                        key=Config.seat_dic[seat_type]
                        if train_Dict[key]=='有' or train_Dict[key].isdigit():
                            train_Dicts.append(train_Dict)
        else:
            print('请求失败')
        return train_Dicts

    @classmethod
    def checkUser_login(cls):
        response=cls.session.post(All_url.checkUser_url,data={'_json_att':''})
        dic=response.json()
        is_login=dic['data']['flag']
        return is_login

    @classmethod
    def submit_order_request(cls,train_Dict):

        print(train_Dict)
        data_dic = {
            'secretStr': unquote(train_Dict['secret_str']),
            'train_date': cls.query_dic['train_date'],
            'back_train_date': cls.query_dic['train_date'],
            'tour_flag': 'dc',
            'purpose_codes': cls.query_dic['purpose_codes'],
            'query_from_station_name': train_Dict['from_station_name'],
            'query_to_station_name': train_Dict['to_station_name'],
            'undefined': ''
        }
        response = cls.session.post(All_url.submit_order_request_url, data=data_dic)
        status = response.json()['status']
        if not status:
            print(response.json()['messages'])
            return False
        print('继续订票')
        return True

    @classmethod
    def initDc(cls):
        response = cls.session.post(All_url.initDc_url, data={'_json_att':''})
        try:
            token = re.findall(r"var globalRepeatSubmitToken = '(.*?)'", response.text)[0]
            key_check_isChange= re.findall(r"'key_check_isChange':'(.*?)'", response.text)[0]
            return (token,key_check_isChange)
        except:
            print('获取相关参数失败')

    @classmethod
    def get_passenger_info(cls,token):
        data_dic={
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN':token
        }
        response=cls.session.post(All_url.passenger_dtos_url,data=data_dic)
        dic=response.json()
        if not dic['status']:
            print('获取乘客信息失败')
            return None
        name=input('输入乘客姓名')
        for each_dic in dic['data']['normal_passengers']:
            if each_dic['passenger_name']==name:
                return each_dic
        return None

    @classmethod
    def check_order_info(cls,seat_type,passenger,token):
        data_dic={
            'cancel_flag': '2', #固定值
            'bed_level_order_num': '000000000000000000000000000000',#固定值

            'passengerTicketStr': "{},{},{},{},{},{},{}, N".format(seat_type,passenger['passenger_flag'],passenger['passenger_type'],passenger['passenger_name'],passenger['passenger_id_type_code'],passenger['passenger_id_no'],passenger['mobile_no']),

            'oldPassengerStr': '{},{},{}, 1_'.format(passenger['passenger_name'],passenger['passenger_id_type_code'],passenger['passenger_id_no']),
            'tour_flag': 'dc',
            'randCode':'',
            'whatsSelect': '1',
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN': token
        }
        response=cls.session.post(All_url.check_Order_url,data=data_dic)
        result=response.json()
        if result['status'] and result['data']['submitStatus']:
            print('订单检查成功')
            return True
        else:
            return False

    @classmethod
    def queue_count(cls,train_dic,seat_type,token):

        dic_data={
            'train_date': Config.date_form_trans(train_dic['train_date']),
            'train_no': train_dic['train_num'],
            'stationTrainCode': train_dic['train_name'],
            'seatType': seat_type,
            'fromStationTelecode': train_dic['from_station_code'],
            'toStationTelecode': train_dic['to_station_code'],
            'leftTicket': train_dic['left_ticket'],
            'purpose_codes': '00',
            'train_location': train_dic['train_location'],
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN': token

        }
        response=cls.session.post(All_url.Queue_count_url,data=dic_data)
        result=response.json()
        if not result['status']:
            print('查询队列消息失败')
            return False
        print('查询队列消息成功','当前余票'+result['data']['ticket'])
        return True

    @classmethod
    def confirm_queue(cls,seat_type,passenger,train_dic,token,key_check_isChange):
        data_dic={
            'passengerTicketStr':"{},{},{},{},{},{},{}, N".format(seat_type,passenger['passenger_flag'],passenger['passenger_type'],passenger['passenger_name'],passenger['passenger_id_type_code'],passenger['passenger_id_no'],passenger['mobile_no']),

            'oldPassengerStr': '{},{},{}, 1_'.format(passenger['passenger_name'], passenger['passenger_id_type_code'],passenger['passenger_id_no']),
            'randCode':'',
            'purpose_codes':'00',
            'key_check_isChange':key_check_isChange,
            'leftTicketStr':train_dic['left_ticket'],
            'train_location':train_dic['train_location'],
            'choose_seats':'',
            'seatDetailType':'000',
            'whatsSelect':'1',
            'roomType':'00',
            'dwAll':'N',
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN': token


        }
        response=cls.session.post(All_url.confirm_queue_url,data=data_dic)
        try:
            dic=response.json()
            result=dic['data']['submitStatus']
            if not result:
                print('抢票失败')
            print('抢票成功')
            print('已经为您抢到'+'由'+train_dic['from_station_name']+'开往'+train_dic['to_station_name']+'的'+train_dic['train_name']+'列车'+'(起始'+train_dic['start_time']+'——'+train_dic['arrive_time']+'到达)的'+Config.seat_name_dic[seat_type]+'车票')
        except:
            print('发送请求失败')

    @classmethod
    def buy_ticket(cls,train_dic=None):
        try:
            if not cls.checkUser_login():
                print('请先登录账户')
                return None

            if cls.submit_order_request(train_dic):
                token,key_check_isChange=cls.initDc()
                passenger_info=cls.get_passenger_info(token)
                if not cls.check_order_info(cls.query_dic['seat_type'],passenger_info,token):
                    print('订单检查失败')
                    return None
                if cls.queue_count(train_dic,cls.query_dic['seat_type'],token):
                    cls.confirm_queue(cls.query_dic['seat_type'],passenger_info,train_dic,token,key_check_isChange)

            return True
        except:
            return False





if __name__ == '__main__':
    a=Config.get_png_file_path()
    print(a)