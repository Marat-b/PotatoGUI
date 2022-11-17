from classes.request_data import RequestData
from db.services.session_service import SessionService
from db.services.request_data_service import RequestDataService


def save_session_data(rdata: RequestData):
    new_session_id = SessionService.new_session_id()
    print(f'new_session_id={new_session_id}')
    RequestDataService.save(new_session_id, rdata)
    print('Data is saves!')