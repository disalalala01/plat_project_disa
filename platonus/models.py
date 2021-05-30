from sqlalchemy.orm import relationship

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import Config

engine = create_engine(f'postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}')
session_db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session_db.query_property()


class Mark(Base):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP)
    last_updated = db.Column(db.TIMESTAMP)
    mark = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    # subject_status = db.Column(db.String(50))
    # rubejka = db.Column(db.Integer)# FIXME Рубежка

    def __init__(self, created, last_updated, mark, user_id, subject_id):
        self.created = created
        self.last_updated = last_updated
        self.mark = mark
        self.user_id = user_id
        self.subject_id = subject_id


class Subject(Base):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(50))
    schedule_time = relationship('ScheduleTime', backref='subject', lazy=True)
    marks = relationship('Mark', backref='subject', lazy=True)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.status = None

    # def save(self): # FIXME check for duplicate or not
    #     try:
    #         q = Subjec
    #     except Exception:
    #         session_db.rollback()
    #         raise


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    iin = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    course = db.Column(db.Integer)
    subjects = relationship('Subject', backref='user', lazy=True)
    schedules = relationship('Schedule', backref='user', lazy=True)

    def __init__(self, iin, password):
        self.iin = iin
        self.password = password

    @classmethod
    def get(cls, iin):
        try:
            user = cls.query.filter(cls.iin == iin).first()
            if user:
                return user.id
            else:
                return False
        except Exception as e:
            session_db.rollback()
            print(e)


class ScheduleTime(Base):
    __tablename__ = 'schedule_time'
    id = db.Column(db.Integer, primary_key=True)
    class_time = db.Column(db.TIMESTAMP)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))


class Teacher(Base):#FIXME
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    def __init__(self, name, subject_id):
        self.name = name
        self.subject_id = subject_id


class Schedule(Base):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    schedule_time = db.Column(db.Integer, db.ForeignKey('schedule_time.id'))


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
