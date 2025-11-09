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
    logistic_data = Logistic.get_all_logistic()
    dummy_student = type('S', (), {'lName': ''})()

    return render_template(
        'studentManager.html', 
        student_data=student_data,
        logistic_data=logistic_data,
        student=dummy_student
    )

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
        
        existing = Student.get_student(sId)
        if existing:
            flash('failed with UniqueViolation')
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
    
    logistic_data = Logistic.get_all_logistic()
    dummy_student = type('S', (), {'lName': ''})()
    
    return render_template(
        'studentManager.html', 
        student_data=student(), 
        logistic_data=logistic_data, 
        student=dummy_student
    )

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
    return render_template('logisticManager.html', logistic_data=Logistic_data)

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
        
        existing = Logistic.get_logistic(lName)
        if existing:
            flash('failed with UniqueViolation')
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
        eId = request.values.get('delete')
        Equipment.delete_equipment(eId)

    elif 'edit' in request.values:
        eId = request.values.get('edit')
        return redirect(url_for('manager_new.edit_equipment', eId=eId))

    equipment_data = equipment()
    logistic_data = Logistic.get_all_logistic()
    dummy_equipment = type('S', (), {'lName': ''})()

    return render_template(
        'equipmentManager.html', 
        equipment_data=equipment_data, 
        logistic_data=logistic_data, 
        equipment=dummy_equipment
    )


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

        eId = request.values.get('eId')
        eName = request.values.get('eName')
        eLocation = request.values.get('eLocation')
        Quantity = request.values.get('Quantity')
        Note = request.values.get('Note')
        lName = request.values.get('lName')

        # validation, can be extended
        if eName is None or Quantity is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager_new.equipmentManager'))
        if len(eName) < 1:
            flash('設備名稱不可為空。')
            return redirect(url_for('manager_new.equipmentManager'))
        
        existing = Equipment.get_equipment(eId)
        if existing:
            flash('failed with UniqueViolation')
            return redirect(url_for('manager_new.equipmentManager'))

        Equipment.create_equipment(
            {
                'eId': eId,
                'eName': eName,
                'eLocation': eLocation,
                'Quantity': Quantity,
                'Note': Note,
                'lName': lName
            }
        )

        return redirect(url_for('manager_new.equipmentManager'))
    
    logistic_data = Logistic.get_all_logistic()
    dummy_equipment = type('S', (), {'lName': ''})()

    return render_template(
        'equipmentManager.html',
        equipment_data=equipment(),
        logistic_data=logistic_data,
        equipment=dummy_equipment
    )

@manager_new.route('/edit_equipment', methods=['GET', 'POST'])
def edit_equipment():
    if request.method == 'POST':
        Equipment.update_equipment(
            {
                'eName' : request.values.get('eName'),
                'eLocation' : request.values.get('eLocation'),
                'Quantity' : request.values.get('Quantity'),
                'Note' : request.values.get('Note'),
                'lName' : request.values.get('lName'),
                'eId' : request.values.get('eId')                
            }
        )
        return redirect(url_for('manager_new.equipmentManager'))
    else:
        equipment = show_equipment_info()
        logistic_data = Logistic.get_all_logistic()
        return render_template('equipmentEditor.html', equipment=equipment, logistic_data=logistic_data)

def show_equipment_info():
    eId = request.args['eId']
    record = Equipment.get_equipment(eId)
    data = record[0]
    eName = data[1]
    eLocation = data[2]
    Quantity = data[3]
    Note = data[4]
    lName = data[5]
    
    equipment = {
        'eId': eId,
        'eName': eName,
        'eLocation': eLocation,
        'Quantity': Quantity,
        'Note': Note,
        'lName': lName
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

    elif 'participant' in request.values:
        aSeq = request.values.get('participant')
        return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))

    activity_data = activity()
    return render_template('activityManager.html', activity_data=activity_data)

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

        aSeq = request.values.get('aSeq')
        aName = request.values.get('aName')
        activityDate = request.values.get('activityDate')
        aLocation = request.values.get('aLocation')

        # validation, can be extended
        if aName is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager_new.activityManager'))
        if len(aName) < 1:
            flash('活動名稱不可為空。')
            return redirect(url_for('manager_new.activityManager'))
        
        existing = Activity.get_activity(aSeq)
        if existing:
            flash('failed with UniqueViolation')
            return redirect(url_for('manager_new.activityManager'))

        Activity.create_activity(
            {
            'aSeq' : aSeq,
            'aName' : aName,
            'activityDate' : activityDate,
            'aLocation' : aLocation
            }
        )

        return redirect(url_for('manager_new.activityManager'))
    
    return render_template('activityManager.html')

@manager_new.route('/edit_activity', methods=['GET', 'POST'])
def edit_activity():
    if request.method == 'POST':
        Activity.update_activity(
            {
                'aName' : request.values.get('aName'),
                'activityDate' : request.values.get('activityDate'),
                'aLocation' : request.values.get('aLocation'),
                'aSeq' : request.values.get('aSeq')
            }
        )
        return redirect(url_for('manager_new.activityManager'))
    else:
        activity = show_activity_info()
        return render_template('activityEditor.html', activity=activity)

def show_activity_info():
    aSeq = request.args['aSeq']
    record = Activity.get_activity(aSeq)
    data = record[0]
    aName = data[1]
    activityDate = data[2]
    aLocation = data[3]

    activity = {
        'aSeq': aSeq,
        'aName': aName,
        'activityDate': activityDate,
        'aLocation': aLocation
    }
    return activity

# =================== Program Management =====================
@manager_new.route('/programManager', methods=['GET', 'POST'])
def programManager():
    aSeq = request.values.get('aSeq')

    if not aSeq:
        flash('活動編號缺失，無法顯示節目列表。')
        return redirect(url_for('manager_new.activityManager'))
    
    if 'delete' in request.values:
        composite_key  = request.values.get('delete')
        if composite_key is None:
            flash('無法刪除節目，缺少必要的識別資訊。')
            return redirect(url_for('manager_new.programManager', aSeq=aSeq))
        aSeq, programTime = composite_key.split('|', 1)
        Program.delete_program(aSeq, programTime)
        return redirect(url_for('manager_new.programManager', aSeq=aSeq))
    
    elif 'edit_program' in request.values:
        composite_key = request.values.get('edit_program')
        if composite_key is None:
            flash('無法編輯節目，缺少必要的識別資訊。')
            return redirect(url_for('manager_new.programManager', aSeq=aSeq))
        aSeq, programTime = composite_key.split('|', 1)
        return redirect(url_for('manager_new.edit_program', aSeq=aSeq, programTime=programTime))

   
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
        aSeq = request.values.get('aSeq')
        programTime = request.values.get('programTime')
        Song = request.values.get('Song')

        # validation, can be extended
        if programTime is None or Song is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager_new.programManager'))
        if len(programTime) < 1:
            flash('節目時間不可為空。')
            return redirect(url_for('manager_new.programManager'))
        if len(Song) < 1:
            flash('曲目名稱不可為空。')
            return redirect(url_for('manager_new.programManager'))
        
        existing = Program.get_program(aSeq, programTime)
        print(f"program: {existing}")
        if existing:
            flash('failed with UniqueViolation')
            return redirect(url_for('manager_new.programManager', aSeq=aSeq))

        Program.create_program(
            {
                'aSeq' : aSeq,
                'programTime' : programTime,
                'Song' : Song
            }
        )

        return redirect(url_for('manager_new.programManager', aSeq=aSeq))
    
    return render_template('programManager.html')

@manager_new.route('/edit_program', methods=['GET', 'POST'])
def edit_program():
    aSeq = request.values.get('aSeq')
    if request.method == 'POST':
        Program.update_program(
            {
                'new_programTime' : request.values.get('new_programTime'),
                'Song' : request.values.get('Song'),
                'aSeq' : aSeq,
                'programTime' : request.values.get('programTime')
            }
        )
        print(f"Updated program: {aSeq}, {request.values.get('programTime')}, {request.values.get('Song')}")
        return redirect(url_for('manager_new.programManager', aSeq=aSeq))
    else:
        program = show_program_info()
        return render_template('programEditor.html', program=program)

def show_program_info():
    aSeq = request.args['aSeq']
    programTime = request.args['programTime']
    record = Program.get_program(aSeq, programTime)
    data = record[0]
    # aSeq = data[0]
    # programTime = data[1]
    Song = data[2]
    
    program = {
        'aSeq': aSeq,
        'programTime': programTime,
        'Song': Song
    }
    return program

# =================== Activity Participant Management =====================
@manager_new.route('/activityJoinManager', methods=['GET', 'POST'])
def activityJoinManager():
    aSeq = request.values.get('aSeq')
    if not aSeq:
        flash('缺少活動編號')
        return redirect(url_for('manager_new.activityManager'))
    
    if 'delete' in request.values:
        sId = request.values.get('delete')
        StudentJoin.delete_participate_activity(aSeq, sId)
        return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))

    participant_data = activityJoin(aSeq)
    return render_template('activityJoinManager.html', participants=participant_data, aSeq=aSeq)

def activityJoin(aSeq):
    activityJoin_row = StudentJoin.get_participate_activity_by_activity(aSeq)
    participant_data = []
    for i in activityJoin_row:
        activityJoin = {
            '參與學生學號': i[0],
            '參與學生姓名': i[1]
        }
        participant_data.append(activityJoin)
    return participant_data

@manager_new.route('/add_activityJoin', methods=['POST'])
def add_activityJoin():
    if request.method == 'POST':
        aSeq = request.values.get('aSeq')
        sId = request.values.get('sId')
        
        # validation, can be extended
        if sId is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))
        if len(sId) < 1:
            flash('學生學號不可為空。')
            return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))

        sId_existing = Student.get_student(sId)
        print(f"check {sId_existing}")
        if not sId_existing:
            flash('failed with ForeignKeyViolation')
            return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))

        existing = StudentJoin.get_participate_activity(aSeq, sId)
        print(f"check {existing}")
        if existing:
            flash('failed with UniqueViolation')
            return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))
        

        StudentJoin.create_participate_activity(
            {
                'aSeq' : aSeq,
                'sId' : sId
            }
        )

        return redirect(url_for('manager_new.activityJoinManager', aSeq=aSeq))

    return render_template('activityJoinManager.html')