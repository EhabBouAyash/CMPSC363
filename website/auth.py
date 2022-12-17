from flask import Blueprint, render_template,request,flash,redirect,url_for
from .models import Student, Teacher, Admin, Course, Department
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth',__name__)
from flask_login import login_user, login_required, logout_user, current_user
from . import database

#login

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password,password):
                flash('Log in was successful!',category='success')
                login_user(admin,remember=True)
                redirect(url_for('views.home'))

            else:
                flash("Incorrect password or email, try again",category='error')
        else:
            flash("Email not found. ", category="error")
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    if request.method=="POST":
        email = request.form.get('email')
        firstname = request.form.get("firstName")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            flash("This email already exists", category='error' )

        elif len(email)<4:
            flash('Email is too short. Must be greater than 3 characters.',category = "error")
        elif len(firstname)<2:
            flash('First name must be greater than 1 characters.',category = "error")
        elif password!=password2:
            flash('Passwords dont match',category = "error")
        elif len(password)<4:
            flash('Password must be at least 4 characters',category = "error")
        else:
            #add user
            newuser = Admin(name = firstname, email= email, password=generate_password_hash(password,method = "md5"))
            database.session.add(newuser)
            database.session.commit()
            login_user(newuser,remember=True)
            flash("Account created. ", category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user=current_user)


@auth.route('/course_insert',methods=['GET', 'POST'])
def course_insert():
    if request.method=="POST":
        _id = request.form.get('course_id')
        cname = request.form.get('course_name')
        course = Course.query.filter_by(id=_id).first()
        if course:
            flash("This course already exists", category='error' )

        else:
            #add user
            newcourse = Course(id=_id, course_name=cname)
            database.session.add(newcourse)
            database.session.commit()
            flash("Course Added. ", category="success")
    return render_template("course_insert.html", user = current_user)


@auth.route('/course_update', methods=['GET', 'POST'])
def course_update():
    if request.method=="POST":
        id= request.form.get("course_id")
        name = request.form.get('course_name')
        course = Course.query.filter_by(id=id).first()
        if course:
            course.course_name = name
            database.session.commit()
    return render_template('course_update.html',user=current_user)

@auth.route('/course_query',methods=['GET','POST'])
def course_query():
    if request.method=="POST":
        id= request.form.get("course_id")
        course = Course.query.filter_by(id=id).first()
        if course:
            data = [i for i in Course.query.with_entities(Course.id,Course.course_name).filter_by(id=id).all()]
            print(data)
            return render_template("table.html",headings=course_headings,data=data,user=current_user)
    return render_template('course_query.html',user=current_user)
@auth.route('/course_delete',methods=['GET','POST'])
def course_delete():
    if request.method=="POST":
        id = request.form.get("course_id")
        course = Course.query.filter_by(id=id).first()
        database.session.delete(course)
        database.session.commit()
        return render_template('course_delete.html', user=current_user)
    return render_template('course_delete.html',user=current_user)



course_headings = ("Course ID", "Course Name")

@auth.route('/courses',methods=['GET','POST'])
def courses():
    #display courses
    data =[i for i in Course.query.with_entities(Course.id, Course.course_name)]
    print(data)
    return render_template("courses.html",headings=course_headings,data=data,user=current_user)

student_headings = ("ID", "Email", "First Name", "Last Name", "Course Registered")
@auth.route('/students',methods=['GET','POST'])
def students():
    #display courses
    data =[i for i in Student.query.with_entities(Student.student_id, Student.email,Student.firstname,Student.lastname,Student.course_name)]
    print(data)
    return render_template("students.html",headings=student_headings,data=data,user=current_user)
    

@auth.route('/student_query', methods=['GET', 'POST'])
def student_query():
    if request.method=="POST":
        id= request.form.get("student_id")
        student = Student.query.filter_by(student_id =id).first()
        if student:
            data = [i for i in Student.query.with_entities(Student.student_id,Student.firstname,Student.lastname,Student.email,Student.course_name).filter_by(student_id=id).all()]
            print(data)
            return render_template("table.html",headings=student_headings,data=data,user=current_user)
    
    return render_template('student_query.html',user=current_user)


@auth.route('/student_update', methods=['GET', 'POST'])
def student_update():
    if request.method=="POST":
        id= request.form.get("student_id")
        course = request.form.get('course_name')
        student = Student.query.filter_by(student_id =id).first()
        if student:
            student.course_name = course
            database.session.commit()
    return render_template('student_update.html',user=current_user)

@auth.route('/student_insert',methods=['GET','POST'])
def student_insert():
    if request.method=="POST":
        _id = request.form.get('student_id')
        first = request.form.get('firstname')
        last = request.form.get('lastname')
        email = request.form.get('email')
        coursename = request.form.get('course')
        courseid = request.form.get('course')
        student = Student.query.filter_by(student_id=_id).first()
        if student:
            flash("This student already exists.", category='error')
        else:
            newstudent = Student(student_id=_id, firstname=first, lastname=last, email=email,course_name=coursename, course_id=courseid)
            database.session.add(newstudent)
            database.session.commit()
            flash("Added Student.")
    return render_template("student_insert.html", user = current_user)

@auth.route("student_delete", methods=['GET','POST'])
def student_delete():
    if request.method=="POST":
        id = request.form.get("student_id")
        student = Student.query.filter_by(student_id=id).first()
        database.session.delete(student)
        database.session.commit()
        return render_template('student_delete.html', user=current_user)
    return render_template('student_delete.html', user=current_user)


department_headings =("ID", "Name")
@auth.route('/departments',methods=['GET','POST'])
def departments():
    #display courses
    data =[i for i in Department.query.with_entities(Department.id, Department.name)]
    print(data)
    return render_template("departments.html",headings=department_headings,data=data,user=current_user)

@auth.route('/departments_insert',methods=['GET', 'POST'])
def departments_insert():
    if request.method=="POST":
        _id = request.form.get('department_id')
        name = request.form.get('department_name')
        dept = Department.query.filter_by(id=_id).first()
        if dept:
            flash("This department already exists", category='error' )

        else:
            #add user
            newdept = Department(id=_id, name=name)
            database.session.add(newdept)
            database.session.commit()
            flash("Department Added. ", category="success")
    return render_template("departments_insert.html", user = current_user)


@auth.route('/departments_query',methods=['GET','POST'])
def departments_query():
    if request.method=="POST":
        id= request.form.get("department_id")
        dept = Department.query.filter_by(id =id).first()
        if dept:
            data = [i for i in Department.query.with_entities(Department.id,Department.name).filter_by(id=id).all()]
            print(data)
            return render_template("table.html",headings=department_headings,data=data,user=current_user)
    
    return render_template('departments_query.html',user=current_user)

@auth.route("departments_delete", methods=['GET','POST'])
def departments_delete():
    if request.method=="POST":
        id = request.form.get("department_id")
        dept = Department.query.filter_by(id=id).first()
        database.session.delete(dept)
        database.session.commit()
        return render_template('departments_delete.html', user=current_user)
    return render_template('departments_delete.html', user=current_user)


teacher_headings = ('ID', 'Name', 'Degree', 'PHD', 'Department', 'Department ID')
@auth.route('/teachers',methods=['GET','POST'])
def teachers():
    #display courses
    data =[i for i in Teacher.query.with_entities(Teacher.teacher_id, Teacher.name, Teacher.degree, Teacher.phd,Teacher.in_dept, Teacher.dept_id)]
    print(data)
    return render_template("teachers.html",headings=teacher_headings,data=data,user=current_user)


@auth.route('/teachers_query',methods=['GET','POST'])
def teachers_query():
    if request.method=="POST":
        id= request.form.get("teacher_id")
        teacher = Teacher.query.filter_by(teacher_id =id).first()
        if teacher:
            data = [i for i in Teacher.query.with_entities(Teacher.teacher_id,Teacher.name,Teacher.degree,Teacher.phd,Teacher.in_dept, Teacher.dept_id).filter_by(teacher_id=id).all()]
            print(data)
            return render_template("table.html",headings=teacher_headings,data=data,user=current_user)
    return render_template('teachers_query.html',user=current_user)
@auth.route('/teachers_insert',methods=['GET', 'POST'])
def teachers_insert():
    if request.method=="POST":
        id = request.form.get('teacher_id')
        name = request.form.get('teacher_name')
        degree = request.form.get('teacher_degree')
        phd = request.form.get('teacher_phd')=='True'
        department = request.form.get('teacher_department')
        departmentid = request.form.get('department_id')

        teacher = Teacher.query.filter_by(teacher_id=id).first()
        if teacher:
            flash("This teacher already exists", category='error' )

        else:
            #add user
            newteacher = Teacher(teacher_id=id, name=name, degree=degree, phd=phd, in_dept = department, dept_id=id)
            database.session.add(newteacher)
            database.session.commit()
            flash("Teacher Added. ", category="success")
    return render_template("teachers_insert.html", user = current_user)

@auth.route("/teachers_delete", methods=['GET','POST'])
def teachers_delete():
    if request.method=="POST":
        id = request.form.get("teacher_id")
        teacher = Teacher.query.filter_by(teacher_id=id).first()
        database.session.delete(teacher)
        database.session.commit()
        return render_template('teachers_delete.html', user=current_user)
    return render_template('teachers_delete.html', user=current_user)

@auth.route('/teachers_update', methods=['GET', 'POST'])
def teachers_update():
    if request.method=="POST":
        id= request.form.get("teacher_id")
        name = request.form.get('teacher_name')
        teacher = Teacher.query.filter_by(teacher_id =id).first()
        if teacher:
            teacher.name = name
            database.session.commit()
    return render_template('teachers_update.html',user=current_user)
