from typing import List

from classes.request_data import RequestData
from db.services.parameter_service import ParameterService
from db.services.request_data_service import RequestDataService
from db.services.session_service import SessionService
from utils.utils import date_str_to_local_str, today_to_local_str


class OfflinePrint:
     data = {'document': '', 'id': '', 'number': '', 'start_date': '', 'start_time':''}

     @classmethod
     def _get_records(self) -> List[RequestData]:
          records = []
          sessions = SessionService.get_sessions()
          for session in sessions:
               record = RequestDataService.get(session.SessionId)
               if record is not None:
                    records.append(record)
          return records

     @classmethod
     def get_data(self, limit: int):
       datas = []
       records = self._get_records()
       for i, record in enumerate(records):
              if limit > i:
                     data = self.data.copy()
                     data['id'] = record.operator_id
                     data['number'] = str(i + 1)
                     data['start_date'] = date_str_to_local_str(record.start_date)
                     data['start_time'] = record.start_time
                     data['document'] = self._get_document(record)
                     datas.append(data)
       return datas

     @classmethod
     def _get_document(self, record: RequestData):
          text = f"<HTML><p style=\"text-align: center;\"><strong>РЕЗУЛЬТАТ АНАЛИЗА</strong></p>" \
                 "<p style=\"text-align: center;\"><strong>Общая информация</strong></p>" \
                 "<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">" \
                 "<tbody>" \
                 "<tr>" \
                 f"<td style=\"width: 50%;\">Дата/время начала:</td><td style=\"width: 50%;\">" \
                 f"{date_str_to_local_str(record.start_date)} " \
                 f"{record.start_time}</td>" \
                 "</tr>" \
                 "<tr>" \
                 f"<td style=\"width: 50%;\">Дата/время завершения:</td><td style=\"width: 50%;\">" \
                 f"{date_str_to_local_str(record.end_date)} " \
                 f"{record.end_time}</td>" \
                 "</tr>" \
                 "<tr>" \
                 f"<td style=\"width: 50%;\">Оператор:</td><td style=\"width: 50%;\">{record.operator_name} " \
                 f"{record.operator_patronymic} {record.operator_surname}</td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Адрес:</td>" \
                 f"<td style=\"width: 50%;\">{ParameterService.get_address()}</td>" \
                 "</tr>" \
                 "</tbody>" \
                 "</table>" \
                 "<p style=\"text-align: center;\"><strong>Данные партии</strong></p>" \
                 "<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">" \
                 "<tbody>" \
                 "<tr>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Параметр</strong></td>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Значение</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Поставщик:</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.provider}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Получатель:</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.recipient}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Марка ТС:</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.car}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Государственный номер:</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.gosnomer}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Ботанический сорт</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.botanical_variety}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Заявленный объем</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.declared_volume}</strong></td>" \
                 "</tr>" \
                 "</tbody>" \
                 "</table>" \
                 "<p style=\"text-align: center;\"><strong>Статистические данные</strong></p>" \
                 "<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">" \
                 "<tbody>" \
                 "<tr>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Параметр</strong></td>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Значение</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Общее количество клубней (шт.):</td>" \
                 f"<td style=\"width: 50%; text-align: left;\"><strong>{record.total_count}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Крупный калибр (шт.):</td>" \
                 f"<td style=\"width: 50%;\"><strong>{record.large_caliber}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Средний калибр (шт.)</td><td style=\"width: " \
                 f"50%;\"><strong>{record.medium_caliber}</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Мелкий калибр (шт.)</td>" \
                 f"<td style=\"width: 50%;\"><strong>{record.small_caliber}</strong></td>" \
                 "</tr>" \
                 "</tbody>" \
                 "</table>" \
                 "<p style=\"text-align: center;\"><strong>Заболевания</strong></p>" \
                 "<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">" \
                 "<tbody>" \
                 "<tr>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Параметр</strong></td>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Значение</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Фитофтороз</td>" \
                 "<td style=\"width: 50%;\"><strong>0</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Серебристая парша</td>" \
                 "<td style=\"width: 50%;\"><strong>0</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Ростовые трещины</td><td style=\"width: 50%;\"><strong>0</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Мелкий калибр (шт.)</td>" \
                 "<td style=\"width: 50%;\"><strong>0</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Повреждения (шт.)</td>" \
                 "<td style=\"width: 50%;\"><strong>0</strong></td>" \
                 "</tr>" \
                 "<tr>" \
                 "<td style=\"width: 50%;\">Гнилая (шт.)</td>" \
                 f"<td style=\"width: 50%;\"><strong>{record.rot}</strong></td>" \
                 "</tr>" \
                 "</tbody>" \
                 "</table>" \
                 "<p> </p>" \
                 "<p> </p>" \
                 "<p> </p>" \
                 "<p> </p>" \
                 "<p> </p>" \
                 "<p> </p>" \
                 "<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">" \
                 "<tbody>" \
                 "<tr>" \
                 "<td style=\"width: 50%; text-align: center;\"><strong>Дата формирования</strong></td>" \
                 f"<td style=\"width: 50%; text-align: center;\"><strong>{today_to_local_str()}</strong></td>" \
                 "</tr>" \
                 "</html>"
          return text

