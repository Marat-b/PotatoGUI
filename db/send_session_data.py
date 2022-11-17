from classes.http_request import HttpRequest
from db.services.request_data_service import RequestDataService
from db.services.session_service import SessionService


def send_session_data(hr: HttpRequest):
    sessions = SessionService().get_sessions()
    # print(f'sessions={sessions}')
    for s in sessions:
        # print(f's.SessionId={s.SessionId}')
        rdata = RequestDataService().get(s.SessionId)
        # print(f'rdata={rdata}')
        if rdata is not None:
            ret = hr.send_request(rdata.data)
            # print(f'ret={ret}')
            if ret:
                # print(f's.SessionId={s.SessionId}')
                SessionService().update_session(s.SessionId)