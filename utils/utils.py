import datetime


def utc_str_to_local_str(utc_str: str):
    utc_format = '%Y-%m-%dT%H:%M:%SZ'
    local_format = '%d.%m.%Y'
    temp1 = datetime.datetime.strptime(utc_str, utc_format)
    temp2 = temp1.replace(tzinfo=datetime.timezone.utc)
    local_time = temp2.astimezone()
    return local_time.strftime(local_format)

def date_str_to_local_str(date_str: str):
    local_str = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%d.%m.%Y')
    return local_str

def today_to_local_str():
    local_str = datetime.datetime.today().strftime('%d.%m.%Y')
    return local_str