from . import database
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class Teacher(database.Model):
    teacher_id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(100))
    degree = database.Column(database.String(100))
    phd = database.Column(database.Boolean, default = False, nullable = False)
    in_dept = database.Column(database.String(100))
    dept_id = database.Column(database.Integer, database.ForeignKey('department.id'))


class Admin(database.Model, UserMixin):
    __tablename__= 'admins'
    id = database.Column(database.Integer, primary_key = True)
    email = database.Column(database.String(100))
    password = database.Column(database.String(120))
    name = database.Column(database.String(100))

class Student(database.Model):
    __tablename__ = 'students'
    student_id = database.Column(database.Integer, primary_key = True)
    email = database.Column(database.String(100))
    firstname = database.Column(database.String(100))
    lastname = database.Column(database.String(100))
    course_id = database.Column(database.Integer, database.ForeignKey('courses.id'))
    course_name = database.Column(database.String(100))
    dept_id = database.Column(database.String(100), database.ForeignKey("department.id"))


class Course(database.Model):
    __tablename__ = 'courses'
    id = database.Column(database.Integer)
    course_name = database.Column(database.String(100),primary_key = True)
    students = database.relationship('Student', backref = 'students',lazy='dynamic')
    def __repr__(self):
        return f'{self.course_id} {self.course_name} '
    

class Department(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    name = database.Column(database.String(100))
    teachers = database.relationship('Teacher', backref='teacher',lazy='dynamic')
    students = database.relationship('Student', backref='student',lazy='dynamic')