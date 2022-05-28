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
@click.option("--retry", '-r', help="Retry to get access to the api or not", default=False)
@click.option("--flag", '-f', help="Flag file path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'read_flag.json'))
def WebParaClient(gap, host, port, car, to, retry, flag): 
    while True:
        Car_para_json = {}
        try: 
            # 检查read_flag.json是否需要重置车辆参数更新位
            flag_f = open(flag)
            flag_json = json.load(flag_f)
            # 程序已经读取完了参数，说明服务端的数据没有更新
            if flag_json['Read_flag'] == True: 
                print("[info] reset car")
                response = requests.post("http://" + host +":" + port + "/api/reset_Car", data={"name": car})
                print(response.text)
            flag_f.close()

            # 获取车辆状态
            Car_state = requests.get("http://" + host +":" + port + "/api/get_Cars")
            Car_para_json["Update_flag"] = json.loads(Car_state.text)[car]["Update_flag"]
            
            # 获取车辆参数
            Car_para = requests.get("http://" + host +":" + port + "/api/get_Paras/" + car)
            tmp_json = json.loads(Car_para.text)
            # 对参数作类别分析
            for i in tmp_json: 
                if tmp_json[i]['Para_type'].lower() == "int": 
                    Car_para_json[i] = int(tmp_json[i]['Para_val'])
                elif tmp_json[i]['Para_type'].lower() == "float": 
                    Car_para_json[i] = float(tmp_json[i]['Para_val'])
                else: 
                    Car_para_json[i] = tmp_json[i]['Para_val']
            print(Car_para_json)
        except: 
            print("Get access to api WRONG")
            if not retry: 
                sys.exit(1)
        
        
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