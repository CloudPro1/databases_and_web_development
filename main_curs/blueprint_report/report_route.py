import os
from flask import Blueprint, render_template, request, current_app
from access import group_required
from database.sql_provider import SQLProvider
from .report_model_route import model_route

bp_report = Blueprint('bp_report', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@bp_report.route('/', methods=['GET'])
@group_required
def reports_menu_handle():
    return render_template('choose_reports.html')

@bp_report.route('/accounting', methods=['GET'])
@group_required
def choose_report_handle():
    return render_template('reports_menu.html')

@bp_report.route('/accounting/create', methods=['GET'])
@group_required
def create_report_handle():
    return render_template('create_report.html')

@bp_report.route('/accounting/create', methods=['POST'])
@group_required
def create_report_form():
    user_input = request.form
    result_info = model_route(current_app.config['db_config'], provider, user_input, 'create_report.sql')
    if not result_info.status or not result_info.result:
        return render_template('create_report.html', message="Ошибка: " + result_info.error_message)
    message = result_info.result[0][0]
    return render_template('create_report.html', message=message)

@bp_report.route('/accounting/show', methods=['GET'])
@group_required
def show_report_handle():
    return render_template('show_report.html')

@bp_report.route('/accounting/show', methods=['POST'])
@group_required
def show_report_form():
    user_input = request.form
    result_info = model_route(current_app.config['db_config'],provider, user_input, 'get_report.sql')
    print(result_info)
    if result_info.status:
        reports = result_info.result
        report_title = 'Отчёт по отработанным часам'
        return render_template('report_result.html', report_title=report_title, reports=reports)
    else:
        return render_template('show_report.html', message='Отчёт не найден')