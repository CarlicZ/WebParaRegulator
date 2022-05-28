import os
import sys
import click
import json
import requests

from flask import Flask, render_template, request, redirect, flash, url_for # 导入flask以及其模板类
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true  # 导入扩展类


# ************** 初始化：app，数据库 **************
# 系统判定决定sqlite路径选择，win与unix类有所区别
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

data_api = Flask(__name__)

# 获取数据库绝对地址，并设置在应用中
db_path = prefix + os.path.join(data_api.root_path, 'RP_car_data.db')
print(db_path)
data_api.config["SQLALCHEMY_DATABASE_URI"] = db_path
data_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 在扩展类实例化前加载配置
db = SQLAlchemy(app=data_api)


# ************** 模组（表）定义 **************
##### 车表，id、车名、更新标志位
class Car(db.Model): 
    Car_name = db.Column(db.String(60), primary_key=True) # 车名不可重复，主键
    Update_flag = db.Column(db.Boolean)

#### 参数表，id、车名、参数名、参数类型、参数值
class Para(db.Model): 
    Para_name = db.Column(db.String(60), primary_key=True)  # 主键
    Car_name = db.Column(db.String(60))
    Para_type = db.Column(db.String(60))
    Para_val = db.Column(db.String(60))

# 初始化数据库，使用命令初始化
@data_api.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        click.echo("Droping database.")
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


# ************** API设计，增删改查部分 **************
# get_Cars_api接口, 获取车辆的API
@data_api.route('/api/get_Cars')
def get_Cars_api():
    Cars = Car.query.all() # 获取全部车子对象
    Cars_json = {}
    for car in Cars: 
        Cars_json[car.Car_name]={"Update_flag": car.Update_flag}
    print(Cars_json)
    return json.dumps(Cars_json, ensure_ascii=False) # 将车子对象以及更新标志打包为json返回

# add_Car_api接口, 增加车子的API
@data_api.route('/api/add_Car', methods=["POST"])
def add_Car_api(): 
    if request.method == 'POST':  # 对POST请求操作
        tmp_Car_name = request.form.get('name') # 获取需要添加的车子名称
        tmp_Car = Car(Car_name=tmp_Car_name, Update_flag=0) # 生成新添加的车对象
        try: # 尝试添加车辆，对错误抛出并返回错误信息
            db.session.add(tmp_Car) 
            db.session.commit()
        except: 
            return "Add Car Fail!"
        else: 
            return redirect(url_for("index"))
    else: 
        return "Add Car Fail!"

# del_Car_api接口, 删除车子的API
@data_api.route('/api/del_Car', methods=["POST"])
def del_Car_api(): 
    if request.method == 'POST':  # 对POST请求操作
        tmp_Car_name = request.form.get('name') # 获取需要删除的车子名称
        tmp_Car = Car.query.get_or_404(tmp_Car_name) # 获取数据库中需要删除的车子对象
        tmpParas = Para.query.filter(Para.Car_name == tmp_Car_name).all() # 获取数据库中需要删除的车子的参数对象
        try: # 尝试删除车辆，对错误抛出并返回错误信息
            db.session.delete(tmp_Car)
            for para in tmpParas: 
                db.session.delete(para)
            db.session.commit()
        except: 
            return "Delete Car Fail!"
        else: 
            return "Delete Car Success!"
    else: 
        return "Delete Car Fail!"

# reset_Car_api接口, 消除车子更新的API
@data_api.route('/api/reset_Car', methods=["POST"])
def reset_Car_api(): 
    if request.method == 'POST': # 处理POST请求
        # 找车辆对象
        tmp_Car_name = request.form.get('name')
        tmp_Car = Car.query.get(tmp_Car_name)
        try: # 尝试修改车辆对象
            if tmp_Car.Update_flag == 1:
                tmp_Car.Update_flag = 0
                db.session.commit()
        except: 
            return "Reset Car Fail!"
        else: 
            return "Reset " + tmp_Car_name + " Success"
    else: 
        return "Reset Car Fail!"

# get_Paras_api接口, 获取车辆所有参数的API
@data_api.route('/api/get_Paras/<Car_name>')
def get_Paras_api(Car_name):
    Paras = Para.query.filter(Para.Car_name==Car_name).all()
    Paras_json = {}
    for para in Paras: 
        Paras_json[para.Para_name[para.Car_name.__len__() + 1:]]={"Car_name": para.Car_name, 
                                                                  "Para_type": para.Para_type, 
                                                                  "Para_val": para.Para_val}
    print(Paras_json)
    return json.dumps(Paras_json, ensure_ascii=False)

# add_Para_api接口, 增加车子参数的API
@data_api.route('/api/add_Para', methods=["POST"])
def add_Para_api(): 
    if request.method == 'POST':  
        tmp_Car_name = request.form.get('Car_name')
        tmp_Para_name = request.form.get('Para_name')
        tmp_Para_type = request.form.get('Para_type')
        tmp_Para_val = request.form.get('Para_val')
        tmp_Para = Para(Para_name=tmp_Car_name + "_" + tmp_Para_name, 
                      Car_name=tmp_Car_name, 
                      Para_type=tmp_Para_type, 
                      Para_val=tmp_Para_val)
        Car_update = Car.query.get(tmp_Car_name)
        try: 
            db.session.add(tmp_Para)
            Car_update.Update_flag = 1
            db.session.commit()
        except: 
            return "Add Para Fail!"
        else: 
            return redirect(url_for("car", Car_name=tmp_Car_name))
    else: 
        return "Add Para Fail!"

# del_Para_api接口, 删除车子参数的API
@data_api.route('/api/del_Para', methods=["POST"])
def del_Para_api(): 
    if request.method == 'POST':  
        tmp_Car_name = request.form.get('Car_name')
        tmp_Para_name = request.form.get('Para_name')
        Para_del = Para.query.get(tmp_Para_name)
        Car_update = Car.query.get(tmp_Car_name)
        try: 
            db.session.delete(Para_del)
            Car_update.Update_flag = 1
            db.session.commit()
        except: 
            return "Delete Para Fail!"
        else: 
            return redirect(url_for("car", Car_name=tmp_Car_name))
    else: 
        return "Delete Para Fail!"

# update_Para_api接口, 更新车子参数的api
@data_api.route('/api/update_Para', methods=["POST"])
def update_Para_api(): 
    if request.method == 'POST':  
        tmp_Car_name = request.form.get('Car_name')
        tmp_Para_name = request.form.get('Para_name')
        tmp_Para_val = request.form.get('Para_val')
        Para_update = Para.query.get(tmp_Para_name)
        Car_update = Car.query.get(tmp_Car_name)
        try: 
            Para_update.Para_val = tmp_Para_val
            Car_update.Update_flag = 1
            db.session.commit()
        except: 
            return "Update Para Fail!"
        else: 
            return redirect(url_for("car", Car_name=tmp_Car_name))
    else: 
        return "Update Para Fail!"

# ************** demo页面设计，用于基础的展示信息 **************
# index页面，模板演示所有车子信息
@data_api.route('/')
def index():
    Cars = Car.query.all()
    Paras = Para.query.all()
    return render_template('index.html',
                           Cars=Cars,
                           Paras=Paras
                           )

# Cars页面，模板显示某辆车子信息
@data_api.route('/car/<Car_name>')
def car(Car_name): 
    Paras = Para.query.filter(Para.Car_name == Car_name).all()
    return render_template('car.html',
                           Car=Car_name,
                           Paras=Paras
                           )

# 获取所有车api

if __name__ == "__main__": 
    data_api.run(host='0.0.0.0', port=5000)