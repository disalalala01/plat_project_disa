
"""
Ассинхронный код для записи в базу что бы сразу показать из JSON и тут по быстрому зписать в  БД
использовать ассинхронный ORM для ДБ
Принимает : JSON распредиляет и записывает в базу можно при большом трффике запихать в очередь
Должен принимать user_id для понимания к какому user-у записовать
"""

import logging
from datetime import datetime

from platonus.models import Mark, Subject, Teacher, session_db


def main(data, user_id):
    try:
        if data['msg'] == 'success':

            for obj in data['content']:
                try:
                    subjects = Subject(name=obj['subject'], user_id=user_id)
                    session_db.add(subjects)
                    session_db.flush()
                    teachers = Teacher(name=obj['teacher'], subject_id=subjects.id)
                    session_db.add(teachers)

                    for mark in obj['marks']:
                        obj_mark = {
                            'created': datetime.now(),
                            'last_updated': datetime.now(),
                            'mark': mark,
                            'user_id': user_id,
                            'subject_id': subjects.id
                        }
                        mark_obj = Mark(**obj_mark)
                        session_db.add(mark_obj)
                    session_db.commit()
                except Exception as e:
                    session_db.rollback()
                    print(e)
        else:
            logging.error('msa is not success')
            pass
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    main()