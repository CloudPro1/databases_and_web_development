from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from blueprint_auth.auth_model_route import auth_req
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
sql_path = os.path.join(os.path.dirname(__file__), 'sql')
print("SQL folder path:", sql_path)
print("Files:", os.listdir(sql_path))

@auth_bp.route('/login', methods=['GET'])
def auth_index():
    if 'user_group' in session:
        session.clear()
    return render_template('auth.html')


@auth_bp.route('/login', methods=['POST'])
def auth_main():
    user_data = request.form
    print(request.form)
    res_info = auth_req(current_app.config['db_config'], user_data, provider) 
    # print(res_info)
    if not res_info.result:
        return render_template('error_auth.html', message=res_info.error_message)

    session['user_group'] = res_info.result[0][3]
    session['user_id'] = res_info.result[0][0]
    session.permanent = True
    
    # print('Выполнена аутентификация')
    return redirect(url_for('main_menu'))


