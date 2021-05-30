import requests
import logging
from config import Config
import json

login_url = 'https://edu.enu.kz/rest/api/login'

"""
{'auth_token': 'b95327af-d0d5-42c7-bfdc-680a5c3e213b', 'login_status': 'success', 'sid': '7fd9518e939ffd1e7b580f0a28b4f964'}
"""

from models import User, session_db
from platonus import cache


def get_session(iin, password):# FIXME Get username from main_page
    try:
        student_session_key = f'student-{iin}'
        headers = {
            'Host': 'edu.enu.kz',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'https://edu.enu.kz/template.html',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
        session_from_cache = cache.get(student_session_key)
        if not session_from_cache:
            with requests.Session() as session:
                payload = {
                    'login': None,
                    'iin': f"{iin}",
                    'icNumber': f"{iin}",
                    'password': f"{password}"
                }
                response = session.post(login_url, json=payload, headers=headers)
                student_session = session.cookies.get_dict()
                result = response.json()  # FIXME cache result
                if result['login_status'] != 'success':
                    return False, False
                else:
                    exist = User.get(iin=iin)
                    if not exist:
                        student = User(iin=iin, password=password)
                        session_db.add(student)
                        session_db.flush()
                        session_db.commit()
                        exist = student.id
                    student_session['user_id'] = exist
                    session_encode = json.dumps(student_session, indent=2).encode('utf-8')
                    cache.set(student_session_key, session_encode, ex=60 * 60 * 4)
                    return student_session
        else:
            # print('get from cache')
            session_decode = json.loads(session_from_cache)
            return session_decode
    except Exception as e:
        # logger.exception(e)
        print(e)


if __name__ == '__main__':
    get_session(iin=Config.LOGIN, password=Config.PASSWORD)
