import os
from flask import Blueprint, session, current_app, render_template, request, redirect, url_for, flash
from database.sql_provider import SQLProvider

from access import group_required
from database.DB_context_manager import DBContextManager
from blueprint_schedule.schedule_model_route import *

bp_schedule = Blueprint ('bp_schedule', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

def get_schedule():
    if 'schedule' not in session:
        session['schedule'] = {}
    return session['schedule']

def drivers_num(items):
    total = 0
    for item in items:
        total += 1
    return total

@bp_schedule.route('/', methods=['GET', 'POST'])
@group_required
def choose_date():
    if request.method == 'POST':
        session['schedule_date'] = request.form['schedule_date']
        return redirect(url_for('bp_schedule.schedule'))
    return render_template('choose_date.html')


@bp_schedule.route('/plan/', methods=['GET', 'POST'])
@group_required
def schedule():
    """Отображение и изменение расписания"""
    db_config = current_app.config['db_config']
    schedule = get_schedule()
    
    if request.method == 'POST':
        dr_id = request.form.get('dr_id')
        route_id = request.form.get('route_id')
        driver_name = request.form.get('name')
        work_start = request.form.get('work_start')
        work_finished = request.form.get('work_finished')

        schedule[driver_name] = {
        'dr_id': dr_id,
        'route_id': route_id,
        'work_start': work_start,
        'work_finished': work_finished
        }
        
        if not route_id:
            current_app.logger.error(f'route_id is empty. Form data: {dict(request.form)}')
            flash('Ошибка: не указан маршрут', 'error')
            return redirect(url_for('bp_schedule.schedule'))
        session['schedule'] = schedule
        session.modified = True
        return redirect(url_for('bp_schedule.schedule'))
    
    else:
        
        drivers_res_info = sch_do(db_config, provider, 'select_drivers.sql')
        routs_res_info = sch_do(db_config, provider, 'select_routes.sql')
        print(drivers_res_info)

        if not drivers_res_info.result:
            return render_template('sch_error.html', message=drivers_res_info.err_message)
        elif not routs_res_info.result:
            return render_template('sch_error.html', message=routs_res_info.err_message)
        else:
            drivers = drivers_res_info.result
            routs = routs_res_info.result
        
        dr_total = drivers_num(drivers)
        assigned_drivers = len(schedule)
        dr_needed = dr_total - assigned_drivers
        schedule_date = session.get('schedule_date')
        # work_start = session
        
        
        return render_template(
            'schedule_plan.html', 
            items=drivers,
            routs=routs,
            date=schedule_date, 
            dr_total=assigned_drivers,
            dr_needed=dr_needed,
            schedule=schedule
        )

@bp_schedule.route('plan/save_schedule', methods=['GET','POST'])
@group_required
def save_schedule():
    if request.method == 'POST':
        session.pop('schedule_date', None)
        session.pop('schedule', None)
        return redirect(url_for('bp_schedule.post_sch'))
    else:
        db_config = current_app.config['db_config']
        date = session.get('schedule_date')

        delete_db = sch_new(db_config, provider, 'sch_delete.sql', (date,))
        if not delete_db.result:
            return render_template('sch_error.html', message=delete_db.err_message)
    
        for driver, info in session['schedule'].items():
            drivers_schedule = (info['dr_id'], info['route_id'], 
                            date, 
                            info['work_start'], info['work_finished'])
            sch_db = sch_new(db_config, provider, 'schedule_new.sql', drivers_schedule, date)
        
            if not sch_db.result:
                return render_template('sch_error.html', message=sch_db.err_message)

        reports_res_info = sch_show(db_config, provider, 'show_table.sql', date)
        reports = reports_res_info.result
        return render_template('schedule_is_ready.html', 
                            date=date,
                            reports=reports)
    

@bp_schedule.route('/plan/sch_is_ready', methods=['GET'])
@group_required
def post_sch():
    return render_template('schedule_posted.html')
      
    
@bp_schedule.route('/plan/clear_session', methods=['GET', 'POST'])
@group_required
def clear_session():
    session.pop('schedule', None)
    flash('Сессия очищена', 'info')
    return redirect(url_for('bp_schedule.schedule'))

