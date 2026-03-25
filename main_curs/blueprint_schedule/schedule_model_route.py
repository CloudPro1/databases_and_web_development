from dataclasses import dataclass
from database.select import select_dict
from database.insert import insert_one


@dataclass
class InfoResponse:
    result: tuple
    status: bool
    err_message: str


def sch_do(db_config, provider, sql: str) -> InfoResponse:
    err_message = ""
    
    try:
        _sql = provider.get(sql)
        result = select_dict(db_config, _sql)
        
        if result:
            return InfoResponse(result=result, status=True, err_message=err_message)
        else:
            err_message = 'Данные не получены'
            return InfoResponse(result=(), status=False, err_message=err_message)
    
    except Exception as e:
        err_message = f'Ошибка при выполнении запроса: {str(e)}'
        return InfoResponse(result=(), status=False, err_message=err_message)
    
def sch_new(db_config, provider, sql_1, info, data=None) -> InfoResponse:
    
    err_message = ""
    try:
        _sql1 = provider.get(sql_1)
        # _sql2 = provider.get(sql_2)

        # result2 = insert_one(db_config, _sql2, data)
        result = insert_one(db_config, _sql1, info)

        if result:
            return InfoResponse(result=result, status=True, err_message=err_message)
        else:
            err_message = 'Данные не получены'
            return InfoResponse(result=(), status=False, err_message=err_message)
    
    except Exception as e:
        err_message = f'Ошибка при выполнении запроса: {str(e)}'
        return InfoResponse(result=(), status=False, err_message=err_message)
    
def sch_show(db_config, provider, sql, date) -> InfoResponse:
    err_message = ""
    try:
        _sql = provider.get(sql)
        result = select_dict(db_config, _sql, (date,))
        # result2 = insert_one(db_config, _sql2, data)
        # result = insert_one(db_config, _sql1, info)

        if result:
            return InfoResponse(result=result, status=True, err_message=err_message)
        else:
            err_message = 'Данные не получены'
            return InfoResponse(result=(), status=False, err_message=err_message)
    
    except Exception as e:
        err_message = f'Ошибка при выполнении запроса: {str(e)}'
        return InfoResponse(result=(), status=False, err_message=err_message)