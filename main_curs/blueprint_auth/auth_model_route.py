from dataclasses import dataclass
from database.select import select_string
from werkzeug.security import check_password_hash

@dataclass
class InfoResponse:
    result: tuple
    error_message: str
    status: bool
    
def auth_req(db_config, user_input_data, sql_provider):
    # _sql = sql_provider.get('user.sql', input_login=user_input_data['login'])
    _sql = sql_provider.get('user.sql')
    result = select_string(db_config, _sql, (user_input_data['login'],))
    
    if not result:
        return InfoResponse(result, error_message="Пользователь не найден", status=False)
    
    stored_hash = result[0][2]
    if check_password_hash(stored_hash, user_input_data['password']):
        return InfoResponse(result, error_message='', status=True)
    else:
        return InfoResponse([], error_message="Неверный пароль", status=False)

