from typing import Optional

import requests


def test_get_point(pinpoint) -> Optional[str]:
    try:
        response = requests.get(f'http://erp.bk-nt.ru/api/point/pair/{pinpoint}' )
        print(response.status_code)
        if response.status_code == 200:
            r = response.json()
            print(f'response={r["data"]}')
            return  r["data"]
        else:
            return None
    except Exception as e:
        return None

if __name__ == "__main__":
    print(test_get_point(638980))