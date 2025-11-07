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

manager_new = Blueprint('manager_new', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager_new.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('manager.studentManager'))

# ================== Student Management =====================
@manager_new.route('/studentManager', methods=['GET', 'POST'])
def studentManager():
    if 'delete' in request.values:
        pid = request.values.get('delete')
        Student.delete_student(pid)

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
        return redirect(url_for('manager.edit_student', pid=pid))
    

    student_data = student()
    return render_template('studentManager.html', student_data = student_data)

def student():
    student_row = Student.get_all_student()
    student_data = []
    for i in student_row:
        student = {
            '學號': i[0],
            '姓名': i[1],
            '性別': i[2],
            '系所': i[3],
            '年級': i[4],
            '是否為成員': i[5]
        }
        # print(student)
        student_data.append(student)
    return student_data

@manager_new.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # note: not completed
        pname = request.values.get('pname')
        gender = request.values.get('gender')
        department = request.values.get('department')
        grade = request.values.get('grade')

        # validation, can be extended
        if pname is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.studentManager'))
        if len(pname) < 1:
            flash('使用者名稱不可為空。')
            return redirect(url_for('manager.studentManager'))

        Student.add_student(
            {
            'pname' : pname,
            'gender' : gender,
            'department' : department,
            'grade':grade
            }
        )

        return redirect(url_for('manager.studentManager'))
    
    return render_template('studentManager.html')

@manager_new.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'POST':
        Student.update_student(
            {
            'pname' : request.values.get('pname'),
            'gender' : request.values.get('gender'),
            'department' : request.values.get('department'),
            'grade' : request.values.get('grade'),
            'pid' : request.values.get('pid')
            }
        )
        return redirect(url_for('manager.studentManager'))
    else:
        student = show_student_info()
        return render_template('edit_student.html', data=student)
    
def show_student_info():
    pid = request.args['pid']
    data = Student.get_student(pid)
    pname = data[1]
    gender = data[2]
    department = data[3]
    grade = data[4]
    
    student = {
        '使用者編號': pid,
        '使用者名稱': pname,
        '使用者性別': gender,
        '使用者系別': department,
        '使用者年級': grade
    }
    return student

# ================== Logistic Management =====================
@manager_new.route('/logisticManager', methods=['GET', 'POST'])
def logisticManager():
    if 'delete' in request.values:
        logistic_name = request.values.get('delete')
        Logistic.delete_logistic(logistic_name)

    elif 'edit' in request.values:
        logistic_name = request.values.get('edit')
        return redirect(url_for('manager.edit_logistic', logistic_name=logistic_name))

    Logistic_data = logistic()
    return render_template('logisticManager.html', logistic_data = Logistic_data)

def logistic():
    logistic_row = Logistic.get_all_logistic()
    logistic_data = []
    for i in logistic_row:
        logistic = {
            '後勤名稱': i[0],
            '工作內容': i[1]
        }
        logistic_data.append(logistic)
    return logistic_data

@manager_new.route('/add_logistic', methods=['GET', 'POST'])
def add_logistic():
    if request.method == 'POST':

        # note: not completed
        logistic_name = request.values.get('logistic_name')
        logistic_description = request.values.get('description')

        # validation, can be extended
        if logistic_name is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.logisticManager'))
        if len(logistic_name) < 1:
            flash('後勤名稱不可為空。')
            return redirect(url_for('manager.logisticManager'))

        Logistic.add_logistic(
            {
            'logistic_name' : logistic_name,
            'logistic_description' : logistic_description
            }
        )

        return redirect(url_for('manager.logisticManager'))
    
    return render_template('logisticManager.html')

@manager_new.route('/edit_logistic', methods=['GET', 'POST'])
def edit_logistic():
    if request.method == 'POST':
        Logistic.update_logistic(
            {
            'logistic_name' : request.values.get('logistic_name'),
            'logistic_description' : request.values.get('description'),
            }
        )
        return redirect(url_for('manager.logisticManager'))
    else:
        logistic = show_logistic_info()
        return render_template('edit_logistic.html', data=logistic)

def show_logistic_info():
    logistic_name = request.args['logistic_name']
    data = Logistic.get_logistic(logistic_name)
    logistic_description = data[1]
    
    logistic = {
        '後勤名稱': logistic_name,
        '工作內容': logistic_description
    }
    return logistic

# ================== Equipment Management =====================
@manager_new.route('/equipmentManager', methods=['GET', 'POST'])
def equipmentManager():
    if 'delete' in request.values:
        equipment_id = request.values.get('delete')
        Equipment.delete_equipment(equipment_id)

    elif 'edit' in request.values:
        equipment_id = request.values.get('edit')
        return redirect(url_for('manager.edit_equipment', equipment_id=equipment_id))

    equipment_data = equipment()
    return render_template('equipmentManager.html', equipment_data = equipment_data)

def equipment():
    equipment_row = Equipment.get_all_equipment()
    equipment_data = []
    for i in equipment_row:
        equipment = {
            '設備編號': i[0],
            '設備名稱': i[1],
            '設備狀態': i[2],
            '設備描述': i[3]
        }
        equipment_data.append(equipment)
    return equipment_data

@manager_new.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':

        # note: not completed
        equipment_name = request.values.get('equipment_name')
        equipment_status = request.values.get('equipment_status')
        equipment_description = request.values.get('description')

        # validation, can be extended
        if equipment_name is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.equipmentManager'))
        if len(equipment_name) < 1:
            flash('設備名稱不可為空。')
            return redirect(url_for('manager.equipmentManager'))

        Equipment.add_equipment(
            {
            'equipment_name' : equipment_name,
            'equipment_status' : equipment_status,
            'equipment_description' : equipment_description
            }
        )

        return redirect(url_for('manager.equipmentManager'))
    
    return render_template('equipmentManager.html')

@manager_new.route('/edit_equipment', methods=['GET', 'POST'])
def edit_equipment():
    if request.method == 'POST':
        Equipment.update_equipment(
            {
            'equipment_name' : request.values.get('equipment_name'),
            'equipment_status' : request.values.get('equipment_status'),
            'equipment_description' : request.values.get('description'),
            'equipment_id' : request.values.get('equipment_id')
            }
        )
        return redirect(url_for('manager.equipmentManager'))
    else:
        equipment = show_equipment_info()
        return render_template('edit_equipment.html', data=equipment)

def show_equipment_info():
    equipment_id = request.args['equipment_id']
    data = Equipment.get_equipment(equipment_id)
    equipment_name = data[1]
    equipment_status = data[2]
    equipment_description = data[3]
    
    equipment = {
        '設備編號': equipment_id,
        '設備名稱': equipment_name,
        '設備狀態': equipment_status,
        '設備描述': equipment_description
    }
    return equipment

# ================== Activity Management =====================
@manager_new.route('/activityManager', methods=['GET', 'POST'])
def activityManager():
    if 'delete' in request.values:
        activity_id = request.values.get('delete')
        Activity.delete_activity(activity_id)
    elif 'edit' in request.values:
        activity_id = request.values.get('edit')
        return redirect(url_for('manager.edit_activity', activity_id=activity_id))

    activity_data = activity()
    return render_template('activityManager.html')

def activity():
    activity_row = Activity.get_all_activity()
    activity_data = []
    for i in activity_row:
        activity = {
            '活動編號': i[0],
            '活動名稱': i[1],
            '活動日期': i[2],
            '活動描述': i[3]
        }
        activity_data.append(activity)
    return activity_data

@manager_new.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':

        # note: not completed
        activity_name = request.values.get('activity_name')
        activity_date = request.values.get('activity_date')
        activity_description = request.values.get('description')

        # validation, can be extended
        if activity_name is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.activityManager'))
        if len(activity_name) < 1:
            flash('活動名稱不可為空。')
            return redirect(url_for('manager.activityManager'))

        Activity.add_activity(
            {
            'activity_name' : activity_name,
            'activity_date' : activity_date,
            'activity_description' : activity_description
            }
        )

        return redirect(url_for('manager.activityManager'))
    
    return render_template('activityManager.html')

@manager_new.route('/edit_activity', methods=['GET', 'POST'])
def edit_activity():
    if request.method == 'POST':
        Activity.update_activity(
            {
            'activity_name' : request.values.get('activity_name'),
            'activity_date' : request.values.get('activity_date'),
            'activity_description' : request.values.get('description'),
            'activity_id' : request.values.get('activity_id')
            }
        )
        return redirect(url_for('manager.activityManager'))
    else:
        activity = show_activity_info()
        return render_template('edit_activity.html', data=activity)

def show_activity_info():
    activity_id = request.args['activity_id']
    data = Activity.get_activity(activity_id)
    activity_name = data[1]
    activity_date = data[2]
    activity_description = data[3]
    
    activity = {
        '活動編號': activity_id,
        '活動名稱': activity_name,
        '活動日期': activity_date,
        '活動描述': activity_description
    }
    return activity

# =================== Program Management =====================
@manager_new.route('/programManager', methods=['GET', 'POST'])
def programManager():
    if 'delete' in request.values:
        program_id = request.values.get('delete')
        Program.delete_program(program_id)
    elif 'edit' in request.values:
        program_id = request.values.get('edit')
        return redirect(url_for('manager.edit_program', program_id=program_id))
   
    program_data = program()
    return render_template('programManager.html')

def program():
    program_row = Program.get_all_program()
    program_data = []
    for i in program_row:
        program = {
            '節目編號': i[0],
            '節目名稱': i[1],
            '節目主持人': i[2],
            '節目時間': i[3]
        }
        program_data.append(program)
    return program_data

@manager_new.route('/add_program', methods=['GET', 'POST'])
def add_program():
    if request.method == 'POST':

        # note: not completed
        program_name = request.values.get('program_name')
        program_host = request.values.get('program_host')
        program_time = request.values.get('program_time')

        # validation, can be extended
        if program_name is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.programManager'))
        if len(program_name) < 1:
            flash('節目名稱不可為空。')
            return redirect(url_for('manager.programManager'))

        Program.add_program(
            {
            'program_name' : program_name,
            'program_host' : program_host,
            'program_time' : program_time
            }
        )

        return redirect(url_for('manager.programManager'))
    
    return render_template('programManager.html')

@manager_new.route('/edit_program', methods=['GET', 'POST'])
def edit_program():
    if request.method == 'POST':
        Program.update_program(
            {
            'program_name' : request.values.get('program_name'),
            'program_host' : request.values.get('program_host'),
            'program_time' : request.values.get('program_time'),
            'program_id' : request.values.get('program_id')
            }
        )
        return redirect(url_for('manager.programManager'))
    else:
        program = show_program_info()
        return render_template('edit_program.html', data=program)

def show_program_info():
    program_id = request.args['program_id']
    data = Program.get_program(program_id)
    program_name = data[1]
    program_host = data[2]
    program_time = data[3]
    
    program = {
        '節目編號': program_id,
        '節目名稱': program_name,
        '節目主持人': program_host,
        '節目時間': program_time
    }
    return program