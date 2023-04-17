from flask import *
import cv2
import mediapipe as mp
import requests
import numpy as np
from src.dbconnectionnew import *
from src.dbconnectionnew import *
from werkzeug.utils import secure_filename
import os
from _thread import start_new_thread
import face_recognition
import argparse
import pickle
from src.encode_faces import enf
import wmi
f = wmi.WMI()
app = Flask(__name__)
app.secret_key="dfgdf"
import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('index.html')
        return func()

    return secure_function

@app.route('/')
def log():
    return render_template("index.html")

@app.route('/login',methods=['post'])
def login():
    username=request.form['textfield']
    password=request.form['textfield2']

    qry="select * from login where username=%s and password=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return'''<script>alert("invalid");
        window.location="/"</script>'''
    elif res['type']=='admin':
        session['lid']=res['id']
        return '''<script>alert("valid");
               window.location="/admin_home"</script>'''

    elif res['type']=='staff':
        session['lid'] = res['id']
        return '''<script>alert("valid");
               window.location="/staff_home"</script>'''
    elif res['type']=='student':
        session['cnt'] = 0
        session['lid'] = res['id']
        return '''<script>alert("valid");
               window.location="/studenthome"</script>'''
    else:
        return '''<script>alert("invalid");
               window.location="/"</script>'''



@app.route('/logout',methods=['get','post'])
def logout():
    session.clear()
    return render_template("index.html")


@app.route('/admin_home')
@login_required
def admin_home():
    return render_template("aindex.html")

@app.route('/staff_home')
@login_required
def staff_home():
    return render_template("staff/sindex.html")


@app.route('/manage_timetable')
@login_required
def manage_timetable():
    q="SELECT `timetable`.*,`exam`.`exam` FROM `exam` JOIN `timetable` ON `timetable`.`exam_id`=`exam`.`id`"
    res=selectall(q)
    return render_template("add and manage timetable.html",val=res)


@app.route('/delete_timetable')
@login_required
def delete_timetable():
    id=request.args.get('id')
    q="DELETE FROM `timetable` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_timetable"</script>'''


@app.route('/staff',methods=['post'])
@login_required
def staff():
    return render_template("add staff.html")

@app.route('/hall',methods=['post'])
@login_required
def hall():
    return render_template("add hall.html")

@app.route('/add')
@login_required
def add():
    return render_template("add.html")

@app.route('/allocation')
@login_required
def allocation():
    return render_template("add allocation.html")

@app.route('/manage_course')
@login_required
def manage_course():
    qry = "select * from course"
    res = selectall(qry)
    return render_template("add and manage course.html",val = res)


@app.route('/delete_course')
@login_required
def delete_course():
    id=request.args.get('id')
    q="DELETE FROM `course` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_course"</script>'''



@app.route('/manage_examdetails')
@login_required
def manage_examdetails():
    qry = "SELECT `exam`.*,`subject`.`subject` FROM `subject` JOIN `exam` ON `exam`.`subject_id`=`subject`.`id`"
    res = selectall(qry)
    return render_template("add and manage exam details.html",val=res)




@app.route('/delete_examdetails')
@login_required
def delete_examdetails():
    id=request.args.get('id')
    q="DELETE FROM `exam` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_examdetails"</script>'''



@app.route('/manage_hall')
@login_required
def manage_hall():
    qry = "select *from hall"
    res = selectall(qry)
    return render_template("add and manage hall.html",val = res)

@app.route('/manage_staff')
@login_required
def manage_staff():
    qry = "select *from staff"
    res = selectall(qry)
    return render_template("add and manage staff.html",val=res)








@app.route('/addstaff',methods=['post'])
@login_required
def addstaff():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    gender=request.form['radiobutton']
    dob=request.form['textfield3']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    phone=request.form['textfield7']
    email=request.form['textfield8']
    uname=request.form['textfield9']
    pswd=request.form['textfield10']
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'staff')"
    val=(uname,pswd)
    id=iud(qry,val)
    q="INSERT INTO `staff` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    v=(str(id),fname,lname,gender,dob,place,post,pin,phone,email)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_staff"</script>'''



@app.route('/editstaff')
@login_required
def editstaff():
    id=request.args.get('id')
    session['estid']=id
    q="SELECT * FROM `staff` WHERE `login_id`=%s"
    res=selectone(q,str(id))
    return render_template("editstaff.html",val=res)





@app.route('/editstaff1',methods=['post'])
@login_required
def editstaff1():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    gender=request.form['radiobutton']
    dob=request.form['textfield3']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    phone=request.form['textfield7']
    email=request.form['textfield8']
    q="update `staff` SET `first_name`=%s,`last_name`=%s,`gender`=%s,`dob`=%s,`place`=%s,`post`=%s,`pin`=%s,`phone`=%s,`email`=%s WHERE `login_id`=%s"
    v=(fname,lname,gender,dob,place,post,pin,phone,email,session['estid'])
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_staff"</script>'''



@app.route('/delete_staff')
@login_required
def delete_staff():
    id=request.args.get('id')
    q="DELETE FROM `login` WHERE `id`=%s"
    iud(q,str(id))

    q = "DELETE FROM `staff` WHERE `login_id`=%s"
    iud(q, str(id))
    return '''<script>alert("deleted");window.location="/manage_staff"</script>'''




@app.route('/manage_subject')
@login_required
def manage_subject():
    qry = "SELECT `subject`.*,`course`.`course` FROM `course` JOIN `subject` ON `course`.`id`=`subject`.`course_id`"
    res = selectall(qry)
    return render_template("add and manage subject.html",val=res)

@app.route('/delete_subject')
@login_required
def delete_subject():
    id=request.args.get('id')
    q="DELETE FROM `subject` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_subject"</script>'''



@app.route('/delete_hall')
@login_required
def delete_hall():
    id=request.args.get('id')
    q="DELETE FROM `hall` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_hall"</script>'''


@app.route('/course',methods=['post'])
@login_required
def course():
    return render_template("add course.html")

@app.route('/addcourse',methods=['post'])
@login_required
def addcourse():
    course=request.form['textfield']
    details=request.form['textfield2']
    q="INSERT INTO `course` VALUES(NULL,%s,%s)"
    v=(course,details)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_course"</script>'''



@app.route('/editcourse')
@login_required
def editcourse():
    id=request.args.get('id')
    session['ecid']=id
    q="SELECT* FROM `course` WHERE `id`=%s"
    res=selectone(q,str(id))
    return render_template("editcourse.html",val=res)

@app.route('/editcourse1',methods=['post'])
@login_required
def editcourse1():
    course=request.form['textfield']
    details=request.form['textfield2']
    q="update course SET `course`=%s,`details`=%s WHERE `id`=%s"
    v=(course,details,session['ecid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/manage_course"</script>'''





@app.route('/subject',methods=['post'])
@login_required
def subject():
    q="SELECT * FROM `course`"
    res=selectall(q)
    return render_template("add subject.html",val=res)

@app.route('/addsubject',methods=['post'])
@login_required
def addsubject():
    sem=request.form['select']
    course=request.form['select2']
    sub=request.form['textfield']
    q="INSERT INTO `subject` VALUES(NULL,%s,%s,%s)"
    v=(course,sub,sem)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_subject"</script>'''


@app.route('/editsubject')
@login_required
def editsubject():
    id = request.args.get('id')
    session['esid'] = id
    q = "SELECT* FROM `subject` WHERE `id`=%s"
    res1 = selectone(q, str(id))
    q="SELECT * FROM `course`"
    res=selectall(q)
    return render_template("editsubject.html",val=res,val1=res1)

@app.route('/editsubject1',methods=['post'])
@login_required
def editsubject1():
    sem=request.form['select']
    course=request.form['select2']
    sub=request.form['textfield']
    q="UPDATE `subject` SET `course_id`=%s,`subject`=%s,`sem`=%s WHERE `id`=%s"
    v=(course,sub,sem,session['esid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/manage_subject"</script>'''




@app.route('/timetable',methods=['post'])
@login_required
def timetable():
    q = "SELECT * FROM `exam`"
    res = selectall(q)
    return render_template("add timetable.html",val=res)

@app.route('/addtimetable',methods=['post'])
@login_required
def addtimetable():
    eid=request.form['select']
    timetable=request.files['file']
    tim=secure_filename(timetable.filename)
    timetable.save(os.path.join('static/timetable',tim))
    q=" INSERT INTO `timetable` VALUES(NULL,%s,%s,CURDATE())"
    v=(tim,eid)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_timetable"</script>'''



@app.route('/allocate_examhall',methods=['post'])
@login_required
def allocate_examhall():
    q = "SELECT * FROM `exam`"
    res = selectall(q)
    q1 = "SELECT * FROM `hall`"
    r = selectall(q1)
    return render_template("allocate exam hall.html",val=res,v=r)


@app.route('/allocate_examhall1',methods=['post'])
@login_required
def allocate_examhall1():
    exm=request.form['select']
    hall=request.form['select2']
    qry="SELECT * FROM `examhall_allocation` WHERE `exam_id`=%s"
    res=selectone(qry,exm)
    if res is None:

        q="INSERT INTO `examhall_allocation` VALUES(NULL,%s,%s)"
        v=(exm,hall)
        iud(q,v)
        return '''<script>alert("allocated");window.location="/allocation_exam"</script>'''
    else:
        return '''<script>alert("already allocated");window.location="/allocation_exam"</script>'''




@app.route('/allocate_staff',methods=['post'])
@login_required
def allocate_staff():
    q="SELECT * FROM `staff`"
    res=selectall(q)
    q1="SELECT * FROM `subject`"
    r=selectall(q1)
    return render_template("allocate staff.html",val=res,v=r)

@app.route('/allocatesub',methods=['post'])
@login_required
def allocatesub():
    stid=request.form['select']
    sub=request.form['select2']
    qry="SELECT * FROM `assign_sub` WHERE `staff_id`=%s AND `subject_id`=%s"
    va=(stid,sub)
    res=selectone(qry,va)
    if res is None:
        q="INSERT INTO `assign_sub` VALUES(NULL,%s,%s)"
        v=(stid,sub)
        iud(q,v)
        return '''<script>alert("allocated");window.location="/allocate_subject"</script>'''

    else:
        return '''<script>alert(" already allocated");window.location="/allocate_subject"</script>'''


@app.route('/allocate_subject')
@login_required
def allocate_subject():
    q="SELECT `subject`.`subject`,`staff`.`first_name`,`last_name`,`assign_sub`.* FROM `staff` JOIN `assign_sub` ON `assign_sub`.`staff_id`=`staff`.`login_id` JOIN `subject` ON `subject`.`id`=`assign_sub`.`subject_id`"
    res=selectall(q)
    return render_template("allocate subject for staff.html",val=res)


@app.route('/deleteallocation')
@login_required
def deleteallocation():
    id=request.args.get('id')
    q="DELETE FROM `assign_sub` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/allocate_subject"</script>'''



@app.route('/exam_details',methods=['post'])
@login_required
def exam_details():
    q = "SELECT * FROM `subject`"
    res = selectall(q)
    return render_template("exam details.html",val=res)

@app.route('/addexam_details',methods=['post'])
@login_required
def addexam_details():
    cid=request.form['select']
    exm=request.form['textfield']
    det=request.form['time']
    date=request.form['textfield3']
    q="INSERT INTO `exam` VALUES(NULL,%s,%s,%s,%s)"
    v=(cid,exm,det,date)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_examdetails"</script>'''


@app.route('/editexm_details')
@login_required
def editexm_details():
    id=request.args.get('id')
    session['exmid']=id
    qry="SELECT * FROM `exam` WHERE `id`=%s"
    res1=selectone(qry,str(id))
    q = "SELECT * FROM `subject`"
    res = selectall(q)
    return render_template("editexamdetails.html",val=res,val1=res1)

@app.route('/editexm_details1',methods=['post'])
@login_required
def editexm_details1():
    cid=request.form['select']
    exm=request.form['textfield']
    det=request.form['textarea']
    date=request.form['textfield3']
    q="UPDATE `exam` SET `subject_id`=%s,`exam`=%s,`time`=%s,`date`=%s WHERE `id`=%s"
    v=(cid,exm,det,date,session['exmid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/manage_examdetails"</script>'''




@app.route('/hall_to_staff',methods=['post'])
@login_required
def hall_to_staff():
    q = "SELECT * FROM `staff`"
    res = selectall(q)
    qry="SELECT `examhall_allocation`.*,`exam`.`exam`,`hall`.`hall_no` FROM `examhall_allocation` JOIN `exam` ON `exam`.`id`=`examhall_allocation`.`id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id`"
    r=selectall(qry)
    return render_template("assign hall to staff.html",v=r,val=res)

@app.route('/hall_to_staff1',methods=['post'])
@login_required
def hall_to_staff1():
    sid=request.form['select']
    allid=request.form['select2']
    q="INSERT INTO `hall allocation to staff` VALUES(NULL,%s,%s)"
    v=(allid,sid)
    iud(q,v)
    return '''<script>alert("allocated");window.location="/hall_allocation_staff"</script>'''




@app.route('/assign_duties',methods=['post'])
@login_required
def assign_duties():
    q="SELECT * FROM `staff`"
    res=selectall(q)
    return render_template("assign duties.html",val=res)

@app.route('/assign_duty',methods=['post'])
@login_required
def assign_duty():
    staff=request.form['select']
    duty=request.form['textfield']
    q="INSERT INTO `assign_duties` VALUES(NULL,%s,%s,CURDATE(),'pending')"
    v=(staff,duty)
    iud(q,v)
    return '''<script>alert("assigned");window.location="/assign_duties_to_staff"</script>'''



@app.route('/assign_duties_to_staff')
@login_required
def assign_duties_to_staff():
    q="SELECT `assign_duties`.*,`staff`.`first_name`,`last_name` FROM `staff` JOIN `assign_duties` ON `assign_duties`.`staff_id`=`staff`.`login_id`"
    res=selectall(q)
    return render_template("assign duties to staff.html",val=res)

@app.route('/hall_allocation_staff')
@login_required
def hall_allocation_staff():
    q="SELECT `hall allocation to staff`.*,`exam`.`exam`,`hall`.`hall_no`,`staff`.`first_name`,`last_name` FROM `exam` JOIN `examhall_allocation` ON `examhall_allocation`.`exam_id`=`exam`.`id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id` JOIN `hall allocation to staff` ON `hall allocation to staff`.`examhall_id`=`examhall_allocation`.`id` JOIN `staff` ON `staff`.`login_id`=`hall allocation to staff`.`staff_id`"
    res=selectall(q)
    return render_template("hall allocation to staff.html",val=res)


@app.route('/dltallocation')
@login_required
def dltallocation():
    id=request.args.get('id')
    q="DELETE FROM `hall allocation to staff` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/hall_allocation_staff"</script>'''


@app.route('/allocation_exam')
@login_required
def allocation_exam():
    q="SELECT `examhall_allocation`.*,`exam`.`exam`,`hall`.`hall_no` FROM `examhall_allocation` JOIN `exam` ON `exam`.`id`=`examhall_allocation`.`id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id`"
    res=selectall(q)
    return render_template("hall allocaton to exam.html",val=res)



@app.route('/dltallocation_exam')
@login_required
def dltallocation_exam():
    id=request.args.get('id')
    q="DELETE FROM `examhall_allocation` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/hall_allocation_staff"</script>'''



###############################staff##########################

@app.route('/managestudent')
@login_required
def managestudent():
    q="SELECT `student`.*,`course`.`course` FROM `student` JOIN `course` ON `course`.`id`=`student`.`course_id`"
    res=selectall(q)

    return render_template("staff/add&manage student.html",v=res)

@app.route('/addstudent',methods=['post'])
@login_required
def addstudent():
    q="SELECT* FROM `course` "
    res=selectall(q)
    return render_template("staff/add student.html",v=res)


@app.route('/addstudent1',methods=['post'])
@login_required
def addstudent1():
    FirstName = request.form['textfield']
    LastName = request.form['textfield2']
    Gender = request.form['RadioGroup1']
    Dob = request.form['textfield3']
    Place = request.form['textfield4']
    Post = request.form['textfield5']
    Pin = request.form['textfield6']
    Phone = request.form['textfield7']
    Email = request.form['textfield8']
    un = request.form['textfield9']
    pwd = request.form['textfield10']
    crs = request.form['select']
    sem = request.form['select2']
    photo=request.files['file']
    eee=secure_filename(photo.filename)
    photo.save(os.path.join('static/student',eee))

    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'student')"
    val=(un,pwd)
    id=iud(qry,val)
    q="INSERT INTO `student` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    v=(str(id),FirstName,LastName,Gender,Dob,Place,Post,Pin,crs,sem,Phone,Email,eee)
    iud(q,v)
    return '''<script>alert("added");window.location="/managestudent"</script>'''



@app.route('/mngnotes')
@login_required
def mngnotes():
    q="SELECT `notes`.*,`subject`.`subject` FROM `subject` JOIN `notes` ON `notes`.`subject_id`=`subject`.`id`"
    res=selectall(q)
    return render_template("staff/add & manage notes.html",val=res)


@app.route('/addnotes',methods=['post'])
@login_required
def addnotes():
    q="SELECT `subject`.* FROM `subject` JOIN `assign_sub` ON `assign_sub`.`subject_id`=`subject`.`id` WHERE `assign_sub`.`staff_id`=%s"
    res=selectall2(q,session['lid'])
    print(res)
    return render_template("staff/add notes.html",val=res)

@app.route('/addnotes1',methods=['post'])
@login_required
def addnotes1():
    sub=request.form['select']
    note=request.files['file']
    n=secure_filename(note.filename)
    note.save(os.path.join('static/notes',n))
    q="INSERT INTO `notes` VALUES(NULL,%s,%s)"
    v=(sub,n)
    iud(q,v)
    return '''<script>alert("added");window.location="/mngnotes"</script>'''




@app.route('/mngqnpaper')
@login_required
def mngqnpaper():
    q="SELECT `questionpaper`.*,`subject`.`subject` FROM `subject` JOIN `questionpaper` ON `questionpaper`.`subjet_id`=`subject`.`id`"
    res=selectall(q)
    return render_template("staff/add & manage qstn paper.html",val=res)


@app.route('/addqnpaper',methods=['post'])
@login_required
def addqnpaper():
    q="SELECT `subject`.* FROM `subject` JOIN `assign_sub` ON `assign_sub`.`subject_id`=`subject`.`id` WHERE `assign_sub`.`staff_id`=%s"
    res=selectall2(q,session['lid'])
    print(res)
    return render_template("staff/add qstn paper.html",val=res)

@app.route('/addqnpaper1',methods=['post'])
@login_required
def addqnpaper1():
    sub=request.form['select']
    note=request.files['file']
    n=secure_filename(note.filename)
    note.save(os.path.join('static/question',n))
    q="INSERT INTO `questionpaper` VALUES(NULL,%s,%s)"
    v=(n,sub)
    iud(q,v)
    return '''<script>alert("added");window.location="/mngqnpaper"</script>'''

@app.route('/viewallocatedsub')
@login_required
def viewallocatedsub():
    q = "SELECT `subject`.* FROM `subject` JOIN `assign_sub` ON `assign_sub`.`subject_id`=`subject`.`id` WHERE `assign_sub`.`staff_id`=%s"
    res = selectall2(q, session['lid'])
    print(res)
    return render_template("staff/view allocated subject.html",val=res)




@app.route('/viewassignedworks')
@login_required
def viewassignedworks():
    q = "SELECT * FROM `assign_duties` WHERE `staff_id`=%s"
    res = selectall2(q, session['lid'])
    print(res)
    return render_template("staff/view assigned works.html",val=res)


@app.route('/updatestts')
@login_required
def updatestts():
    id=request.args.get('id')
    session['duid']=id
    return render_template("staff/status.html")

@app.route('/updatestts1',methods=['post'])
@login_required
def updatestts1():
    stts=request.form['ss']
    q="UPDATE `assign_duties` SET `status`=%s WHERE `id`=%s"
    v=(stts,session['duid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/viewassignedworks"</script>'''




@app.route('/viewallocatedhall')
@login_required
def viewallocatedhall():
    q = "SELECT `hall allocation to staff`.*,`exam`.`exam`,`hall`.`hall_no` FROM `hall allocation to staff` JOIN `examhall_allocation` ON `examhall_allocation`.`id`=`hall allocation to staff`.`examhall_id` JOIN `exam` ON `exam`.`id`=`examhall_allocation`.`exam_id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id` WHERE `hall allocation to staff`.`staff_id`=%s"
    res = selectall2(q, session['lid'])
    print(res)
    return render_template("staff/view allocated hall.html",val=res)

@app.route('/dltstudent')
@login_required
def dltstudent():
    id=request.args.get('id')
    q="DELETE FROM `login` WHERE `id`=%s"
    iud(q,str(id))
    qry="DELETE FROM `student` WHERE `login_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("deleted");window.location="/managestudent"</script>'''

@app.route('/dltnote')
@login_required
def dltnote():
    id = request.args.get('id')
    q = "DELETE FROM `notes` WHERE `id`=%s"
    iud(q, str(id))
    return '''<script>alert("deleted");window.location="/mngnotes"</script>'''


@app.route('/dltquestion')
@login_required
def dltquestion():
    id = request.args.get('id')
    q = "DELETE FROM `questionpaper` WHERE `id`=%s"
    iud(q, str(id))
    return '''<script>alert("deleted");window.location="/mngqnpaper"</script>'''



@app.route('/viewmalpractice')
@login_required
def viewmalpractice():
    qry="SELECT `malpractice`.*,`student`.`first_name`,`last_name` FROM `malpractice` JOIN `student` ON `student`.`login_id`=`malpractice`.`studid`"
    res=selectall(qry)
    print(res)
    return render_template("staff/viewmalpractice.html",val=res)


@app.route('/viewmalpractice1')
@login_required
def viewmalpractice1():
    qry="SELECT `malpractice`.*,`student`.`first_name`,`last_name` FROM `malpractice` JOIN `student` ON `student`.`login_id`=`malpractice`.`studid`"
    res=selectall(qry)
    return render_template("viewmalpractice.html",val=res)



@app.route('/editstudent')
@login_required
def editstudent():
    id=request.args.get('id')
    session['studid']=id
    qry="SELECT * FROM `student` WHERE `login_id`=%s"
    res1=selectone(qry,str(id))
    q1="SELECT * FROM `course`"
    res=selectall(q1)
    print(res)
    return render_template("staff/edit_student.html",val2=selectall(q1),v=res1)


@app.route('/editstudent1',methods=['post'])
@login_required
def editstudent1():
    FirstName = request.form['textfield']
    LastName = request.form['textfield2']
    Gender = request.form['RadioGroup1']
    Dob = request.form['textfield3']
    Place = request.form['textfield4']
    Post = request.form['textfield5']
    Pin = request.form['textfield6']
    Phone = request.form['textfield7']
    Email = request.form['textfield8']
    crs = request.form['select']
    sem = request.form['select2']
    q="update `student` SET `first_name`=%s,`last_name`=%s,`gender`=%s,`dob`=%s,`place`=%s,`post`=%s,`pin`=%s,`course_id`=%s,`sem`=%s,`phone`=%s,`email`=%s WHERE `login_id`=%s"
    v=(FirstName,LastName,Gender,Dob,Place,Post,Pin,crs,sem,Phone,Email,session['studid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/managestudent"</script>'''



##################student##################



@app.route('/studenthome')
def studenthome():
    return render_template("studindex.html")




@app.route('/viewsubjects')
def viewsubjects():
    qry="SELECT `course_id` FROM `student` WHERE `login_id`=%s"
    res=selectone(qry,session['lid'])
    print(res)
    q="SELECT * FROM `subject` WHERE `course_id`=%s"
    cid=res['course_id']
    r=selectall2(q,cid)
    print(r)
    return render_template("student/view_subjects.html",val=r)
@app.route('/viewnotes')
def viewnotes():
    qry="select * from subject"
    v=selectall(qry)

    return render_template("student/view_notes.html",val=v)

@app.route('/searchnotes',methods=['post'])
def searchnotes():
    sid=request.form['select']
    qry = "select * from subject"
    v = selectall(qry)
    q = "SELECT * FROM `notes` WHERE `subject_id`=%s"
    res = selectall2(q, sid)
    return render_template("student/view_notes.html", val=v,val1=res)

@app.route('/viewqnpaper')
def viewqnpaper():
    qry="select * from subject"
    v=selectall(qry)

    return render_template("student/view_qpaper.html",val=v)



@app.route('/viewqnpapers',methods=['post'])
def viewqnpapers():
    sid = request.form['select']
    qry = "select * from subject"
    v = selectall(qry)
    q = "SELECT *FROM `questionpaper` WHERE `subjet_id`=%s"
    res = selectall2(q, sid)
    return render_template("student/view_qpaper.html",val1=res,val=v)


@app.route('/viewexamdetails')
def viewexamdetails():
    session['ml']=""
    q="SELECT `exam`.*,`subject`.`subject`,`timetable`.`timetable` FROM `exam` JOIN `subject` ON `subject`.`id`=`exam`.`subject_id` JOIN `timetable` ON `timetable`.`exam_id`=`exam`.`id`"
    res=selectall(q)
    return render_template("student/view_exam_details.html",val=res)


@app.route('/viewexamdetailss')
def viewexamdetailss():
    q="SELECT `exam`.*,`subject`.`subject` FROM `exam` JOIN `subject` ON `subject`.`id`=`exam`.`subject_id` "
    res=selectall(q)
    return render_template("staff/view_exam_detailss.html",val=res)

@app.route('/mngquestions')
def mngquestions():
    id=request.args.get('id')
    session['eid']=id

    q="SELECT * FROM  `questions` WHERE `eid`=%s"
    res=selectall2(q,id)
    return render_template("staff/manage_question.html",val=res)


# @app.route('/viewquestions',methods=['post'])
# def viewquestions():
#     sid=request.form['select']
#     q = "SELECT * FROM  `subject` WHERE `course_id`=%s"
#     res = selectall2(q, session['cidd'])
#     q="SELECT * FROM `questions` WHERE `subid`=%s"
#     re=selectall2(q,sid)
#     return render_template("staff/manage_question.html",val=res,v=re)

@app.route('/examsubjects',methods=['post'])
def examsubjects():
    id=request.args.get('id')
    q=""


    return render_template("student/exam_subjects.html")

@app.route('/addquestions')
def addquestions():

    return render_template("staff/add_questions.html")


@app.route('/addquestions1',methods=['post'])
def addquestions1():
    qstn=request.form['textfield']
    op1=request.form['textfield2']
    op2=request.form['textfield3']
    op3=request.form['textfield4']
    op4=request.form['textfield5']
    answr=request.form['textfield6']
    q="INSERT INTO `questions` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)"
    v=(session['eid'],qstn,op1,op2,op3,op4,answr)
    iud(q,v)
    return '''<script>alert("added");window.location="/staff_home"</script>'''



###########################test############################

def cam_check():
    # Initializing the wmi constructor
    facecount=0
    mal_count = 0
    # Printing the header for the later columns
    print("pid Process name")

    # Iterating through all the running processes
    chromelis = []
    msedgelist = []
    # for process in f.Win32_Process():
    #     # Displaying the P_ID and P_Name of the process
    #     # print(f"{# process.ProcessId:<10} {# process.Name}")
    #     if process.Name == 'chrome.exe':
    #         chromelis.append(process.Name)
    #
    #     if process.Name == 'msedge.exe':
    #         msedgelist.append(process.Name)
    #
    # print(len(chromelis))
    # print(len(msedgelist))
    #
    # chrome_count=len(chromelis)
    # msedge_count=len(msedgelist)


    labelsPath = os.path.sep.join(
        [r"E:\malpractice\src\static\yolo", "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")

    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                               dtype="uint8")

    weightsPath = os.path.sep.join(
        [r"E:\malpractice\src\static\yolo", "yolov3.weights"])
    configPath = os.path.sep.join(
        [r"E:\malpractice\src\static\yolo", "yolov3.cfg"])

    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    qry="select * from cam_status"
    res=selectall(qry)
    if len(res)==0:
        return "hhh"
    else:

        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        cap = cv2.VideoCapture(0)

        flag = 0
        count = 0
        text = ""
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        path = r"E:\malpractice\src\static/"



        while cap.isOpened():
         try:
            qry = "select * from cam_status"
            res = selectall(qry)
            if len(res)==0:
                break
            sid=res[-1]['sid']
            tid=res[-1]['tid']
            success, image = cap.read()

            cv2.imwrite("ro.jpg", image)
            img = cv2.imread("ro.jpg")
            import time



            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            (W, H) = (None, None)


            if W is None or H is None:
                (H, W) = img.shape[:2]
####################################################
            if len(faces)>0:
                if facecount==0:

                    q="SELECT * FROM `student` WHERE `login_id`=%s"
                    res=selectone(q,sid)
                    print(res,"sssssssssssssssssssssssssssss")
                    iii=res['photo']
                    print(iii,"ppppppppppppppppppppppppppp")
                    path=r"E:\malpractice\src\static\student/"+iii
                    enf("ro.jpg")
                    data = pickle.loads(open('faces.pickles', "rb").read())
                    # load the input image and convert it from BGR to RGB
                    image = cv2.imread(path)
                    # print(image)
                    h, w, ch = image.shape
                    print(ch)
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    print("[INFO] recognizing faces...")
                    boxes = face_recognition.face_locations(rgb,
                                                            model='hog')
                    encodings = face_recognition.face_encodings(rgb, boxes)
                    # loop over the facial embeddings
                    name = "na"
                    for encoding in encodings:
                        matches = face_recognition.compare_faces(data["encodings"],
                                                                 encoding, tolerance=0.6)


                        # check to see if we have found a match
                        if True in matches:
                            # find the indexes of all matched faces then initialize a
                            # dictionary to count the total number of times each face
                            # was matched
                            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                            counts = {}

                            # loop over the matched indexes and maintain a count for
                            # each recognized face face
                            for i in matchedIdxs:
                                name = data["names"][i]
                                counts[name] = counts.get(name, 0) + 1
                            print(counts, " rount ")
                            name = max(counts, key=counts.get)
                            print("result1111111", name)

                    if name != "na":
                        print("result1111111", name)





                    else:
                        print("result22222222222", name)
                        dt = time.strftime("%Y%m%d_%H%M%S")
                        cv2.imwrite( "static/malpractice\\" + dt + ".png", img)
                        ptth = dt + ".png"
                        qry = "INSERT INTO `malpractice` VALUES(NULL,CURDATE(),CURTIME(),%s,%s,%s,'unknown')"
                        val = (tid, sid, ptth)
                        iud(qry, val)
                        session['ml']="unknown"

                frame=img
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                             swapRB=True, crop=False)
                net.setInput(blob)

                layerOutputs = net.forward(ln)


                # initialize our lists of detected bounding boxes, confidences,
                # and class IDs, respectively
                boxes = []
                confidences = []
                classIDs = []

                # loop over each of the layer outputs
                for output in layerOutputs:
                    # loop over each of the detections
                    for detection in output:
                        # extract the class ID and confidence (i.e., probability)
                        # of the current object detection
                        scores = detection[5:]
                        classID = np.argmax(scores)
                        confidence = scores[classID]

                        # filter out weak predictions by ensuring the detected
                        # probability is greater than the minimum probability
                        if confidence > 0.4:
                            # scale the bounding box coordinates back relative to
                            # the size of the image, keeping in mind that YOLO
                            # actually returns the center (x, y)-coordinates of
                            # the bounding box followed by the boxes' width and
                            # height
                            box = detection[0:4] * np.array([W, H, W, H])
                            (centerX, centerY, width, height) = box.astype("int")

                            # use the center (x, y)-coordinates to derive the top
                            # and and left corner of the bounding box
                            x = int(centerX - (width / 2))
                            y = int(centerY - (height / 2))

                            # update our list of bounding box coordinates,
                            # confidences, and class IDs
                            boxes.append([x, y, int(width), int(height)])
                            confidences.append(float(confidence))
                            classIDs.append(classID)

                # apply non-maxima suppression to suppress weak, overlapping
                # bounding boxes
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4,
                                        0.5)

                # ensure at least one detection exists
                if len(idxs) > 0:
                    # loop over the indexes we are keeping
                    for i in idxs.flatten():
                        # extract the bounding box coordinates
                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])

                        # draw a bounding box rectangle and label on the frame
                        color = [int(c) for c in COLORS[classIDs[i]]]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                                   confidences[i])
                        print(LABELS[classIDs[i]],"++++=====______")
                        if LABELS[classIDs[i]]=='cell phone':
                            dt = time.strftime("%Y%m%d_%H%M%S")
                            cv2.imwrite("static/malpractice\\" + dt + ".png", img)
                            ptth = dt + ".png"
                            print("===============")
                            qry = "INSERT INTO `malpractice` VALUES(NULL,CURDATE(),CURTIME(),%s,%s,%s,'cell phone')"
                            val = (tid, sid, ptth)
                            iud(qry, val)
                            session['ml']="cell phone"
                        cv2.putText(frame, text, (x, y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


                facecount=facecount+1
                if facecount==10:
                    facecount=0
            for (xx, yy, w, h) in faces:

                cv2.rectangle(img, (xx, yy), (xx + w, yy + h), (255, 0, 0), 2)  # draw rectangle to main image

                image = img[int(yy - 10):int(yy + h + 10), int(xx - 10):int(xx + w + 10)]  # crop detected face

                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

                # To improve performance
                image.flags.writeable = False

                # Get the result
                results = face_mesh.process(image)

                # To improve performance
                image.flags.writeable = True

                # Convert the color space from RGB to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                img_h, img_w, img_c = image.shape
                face_3d = []
                face_2d = []

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        for idx, lm in enumerate(face_landmarks.landmark):
                            if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                                if idx == 1:
                                    nose_2d = (lm.x * img_w, lm.y * img_h)
                                    nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                                x, y = int(lm.x * img_w), int(lm.y * img_h)

                                # Get the 2D Coordinates
                                face_2d.append([x, y])

                                # Get the 3D Coordinates
                                face_3d.append([x, y, lm.z])

                                # Convert it to the NumPy array
                        face_2d = np.array(face_2d, dtype=np.float64)

                        # Convert it to the NumPy array
                        face_3d = np.array(face_3d, dtype=np.float64)

                        # The camera matrix
                        focal_length = 1 * img_w

                        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                               [0, focal_length, img_w / 2],
                                               [0, 0, 1]])

                        # The Distance Matrix
                        dist_matrix = np.zeros((4, 1), dtype=np.float64)

                        # Solve PnP
                        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                        # Get rotational matrix
                        rmat, jac = cv2.Rodrigues(rot_vec)

                        # Get angles
                        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                        # Get the y rotation degree
                        x = angles[0] * 360
                        y = angles[1] * 360
                        # print(y)
                        # See where the user's head tilting
                        if y < -10:
                            flag = 1
                            mal_count = mal_count + 1
                            text = "Looking Left"
                        elif y > 10:
                            flag = 1
                            mal_count = mal_count + 1
                            text = "Looking Right"
                        elif x < -10:
                            flag = 1
                            mal_count = mal_count + 1
                            text = "Looking Down"
                        else:
                            flag = 0
                            # mal_count = 0
                            text = "Forward"

                else:
                    text = "No Face"
                    cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if flag == 1:

                if mal_count == 20:
                    import time
                    dt = time.strftime("%Y%m%d_%H%M%S")
                    cv2.imwrite("static/malpractice\\" + dt + ".png", image)
                    pth = dt + ".png"
                    # insert_malpractice()
                    # requests.get("http://127.0.0.1:8000/insert_malpractice/"+ dt + ".png")
                    # db = Db()
                    # db.insert(
                    #     "insert into malpractice values(null,'1',curdate(),curtime(), '" + pth + "' )")
                    q = "insert into malpractice values(null,curdate(),curtime(),%s,%s,%s,%s)"
                    iud(q, (tid,sid,pth,text))
                    session['ml'] = text


                    print("+_+_+_+_+_+)+)+)+)+_+_+_+_+_)()_")
                    mal_count = 0
                    flag = 0
         except Exception as e:
             print(e,"++++++++++++++++++++++++++++++++++++++")
             print(e,"++++++++++++++++++++++++++++++++++++++")
             print(e,"++++++++++++++++++++++++++++++++++++++")
             print(e,"++++++++++++++++++++++++++++++++++++++")
             pass
        cap.release()

@app.route('/view_sample_question/<tid>', methods=['get', 'post'])
def view_sample_question(tid):
        if 'ml' not in session:
            session['ml'] =""
        if session['ml']!="":
            return '''<script>alert("Malpractice Detected!!!!Session Terminate");window.location="/studenthome#about"</script>'''

        print(tid,session['cnt'])
        cnt=session['cnt']
        session['cp']=tid
        # session['ct']=cid
        qqry="select * from malpractice where studid=%s and `date`=curdate() "
        ress=selectone(qqry,session['lid'])
        if ress is None:
            q=[]
            qr="SELECT * FROM `test_result`  WHERE `studid`=%s AND `eid`=%s"
            v=(session['lid'],session['cp'])
            r=selectone(qr,v)
            print(r)
            if r is None:
                res=selectall2("select * from `questions` where eid=%s",str(tid))
                for i in res:
                    q.append(i['qid'])
                qry="INSERT INTO `cam_status` VALUES(%s,%s)"
                val=(tid,session['lid'])
                iud(qry,val)
                start_new_thread(cam_check, ())
                res1 = selectone("select * from `questions` WHERE eid=%s and  qid=%s ",(str(tid),str(q[cnt])))

                return render_template('student/view_exam_question.html',data=res1, ln=len(res), cnt=int(cnt),cc="0")
            else:
                return '''<script>alert("Already attended");window.location="/viewexamdetails#about"</script>'''
        else:
            return '''<script>alert("Malpractice Detected!!!!Session Terminate");window.location="/studenthome#about"</script>'''


@app.route('/quit',methods=['post','get'])
def quit():
    session['cnt'] = 0
    qry = "update test_result set status ='completed' where studid=%s and eid=%s "
    res = iud(qry, (session['lid'], session['cp']))
    qry = "DELETE FROM `cam_status` WHERE `tid`=%s AND `sid`=%s"
    val = (session['cp'], session['lid'])
    iud(qry, val)
    return '''<script>alert("Succesfully Quited");window.location="/studenthome"</script>'''





@app.route('/finishexm/<q>',methods=['post'])
def finishexm(q):

        print("====================else")
        user_ans = request.form['RadioGroup']
        crct_ans = request.form['rans']

        btn = request.form['button']
        print(crct_ans,user_ans)


        if btn=="FINISH":
            print("finish")
            session['cnt']=0
            if user_ans == crct_ans:

                qry = "update test_result set mark=mark+1 ,status ='completed' where studid=%s and eid=%s "
                res = iud(qry,(session['lid'],session['cp']))
                qry = "DELETE FROM `cam_status` WHERE `tid`=%s AND `sid`=%s"
                val = (session['cp'], session['lid'])
                iud(qry,val)
                print("cccc",res)
                return '''<script>alert("succesfully attended");window.location="/studenthome"</script>'''
            else:
                qry = "update test_result set status ='completed' where studid=%s and eid=%s "
                res = iud(qry, (session['lid'], session['cp']))
                print("cccc", res)
                print("okk===============================")

                return '''<script>alert("succesfully attended");window.location="/studenthome"</script>'''

        else:

                    print("next====>>>>>")

                    session['cnt'] = session['cnt'] + 1
                    if user_ans == crct_ans:



                        qry = "update test_result set mark=mark+1,status='pending' where studid=%s and eid=%s"
                        res = iud(qry,(session['lid'],session['cp']))
                        return redirect(url_for('view_sample_question',tid=session['cp']) )


                    else:
                        print("kkk")
                        return redirect(url_for('view_sample_question', tid=session['cp']))






app.run(debug=True)








