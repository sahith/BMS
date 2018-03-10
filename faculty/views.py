import bluetooth
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Register,Attendance_sheet
from .forms import RegisterForm
from datetime import date
from student.models import RegisterStudent,StudentCourses
from django.core.urlresolvers import reverse
import math

# Create your views here.


def home(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register = Register(username=request.POST['username'],
                                email=request.POST['email'],
                                factid=None,
                                course=request.POST['course'],
                                password=request.POST['password'],
                                approval=False
                                )
            register.save()
            return redirect('faculty:success')
        else:
            error = 'Please correct the errors below.'
            return render(request, 'faculty/register_form.html', {
                'error': error,
                'register_form': register_form})
    else:
        # First time the form is displayed to student
        register_form = RegisterForm()
        return render(request, 'faculty/register_form.html', {
            'register_form': register_form
        })




def regs(request):
    return render(request,'faculty/regsuccess.html')

def flogin(request):
    if request.method == "POST":
        Email = request.POST['email']
        password = request.POST['password']
        registers = Register.objects.filter(email=Email, password=password)
        if registers.count() == 1:
            for register in registers:
                request.session['id'] = register.pk
            r = Register.objects.filter(email=Email, password=password,approval=True)
            if r.count() == 1:
                return redirect('faculty:fachome')
            else:
                return render(request, 'faculty/login.html',{'error':'Not Approved Yet'})
        else:
            return render(request, 'faculty/login.html', {'error': 'Wrong Credentials'})
    else:
        return render(request, 'faculty/login.html')


def fachome(request):
    if 'id' in request.session:
        register = Register.objects.get(pk=request.session['id'])
        s = RegisterStudent.objects.filter(approval=True)
        return render(request, 'faculty/facultyhome.html', {'register': register,'s':s})
    else:
        return redirect('faculty:flogin')

def fac_logout(request):
    del request.session['id']
    return redirect('faculty:flogin')


def attendance(request):
    if 'id' in request.session:
        faculty = Register.objects.get(pk=request.session['id'])
        nearby_devices = bluetooth.discover_devices()
        students = StudentCourses.objects.filter(course=faculty.course,studentid__approval=True)
        s1 = Attendance_sheet.objects.filter(course=faculty.course,date=date.today())
        if s1.count()==0:
            faculty.count=faculty.count+1
            faculty.save()
        for i in students:
            for j in nearby_devices:
                if i.studentid.bluetooth_addr==j:
                    s1 = Attendance_sheet.objects.filter(factid=faculty.factid,course=i.course,date=date.today(),sid=i.studentid.studid)
                    if s1.count()==0:
                        s = Attendance_sheet(factid=faculty.factid, course=i.course, date=date.today(),sid=i.studentid.studid)
                        s.save()
        return render(request, 'faculty/attendance.html',{'nearby_devices':nearby_devices,'faculty':faculty,'students':students})
    else:
        return redirect('faculty:flogin')

def viewsheet(request):
    if 'id' in request.session:
        faculty = Register.objects.get(pk=request.session['id'])
        if request.method == 'POST':
            d = request.POST.get('date')
            sheet = Attendance_sheet.objects.filter(course=faculty.course,date=d)
            students =RegisterStudent.objects.filter(approval=True)
            if sheet.count()>0:
                return render(request, 'faculty/viewsheet.html',{'sheet':sheet,'students':students})
            else:
                return render(request,'faculty/viewsheet.html',{'messages':'No records present'})
        else:
            return render(request, 'faculty/sheet.html')
    else:
        return redirect('faculty:flogin')

def sheet(request):
    if 'id' in request.session:
        return render(request, 'faculty/sheet.html')
    else:
        return redirect('faculty:flogin')


def editsheet(request):
    if 'id' in request.session:
        faculty = Register.objects.get(pk=request.session['id'])
        faculty = Register.objects.get(pk=request.session['id'])
        all_students = StudentCourses.objects.filter(course=faculty.course, studentid__approval=True)
        students = Attendance_sheet.objects.filter(course=faculty.course, date=date.today())
        dict = {}
        pdict = {}
        f = 0
        for i in all_students:
            f = 0
            for j in students:
                if i.studentid.studid == j.sid:
                    f = 1
            if f == 1:
                pdict[i.studentid.studid] = i.studentid.username
            else:
                dict[i.studentid.studid] = i.studentid.username
        return render(request, 'faculty/editsheet.html', {'dict': dict, 'pdict': pdict})
    else:
        return redirect('faculty:flogin')

def view(request):
    if 'id' in request.session:
        faculty = Register.objects.get(pk=request.session['id'])
        s = Attendance_sheet.objects.filter(course=faculty.course, date=date.today(), factid=faculty.factid)
        s.delete()
        print('faculty course:'+faculty.course)
        students = request.POST.getlist('sid')
        for j in students:
            s1 = Attendance_sheet(factid=faculty.factid, course=faculty.course, sid=j)
            s1.save()
        return render(request,'faculty/edited.html')
    else:
        return redirect('faculty:flogin')


def fullsheet(request):
    if 'id' in request.session:
        faculty = Register.objects.get(pk=request.session['id'])
        s = Attendance_sheet.objects.filter(course=faculty.course, factid=faculty.factid)
        s1 = StudentCourses.objects.filter(studentid__approval=True, course=faculty.course)
        dict  = {}
        for i in s1:
            k = Attendance_sheet.objects.filter(course=faculty.course, factid=faculty.factid, sid=i.studentid.studid)
            if faculty.count > 0:
                dict[i.studentid.studid] = math.ceil((k.count() / faculty.count) * 100)
            else:
                dict[i.studentid.studid] = 0
            print(i.studentid.studid)
            print(dict[i.studentid.studid])
        if s.count() == 0:
            return render(request, 'faculty/fullsheet.html', {'dict': dict, 'faculty': faculty, 's1': s1, 'messages': 'No records present'})
        else:
            return render(request, 'faculty/fullsheet.html',{'dict': dict, 'faculty': faculty, 's1': s1})
    else:
        return redirect('faculty:flogin')










