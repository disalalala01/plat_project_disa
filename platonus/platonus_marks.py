from bs4 import BeautifulSoup
import requests


"""
Главный парсер для (оценок, учителей, груп, ... для Журнала)
Отдает JSON для показа и записи в базу
"""


mark_url = 'https://edu.enu.kz/current_progress_gradebook_student'

import write_to_db


def get_all(session):
    try:
        result = {}
        headers = {
            'Host': 'edu.enu.kz',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': 'https://edu.enu.kz/templates/JSF/schedule/studentScheduleViewer.xhtml?',
            'Accept-Language': 'ru',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        user_id = session['user_id']
        del session['user_id']
        test_list = []
        marks = []
        resp = requests.get(mark_url, headers=headers, cookies=session)
        soup = BeautifulSoup(resp.text, 'lxml')
        trs = soup.find('div', class_='table-responsive').find('table', class_='table table-compact-2x bordered').find(
            'tbody').find_all('tr', class_='subject')
        for tr in trs:
            tds = tr.find_all('td')
            subject = tds[0].text
            teacher = tds[2].text
            for i in range(3, 10):
                marks.append(tds[i].text)
            data = {
                'subject': subject,
                'teacher': teacher,
                'marks': marks
            }
            test_list.append(data)
        result['msg'] = 'success'
        result['content'] = test_list
        # write_to_db.main(result, user_id)
        return result
    except Exception as e:
        # logger.exception(e)
        print(e)