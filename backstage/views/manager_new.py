from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
# noted change
from api.sql_new import *

import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/personManager', methods=['GET', 'POST'])
def personManager():
    if 'delete' in request.values:
        pid = request.values.get('delete')
        Person.delete_person(pid)

    #     if 'delete' in request.values:
    #         pid = request.values.get('delete')
    #         data = Record.delete_check(pid)
            
    #         if(data != None):
    #             flash('failed')
    #         else:
    #             data = Product.get_product(pid)
    #             Product.delete_product(pid)

    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit_person', pid=pid))
    

    person_data = person()
    return render_template('personManager.html', person_data = person_data, user=current_user.name)

def person():
    person_row = Person.get_all_person()
    person_data = []
    for i in person_row:
        person = {
            '使用者編號': i[0],
            '使用者名稱': i[1],
            '使用者角色': i[2],
            '使用者信箱': i[3]
        }
        person_data.append(person)
    return person_data

@manager.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':

        # note: not completed
        pname = request.values.get('pname')
        gender = request.values.get('gender')
        department = request.values.get('department')
        grade = request.values.get('grade')

        # validation, can be extended
        if pname is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.personManager'))
        if len(pname) < 1:
            flash('使用者名稱不可為空。')
            return redirect(url_for('manager.personManager'))

        Person.add_person(
            {
            'pname' : pname,
            'gender' : gender,
            'department' : department,
            'grade':grade
            }
        )

        return redirect(url_for('manager.personManager'))
    
    return render_template('personManager.html')

@manager.route('/edit_person', methods=['GET', 'POST'])
def edit_person():
    if request.method == 'POST':
        Person.update_person(
            {
            'pname' : request.values.get('pname'),
            'gender' : request.values.get('gender'),
            'department' : request.values.get('department'),
            'grade' : request.values.get('grade'),
            'pid' : request.values.get('pid')
            }
        )
        return redirect(url_for('manager.personManager'))
    else:
        person = show_person_info()
        return render_template('edit_person.html', data=person)
    
def show_person_info():
    pid = request.args['pid']
    data = Person.get_person(pid)
    pname = data[1]
    gender = data[2]
    department = data[3]
    grade = data[4]
    
    person = {
        '使用者編號': pid,
        '使用者名稱': pname,
        '使用者性別': gender,
        '使用者系別': department,
        '使用者年級': grade
    }
    return person

@manager.route('/logisticsManager', methods=['GET', 'POST'])
def logisticsManager():
    if 'delete' in request.values:
        logistics_name = request.values.get('delete')
        Person.delete_person(logistics_name)

    #     if 'delete' in request.values:
    #         pid = request.values.get('delete')
    #         data = Record.delete_check(pid)
            
    #         if(data != None):
    #             flash('failed')
    #         else:
    #             data = Product.get_product(pid)
    #             Product.delete_product(pid)

    elif 'edit' in request.values:
        logistics_name = request.values.get('edit')
        return redirect(url_for('manager.edit_person', logistics_name=logistics_name))
    

    person_data = person()
    return render_template('personManager.html', person_data = person_data, user=current_user.name)

def person():
    person_row = Person.get_all_person()
    person_data = []
    for i in person_row:
        person = {
            '使用者編號': i[0],
            '使用者名稱': i[1],
            '使用者角色': i[2],
            '使用者信箱': i[3]
        }
        person_data.append(person)
    return person_data

@manager.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':

        # note: not completed
        pname = request.values.get('pname')
        gender = request.values.get('gender')
        department = request.values.get('department')
        grade = request.values.get('grade')

        # validation, can be extended
        if pname is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.personManager'))
        if len(pname) < 1:
            flash('使用者名稱不可為空。')
            return redirect(url_for('manager.personManager'))

        Person.add_person(
            {
            'pname' : pname,
            'gender' : gender,
            'department' : department,
            'grade':grade
            }
        )

        return redirect(url_for('manager.personManager'))
    
    return render_template('personManager.html')

@manager.route('/edit_person', methods=['GET', 'POST'])
def edit_person():
    if request.method == 'POST':
        Person.update_person(
            {
            'pname' : request.values.get('pname'),
            'gender' : request.values.get('gender'),
            'department' : request.values.get('department'),
            'grade' : request.values.get('grade'),
            'pid' : request.values.get('pid')
            }
        )
        return redirect(url_for('manager.personManager'))
    else:
        person = show_person_info()
        return render_template('edit_person.html', data=person)
    
def show_person_info():
    pid = request.args['pid']
    data = Person.get_person(pid)
    pname = data[1]
    gender = data[2]
    department = data[3]
    grade = data[4]
    
    person = {
        '使用者編號': pid,
        '使用者名稱': pname,
        '使用者性別': gender,
        '使用者系別': department,
        '使用者年級': grade
    }
    return person


# @manager.route('/orderManager', methods=['GET', 'POST'])
# @login_required
# def orderManager():
#     if request.method == 'POST':
#         pass
#     else:
#         order_row = Order_List.get_order()
#         order_data = []
#         for i in order_row:
#             order = {
#                 '訂單編號': i[0],
#                 '訂購人': i[1],
#                 '訂單總價': i[2],
#                 '訂單時間': i[3]
#             }
#             order_data.append(order)
            
#         orderdetail_row = Order_List.get_orderdetail()
#         order_detail = []

#         for j in orderdetail_row:
#             orderdetail = {
#                 '訂單編號': j[0],
#                 '商品名稱': j[1],
#                 '商品單價': j[2],
#                 '訂購數量': j[3]
#             }
#             order_detail.append(orderdetail)

#     return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)