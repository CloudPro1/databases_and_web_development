import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataclasses import dataclass
from database.select import select_list


@dataclass
class InfoResponse:
    result: tuple
    status: bool
    err_message: str


def model_route_req_1(db_config, user_input: dict, provider):
    err_message = ''
    _sql = provider.get('1.sql')
    result, schema = select_list(db_config, _sql, user_input['driver_name'])
    if result:
        return InfoResponse(result, status=True, err_message=err_message)
    else:
        return InfoResponse(tuple(), status=True, err_message=err_message)

def model_route_req_2(db_config, user_input: dict, provider):
    err_message = ''
    _sql = provider.get('2.sql')
    result, schema = select_list(db_config, _sql, params=(
    user_input['route'],
    user_input['year'],
    user_input['month']))
    if result:
        return InfoResponse(result=result, status=True, err_message=err_message)
    else:
        return InfoResponse(tuple(), status=True, err_message=err_message)

def model_route_req_3(db_config, user_input: dict, provider):
    err_message = ''
    _sql = provider.get('3.sql')
    result, schema = select_list(db_config, _sql, user_input['report_month'])
    if result:
        return InfoResponse(result=result, status=True, err_message=err_message)
    else:
        return InfoResponse(tuple(), status=True, err_message=err_message)


