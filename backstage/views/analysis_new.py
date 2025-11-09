from flask import render_template, Blueprint, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from api.sql_new import Analysis

analysis_new = Blueprint('analysis_new', __name__, template_folder='../templates')

@analysis_new.route('/dashboard', methods=['GET'])
def dashboard():
    # 1) 各活動參加人數
    participants_rows = Analysis.count_participants()
    participants_data = [
        {'活動名稱': r[0], '參加人數': r[1]} for r in participants_rows
    ]

    # 2) 活動節目明細（活動名稱、節目名稱、表演者）
    act_detail_rows = Analysis.activity_detail()
    activity_detail = [
        {'活動名稱': r[0], '節目名稱': r[1], '表演者': r[2]} for r in act_detail_rows
    ]

    # 3) 節目器材使用（節目名稱、器材名稱、數量）
    equip_usage_rows = Analysis.equipment_usage()
    equipment_usage = [
        {'節目名稱': r[0], '器材名稱': r[1], '數量': r[2]} for r in equip_usage_rows
    ]

    # 4) 後勤歸屬（組別、器材名稱、成員）
    equip_belongs_rows = Analysis.equipment_belongs()
    equipment_belongs = [
        {'組別': r[0], '器材名稱': r[1], '成員': r[2]} for r in equip_belongs_rows
    ]

    # 5)（可選）單一學生參與紀錄：?sName=王小明
    s_name = request.args.get('sName')
    student_participation = []
    if s_name:
        sp_rows = Analysis.student_participation(s_name)
        student_participation = [
            {'學號': r[0], '學生': r[1], '活動名稱': r[2]} for r in sp_rows
        ]

    return render_template(
        'dashboard.html',
        participants_data=participants_data,
        activity_detail=activity_detail,
        equipment_usage=equipment_usage,
        equipment_belongs=equipment_belongs,
        student_participation=student_participation,
        sName=s_name or ""
    )
