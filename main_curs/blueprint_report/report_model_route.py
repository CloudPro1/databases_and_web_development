from dataclasses import dataclass
from database.select import select_list


@dataclass
class InfoResponse:
    result: tuple
    error_message: str
    status: bool

def model_route(db_config, provider, user_input: dict, sql_file):
    err_message = ''
    _sql = provider.get(sql_file)

    params = [user_input.get('month'), user_input.get('year')]
        
    try:
        print(params)
        result, schema = select_list(db_config, _sql, params)
        if result:
            return InfoResponse(result=result, error_message=err_message, status=True)
        else:
            # print("lol2")
            err_message = 'Данные не получены - пустой результат'
            return InfoResponse(result=result, error_message=err_message, status=False)
    except Exception as e:
        err_message = f'Ошибка при выполнении запроса: {str(e)}'
        return InfoResponse(result=None, error_message=err_message, status=False)