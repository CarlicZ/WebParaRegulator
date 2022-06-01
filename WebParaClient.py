'''
    This is the client program of the WebParameter adjust system
'''

import json
import requests
import click
import os
import sys

from time import sleep

# command option setting
@click.command()
@click.option("--gap", "-g", help="Time gap for waiting", default=1)
@click.option("--host", '-h', help="Host address for get conf", default="127.0.0.1")
@click.option("--port", '-p', help="Port of the service on the host", default="5000")
@click.option("--car", '-c', help="Name of the car to get conf", required=True)
@click.option("--to", '-t', help="Conf file output path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'car_conf.json'))
@click.option("--retry", '-r', help="Retry to get access to the api or not", default=True)
@click.option("--flag", '-f', help="Flag file path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'read_flag.json'))
def WebParaClient(gap, host, port, car, to, retry, flag): 
    while True:
        Http_flag = True # 用于标志http请求是否正常

        Car_para_json = {}
        # 检查read_flag.json是否需要重置车辆参数更新位
        if not os.path.exists(flag):
            f_tmp=open(flag,"w")
            f_tmp.close()
        flag_f = open(flag, "r")
        try:
            flag_json = json.load(flag_f)
        except:
            flag_json={}
        if 'Read_flag' not in flag_json:
            flag_json['Read_flag']=False
        # 程序已经读取完了参数，说明服务端的数据没有更新
        if flag_json['Read_flag'] == True: 
            print("[info] Reseting car")
            try: 
                response = requests.post("http://" + host +":" + port + "/api/reset_Car", data={"name": car})
                print(response.text)
                print("[info] Reset car success!")
            except: 
                print("\033[31m[err] Reset car failed!\033[0m")
                Http_flag = False
        flag_f.close()
        try: 
            # 获取车辆状态
            print("[info] Getting car Update_flag")
            Car_state = requests.get("http://" + host +":" + port + "/api/get_Cars")
            Car_para_json["Update_flag"] = json.loads(Car_state.text)[car]["Update_flag"]
            print("[info] Getting car Update_flag success!")
            
            # 获取车辆参数
            print("[info] Getting car paras")
            Car_para = requests.get("http://" + host +":" + port + "/api/get_Paras/" + car)
            print("[info] Getting car paras")
        except: 
            print("\033[31m[err] Getting car Updata_flag or para failed!\033[0m")
            Http_flag = False
        

        # HTTP请求标志检查，如果不正常，本次请求流程作废，不更新参数文件
        if not Http_flag: 
            print("\033[31m[err]Get access to api WRONG\033[0m")
            if not retry: 
                sys.exit(1)
        # HTTP请求标志正常，更新参数文件
        else: 
            # 对参数作类别分析
            tmp_json = json.loads(Car_para.text)
            for i in tmp_json: 
                if tmp_json[i]['Para_type'].lower() == "int": 
                    Car_para_json[i] = int(tmp_json[i]['Para_val'])
                elif tmp_json[i]['Para_type'].lower() == "float": 
                    Car_para_json[i] = float(tmp_json[i]['Para_val'])
                else: 
                    Car_para_json[i] = tmp_json[i]['Para_val']
            print(Car_para_json)
            # 写文件
            try:
                to_f = open(to, "w")
                json.dump(Car_para_json, to_f, ensure_ascii=False, indent=4)
                to_f.close()
            except: 
                print("write json fail!")
                to_f.close()
                sys.exit(1)
        sleep(gap)


if __name__ == "__main__": 
    WebParaClient()
    
    pass