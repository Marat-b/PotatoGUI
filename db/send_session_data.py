from classes.http_request import HttpRequest
from db.services.request_data_service import RequestDataService
from db.services.session_service import SessionService


def send_session_data(hr: HttpRequest, data):
    sessions = SessionService().get_sessions()
    # print(f'sessions={sessions}')
    for s in sessions:
        # print(f's.SessionId={s.SessionId}')
        rdata = RequestDataService().get(s.SessionId)
        rdata.operator_id = data['operator_id']
        rdata.operator_name = data['operator_name']
        rdata.operator_surname = data['operator_surname']
        rdata.operator_patronymic = data['operator_patronymic']
        # print(f'rdata={rdata}')
        if rdata is not None:
            ret = hr.send_request(data['token'], rdata.data)
            # print(f'ret={ret}')
            if ret:
                # print(f's.SessionId={s.SessionId}')
                SessionService().update_session(s.SessionId)