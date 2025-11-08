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
    return redirect(url_for('manager_new.studentManager'))

# ================== Student Management =====================
@manager_new.route('/studentManager', methods=['GET', 'POST'])
def studentManager():
    if 'delete' in request.values:
        sId = request.values.get('delete')
        Student.delete_student(sId)

    #     if 'delete' in request.values:
    #         sId = request.values.get('delete')
    #         data = Record.delete_check(sId)
            
    #         if(data != None):
    #             flash('failed')
    #         else:
    #             data = Product.get_product(sId)
    #             Product.delete_product(sId)

    elif 'edit' in request.values:
        sId = request.values.get('edit')
        return redirect(url_for('manager_new.edit_student', sId=sId))
    

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
            '年級': i[3],
            '系所': i[4],
            '是否為成員': i[5],
            '所屬後勤團隊': i[6]
        }
        # print(student)
        student_data.append(student)
    return student_data

@manager_new.route('/add_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':

        sId = request.values.get('sId')
        sName = request.values.get('sName')
        gender = request.values.get('gender')
        grade = request.values.get('grade')
        department = request.values.get('department')
        is_member = request.values.get('isMember')
        logistic = request.values.get('logistic') or None

        # validation, can be extended
        if not sId or not sName or not gender or not department:
            flash('所有欄位都是必填的（除了後勤組別），請確認輸入內容。')
            return redirect(url_for('manager_new.studentManager'))
        if len(sName) < 1:
            flash('使用者名稱不可為空。')
            return redirect(url_for('manager_new.studentManager'))

        Student.create_student(
            {
                'sId': sId,
                'sName': sName,
                'gender': gender,
                'grade': grade,
                'department': department,
                'isMember': is_member,
                'logistic': logistic
            }
        )

        return redirect(url_for('manager_new.studentManager'))

    return render_template('studentManager.html')

@manager_new.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'POST':
        Student.update_student(
            {
                'sId' : request.values.get('sId'),
                'sName' : request.values.get('sName'),
                'gender' : request.values.get('gender'),
                'grade' : request.values.get('grade'),                
                'department' : request.values.get('department'),
                'isMember' : request.values.get('isMember'),
                'logistic' : request.values.get('logistic'),
            }
        )
        return redirect(url_for('manager_new.studentManager'))
    else:
        student = show_student_info()
        logistic_data = Logistic.get_all_logistic()
        return render_template('studentEditor.html', student=student, logistic_data=logistic_data)
    
def show_student_info():
    sId = request.args['sId']
    record = Student.get_student(sId)
    data = record[0]
    sName = data[1]
    gender = data[2]
    grade = data[3]
    department = data[4]
    isMember = data[5]
    lName = data[6]

    student = {
        'sId': sId,
        'sName': sName,
        'gender': gender,
        'department': department,
        'grade': grade,
        'isMember': isMember,
        'lName': lName

    }
    return student

# ================== Logistic Management =====================
@manager_new.route('/logisticManager', methods=['GET', 'POST'])
def logisticManager():
    if 'delete' in request.values:
        lName = request.values.get('delete')
        Logistic.delete_logistic(lName)

    elif 'edit' in request.values:
        lName = request.values.get('edit')
        return redirect(url_for('manager_new.edit_logistic', lName=lName))

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

        lName = request.values.get('lName')
        Job_Desc = request.values.get('Job_Desc')

        # validation, can be extended
        if lName is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager_new.logisticManager'))
        if len(lName) < 1:
            flash('後勤名稱不可為空。')
            return redirect(url_for('manager_new.logisticManager'))

        Logistic.create_logistic(
            {
            'lName' : lName,
            'Job_Desc' : Job_Desc
            }
        )

        return redirect(url_for('manager_new.logisticManager'))
    
    return render_template('logisticManager.html')

@manager_new.route('/edit_logistic', methods=['GET', 'POST'])
def edit_logistic():
    if request.method == 'POST':
        Logistic.update_logistic(
            {
            'new_lName' : request.values.get('new_lName'),
            'Job_Desc' : request.values.get('Job_Desc'),
            'lName' : request.values.get('lName')
            }
        )
        return redirect(url_for('manager_new.logisticManager'))
    else:
        logistic = show_logistic_info()
        return render_template('logisticEditor.html', logistic=logistic)

def show_logistic_info():
    lName = request.args['lName']
    record = Logistic.get_logistic(lName)
    data = record[0]
    lName = data[0]
    Job_Desc = data[1]
    
    logistic = {
        'lName': lName,
        'Job_Desc': Job_Desc
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
        return redirect(url_for('manager_new.edit_equipment', equipment_id=equipment_id))

    equipment_data = equipment()
    return render_template('equipmentManager.html', equipment_data = equipment_data)

def equipment():
    equipment_row = Equipment.get_all_equipment()
    equipment_data = []
    for i in equipment_row:
        equipment = {
            '編號': i[0],
            '器材名稱': i[1],
            '位置': i[2],
            '數量': i[3],
            '備註': i[4],
            '組別名稱': i[5]
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
            return redirect(url_for('manager_new.equipmentManager'))
        if len(equipment_name) < 1:
            flash('設備名稱不可為空。')
            return redirect(url_for('manager_new.equipmentManager'))

        Equipment.add_equipment(
            {
            'equipment_name' : equipment_name,
            'equipment_status' : equipment_status,
            'equipment_description' : equipment_description
            }
        )

        return redirect(url_for('manager_new.equipmentManager'))
    
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
        return redirect(url_for('manager_new.equipmentManager'))
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
        aSeq = request.values.get('delete')
        Activity.delete_activity(aSeq)

    elif 'edit' in request.values:
        aSeq = request.values.get('edit')
        return redirect(url_for('manager_new.edit_activity', aSeq=aSeq))

    elif 'view' in request.values:
        aSeq = request.values.get('view')
        return redirect(url_for('manager_new.programManager', aSeq=aSeq))

    activity_data = activity()
    return render_template('activityManager.html', activity_data = activity_data)

def activity():
    activity_row = Activity.get_all_activity()
    activity_data = []
    for i in activity_row:
        activity = {
            '序號': i[0],
            '活動名稱': i[1],
            '日期': i[2],
            '地點': i[3]
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
            return redirect(url_for('manager_new.activityManager'))
        if len(activity_name) < 1:
            flash('活動名稱不可為空。')
            return redirect(url_for('manager_new.activityManager'))

        Activity.add_activity(
            {
            'activity_name' : activity_name,
            'activity_date' : activity_date,
            'activity_description' : activity_description
            }
        )

        return redirect(url_for('manager_new.activityManager'))
    
    return render_template('activityManager.html')

@manager_new.route('/edit_activity', methods=['GET', 'POST'])
def edit_activity():
    if request.method == 'POST':
        print(f"\n\n\n\n\n\n")
        Activity.update_activity(
            {
            'activity_name' : request.values.get('activity_name'),
            'activity_date' : request.values.get('activity_date'),
            'activity_description' : request.values.get('description'),
            'aSeq' : request.values.get('aSeq')
            }
        )
        return redirect(url_for('manager_new.activityManager'))
    else:
        activity = show_activity_info()
        return render_template('edit_activity.html', data=activity)

def show_activity_info():
    aSeq = request.args['aSeq']
    data = Activity.get_activity(aSeq)
    activity_name = data[1]
    activity_date = data[2]
    activity_description = data[3]
    
    activity = {
        '活動編號': aSeq,
        '活動名稱': activity_name,
        '活動日期': activity_date,
        '活動描述': activity_description
    }
    return activity

# =================== Program Management =====================
@manager_new.route('/programManager', methods=['GET', 'POST'])
def programManager():
    aSeq = request.values.get('aSeq')
    # print(f"Debug: aSeq = {aSeq}")
    # print(f"Request values: {request.values}")
    if not aSeq:
        print("活動編號缺失，無法顯示節目列表。")
        flash('活動編號缺失，無法顯示節目列表。')
        return redirect(url_for('manager_new.activityManager'))
    

    if 'delete' in request.values:
        print("Delete program")
        composite_key  = request.values.get('delete')
        aSeq, program_time = composite_key.split('|', 1)
        Program.delete_program(aSeq, program_time)
        return redirect(url_for('manager_new.programManager', aSeq=aSeq))
    elif 'edit_program' in request.values:
        print("Edit program")
        composite_key = request.values.get('edit_program')
        aSeq, program_time = composite_key.split('|', 1)

        return redirect(url_for('manager_new.edit_program', aSeq=aSeq, program_time=program_time))

   
    program_data = program(aSeq)
    return render_template('programManager.html', program_data=program_data, aSeq=aSeq)

def program(aSeq):
    program_row = Program.get_activity_program(aSeq)
    program_data = []
    for i in program_row:
        program = {
            '活動序號': i[0],
            '節目時間': i[1],
            '曲目': i[2]
        }
        program_data.append(program)
    return program_data

@manager_new.route('/add_program', methods=['POST'])
def add_program():
    if request.method == 'POST':

        # note: not completed
        program_name = request.values.get('program_name')
        program_host = request.values.get('program_host')
        program_time = request.values.get('program_time')

        # validation, can be extended
        if program_name is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager_new.programManager'))
        if len(program_name) < 1:
            flash('節目名稱不可為空。')
            return redirect(url_for('manager_new.programManager'))

        Program.add_program(
            {
            'program_name' : program_name,
            'program_host' : program_host,
            'program_time' : program_time
            }
        )

        return redirect(url_for('manager_new.programManager'))
    
    return render_template('programManager.html')

@manager_new.route('/edit_program', methods=['GET', 'POST'])
def edit_program():
    if request.method == 'POST':
        aSeq = request.values.get('aSeq')
        Program.update_program(
            {
            'program_name' : request.values.get('program_name'),
            'program_host' : request.values.get('program_host'),
            'program_time' : request.values.get('program_time'),
            'program_id' : request.values.get('program_id')
            }
        )
        return redirect(url_for('manager_new.programManager', aSeq=aSeq))
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