'''
    这个程序是与WebParaClient对接程序的逻辑演示程序
    客户端逻辑：
        从服务端获取参数，通过read_flag.json的"Read_flag"判断对接程序是否读取
            若已经读取，"Read_flag"应为true，则将服务端的"Update_flag"置为false
            若没有读取，"Read_flag"应为false，不作操作
    
    对接程序逻辑：
        检查客户端从服务器获取的数据文件car_conf.json，通过"Update_flag"判断数据是否更新
            若更新了，"Update_flag"应为true，则将read_flag.json的"Read_flag"置为true，同时进行更新参数操作
            若没有更新，"Update_flag"应为false，则将read_flag.json的"Read_flag"置为false
'''
import json
import os

from time import sleep

if __name__=="__main__": 
    
    # 循环获取程序
    while(True): 
        # 获取当前参数
        conf_f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'car_conf.json'), "r")
        conf = json.load(conf_f)
        conf_f.close()
        flag = {}

        # 检查车辆参数是否需要更新
        # 如果发现获取到的数据更新了（"Update_flag": true），读取更新数据，然后向指定路径的read_flag.json文件中写入：{"Update_flag": true}
        if conf["Update_flag"] == True: 
            # 写入read_flag.json文件：{"Update_flag": false}
            flag_f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'read_flag.json'), "w")
            flag["Read_flag"] = True
            json.dump(flag, flag_f, ensure_ascii=False, indent=4)
            flag_f.close()

            # 成功更新后应当执行的命令，即在此处调用更新参数的接口
            print("[info] successfully update conf!")
        
        # 如果发现不需要更新（"Update_flag": false），向指定路径的read_flag.json文件中写入：{"Update_flag": false}
        else: 
            # 写入read_flag.json文件：{"Update_flag": false}
            flag_f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'read_flag.json'), "w")
            flag["Read_flag"] = False
            json.dump(flag, flag_f, ensure_ascii=False, indent=4)
            flag_f.close()
        print(conf)
        sleep(1)