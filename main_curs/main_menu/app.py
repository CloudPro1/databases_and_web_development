import json
import sys
import os
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..") 
)
from flask import Flask, session, render_template, json, redirect, url_for
from blueprint_query.query_route import bp_query
from blueprint_auth.auth_route import auth_bp
from blueprint_report.report_route import bp_report
from blueprint_schedule.schedule_route import bp_schedule
from access import login_required

app = Flask(__name__)
app.register_blueprint(bp_query, url_prefix = '/query')
app.secret_key = 'No one knows'
app.register_blueprint(auth_bp, url_prefix = '/auth')
app.register_blueprint(bp_report, url_prefix='/reports')
app.register_blueprint(bp_schedule, url_prefix='/schedule')

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

db_config_path = os.path.join(current_dir, '..', 'data', 'db_config.json') 
with open(db_config_path) as f:  
    app.config['db_config'] = json.load(f)

db_access_path = os.path.join(current_dir, '..', 'data', 'db_auth_check.json')
with open(db_access_path) as f:
    app.config['db_access'] = json.load(f)


@app.route('/')
@login_required
def main_menu():
    return render_template('main_menu.html')

@app.route('/exit')
def exit_func():
    if 'user_group' in session:
        session.clear()
        return redirect(url_for('main_menu'))
    return redirect(url_for('main_menu'))

@app.route('/error')
def error_message():
    return render_template("error.html", message="Где-то ошибка")

if __name__ == '__main__':
    app.run(debug=True, port=5005)