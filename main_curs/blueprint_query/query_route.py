import os
from flask import render_template, request, Blueprint, current_app
from .query_model_route import *
from database.sql_provider import SQLProvider
from access import group_required

bp_query = Blueprint('bp_query', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_query.route('/',methods=['GET'])
@group_required
def query_menu():
    return render_template('query_menu.html')

@bp_query.route('/input_1_sql')
@group_required
def input_1request():
    return render_template('input_1req.html')

@bp_query.route('/result_req_1', methods=['POST'])
@group_required
def result_1_req():
    user_input = request.form
    print("request.form = ", user_input)
    res = model_route_req_1(current_app.config['db_config'], user_input, provider)
    if res.result:
        query_title = f'Результат запроса по зарплате водителя {user_input["driver_name"]}'
        return render_template("result1.html", bouquets=res.result, query_title=query_title)
    else:
        return render_template('comeback.html', message="Данные не найдены")

@bp_query.route('/input_2_sql')
@group_required
def input_2request():
    return render_template('input_2req.html')

@bp_query.route('/result_req_2', methods=['POST'])
@group_required
def result_2_req():
    user_input = request.form
    print("request.form = ", user_input)
    res = model_route_req_2(current_app.config['db_config'], user_input, provider)
    if res.result:
        query_title = f'Расписание маршрута {user_input["route"]} за {user_input["month"]}/{user_input["year"]}'
        return render_template("result2.html", bouquets=res.result, query_title=query_title)
    else:
        return render_template('comeback.html', message="Данные не найдены")

@bp_query.route('/input_3_sql')
@group_required
def input_3request():
    return render_template('input_3req.html')

@bp_query.route('/result_req_3', methods=['POST'])
@group_required
def result_3_req():
    user_input = request.form
    search_value = user_input['report_month'] + '%'
    modified_input = {'report_month': search_value}

    res = model_route_req_3(current_app.config['db_config'], modified_input, provider)
    if res.result:
        query_title = f'Троллейбусы серии "{user_input["report_month"]}"'
        return render_template("result3.html", bouquets=res.result, query_title=query_title)
    else:
        return render_template('comeback.html', message="Данные не найдены")

