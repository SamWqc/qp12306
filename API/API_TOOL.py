from PyQt5.Qt import *
import requests
import json
import re
import os
from urllib.parse import unquote,quote
import datetime

class Config(object):

    now=datetime.datetime.now()
    date1=now.strftime('%Y-%m-%d')
    date2=now+datetime.timedelta(days=2)
    date2=date2.strftime('%Y-%m-%d')


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


    @staticmethod
    def get_station_file_path():
        current_path = os.path.realpath(__file__)
        current_dic = os.path.split(current_path)[0]
        return current_dic+r'\staions'

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
        cookies_1 = requests.utils.dict_from_cookiejar(cls.session.cookies)
        with open("cook1.txt", "w") as fp:
            json.dump(cookies_1, fp)


        #获取验证码
        response=cls.session.get(All_url.check_url)

        cookies_2 = requests.utils.dict_from_cookiejar(cls.session.cookies)
        with open("cook2.txt", "w") as fp:
            json.dump(cookies_2, fp)

        with open('D:/qp/API/check.jpg','wb') as f:
            f.write(response.content)
        return 'API/check.jpg'

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

        with open('D:/qp/ui/cook1.txt', "r") as f:  # 设置文件对象
            cookies_1 = f.read()

        with open('D:/qp/ui/cook2.txt', "r") as f:  # 设置文件对象
            cookies_2 = f.read()

        cookies_1=json.loads(cookies_1)
        cookies_2=json.loads(cookies_2)
        pass_ct = cookies_2['_passport_ct']
        pass_session = cookies_2['_passport_session']
        BIGGip_pass = cookies_2['BIGipServerpool_passport']
        BIGGip_otn = cookies_1['BIGipServerotn']
        route=cookies_2['route']

        my_cookie='_passport_ct='+pass_ct+'; _passport_session='+pass_session+'; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1554788942127; RAIL_DEVICEID=Y4IgyRD7HrMJJolLl2Vkkv1TYOqODnX6JUSMFEG5l8aVQsCfk7JfFkRiSHHceuhGGBVcjeZS82T-gpStar_RRAZ6dR5R3EBdpwYBKyBgXIkmSHSer6jmfrhMNsJT4QBdGNbPIFmuJgMFgqokjvmp22rZW8NdMggo; route='+route+'; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
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
        dic=response.json()

        login_result=dic['result_message']
        login_code = dic['result_code']
        uamtk=dic['uamtk']
        cookie = requests.utils.dict_from_cookiejar(cls.session.cookies)
        JSESSIONID = cookie['JSESSIONID']

        if login_code==0:#用户名密码均正确 继续往下
            response = cls.session.post(All_url.user_login, data={'_json_att': ''})

            response = cls.session.get(All_url.log_redirect)
            JSESSIONID_1 = response.headers['Set-Cookie']
            JSESSIONID = re.findall(r"J(.+?);", JSESSIONID_1)
            JSESSIONID = 'J' + JSESSIONID[0]


            my_cookie = '_passport_session=' + pass_session + '; uamtk=' + uamtk + '; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1554788942127; RAIL_DEVICEID=Y4IgyRD7HrMJJolLl2Vkkv1TYOqODnX6JUSMFEG5l8aVQsCfk7JfFkRiSHHceuhGGBVcjeZS82T-gpStar_RRAZ6dR5R3EBdpwYBKyBgXIkmSHSer6jmfrhMNsJT4QBdGNbPIFmuJgMFgqokjvmp22rZW8NdMggo; route=' + route + '; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
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

            my_cookie = JSESSIONID + '; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1554788942127; RAIL_DEVICEID=Y4IgyRD7HrMJJolLl2Vkkv1TYOqODnX6JUSMFEG5l8aVQsCfk7JfFkRiSHHceuhGGBVcjeZS82T-gpStar_RRAZ6dR5R3EBdpwYBKyBgXIkmSHSer6jmfrhMNsJT4QBdGNbPIFmuJgMFgqokjvmp22rZW8NdMggo; route=' + route + '; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
            headers = {
                'Cookie': my_cookie,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
            }
            cls.session.headers = headers
            response = cls.session.post(All_url.uamtkclient_url, data={'tk': tk})

            my_cookie = JSESSIONID + '; tk=' + tk + '; ten_js_key=6xOp4XVGdN9%2FTvfJFcMTxizDWca166J6; ten_key=mo/81LXM/45d0AmB+Pbd3BSx0GJbo+Pm; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1554788942127; RAIL_DEVICEID=Y4IgyRD7HrMJJolLl2Vkkv1TYOqODnX6JUSMFEG5l8aVQsCfk7JfFkRiSHHceuhGGBVcjeZS82T-gpStar_RRAZ6dR5R3EBdpwYBKyBgXIkmSHSer6jmfrhMNsJT4QBdGNbPIFmuJgMFgqokjvmp22rZW8NdMggo; route=' + route + '; BIGipServerpool_passport='+BIGGip_pass+'; _jc_save_toDate='+Config.date1+'; _jc_save_fromDate='+Config.date2+'; BIGipServerpassport=770179338.50215.0000; BIGipServerotn='+BIGGip_otn
            headers = {
                'Cookie': my_cookie,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
            }
            cls.session.headers = headers
            response = cls.session.post(All_url.greeting_url)
            dic = response.json()
            hello=dic['data']['user_name']+dic['data']['user_regard']
            print(hello)

        else:#密码或者用户错误
            return None

        return login_code,hello

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
        print(dic)
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

        token = re.findall(r'var globalRepeatSubmitToken = (.*?)', response.text)
        print(token)
        return token

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

            'passengerTicketStr': "{}, {}, {}, {}, {}, {}, {}, N".format(seat_type,passenger['passenger_flag'],passenger['passenger_type'],passenger['passenger_name'],passenger['passenger_id_type_code'],passenger['passenger_id_no'],passenger['mobile_no']),

            'oldPassengerStr': '{}, {}, {}, 1_'.format(passenger['passenger_name'],passenger['passenger_id_type_code'],passenger['passenger_id_no']),
            'tour_flag': 'dc',
            'randCode':'',
            'whatsSelect': '1',
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN': token
        }
        response=cls.session.post(All_url.check_Order_url,data=data_dic)
        print(response.text)

    @classmethod
    def buy_ticket(cls,train_Dict=None):

        if not cls.checkUser_login():
            print('请先登录账户')
            return None
        if cls.submit_order_request(train_Dict):
            token=cls.initDc()
            data_dic={
                '_json_att':'',
                'REPEAT_SUBMIT_TOKEN': token
            }
            passenger_info=cls.get_passenger_info(token)
            print(passenger_info)
            cls.check_order_info(cls.query_dic['seat_type'],passenger_info,token)






if __name__ == '__main__':
    a=APITool.get_station_name_reverse()
    print(a)
