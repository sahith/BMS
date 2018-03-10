from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from faculty.models import Register
from student.models import StudentCourses,RegisterStudent
from django.core.urlresolvers import reverse



# Create your views here.



def home(request):
        #after login to admin
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('adminstrator:adminhome')
                else:
                    return render(request, 'adminstrator/login.html', {'error': 'Your account has been disabled'})
            else:
                return render(request, 'adminstrator/login.html', {'error': 'Invalid login'})
        #before login
        return render(request, 'adminstrator/login.html')

def adminhome(request):
    if not request.user.is_authenticated():
        return redirect('adminstrator:home')
    else:
        registers = Register.objects.filter(approval=False)
        students = RegisterStudent.objects.filter(approval=False)
        courses = StudentCourses.objects.filter(studentid__approval=False)
        return render(request, 'adminstrator/adminhome.html',{'registers': registers,'students':students,'courses':courses})

def logoutadmin(request):
    #logging out
    logout(request)
    return redirect('adminstrator:home')

def fapproval(request):
    course = request.POST['course']
    id = request.POST['fid']
    status = request.POST['status']
    if status == 'approve':
        if id != '-1':
            regs = Register.objects.filter(factid=id)
            if regs.count() == 1:
                registers = Register.objects.filter(approval=False)
                students = RegisterStudent.objects.filter(approval=False)
                courses = StudentCourses.objects.filter(studentid__approval=False)
                return render(request,'adminstrator/adminhome.html',{'error' : 'Faculty id was already taken'
                    ,'registers': registers,'students':students,'courses':courses})
            elif regs.count() == 0:
                reg = get_object_or_404(Register,course=course)
                reg.approval = True
                reg.factid = id
                reg.save()
                freg = Register.objects.get(course=course)
                return render(request , 'adminstrator/fapproved.html' , {'freg': freg})
        else:
            registers = Register.objects.filter(approval=False)
            students = RegisterStudent.objects.filter(approval=False)
            courses = StudentCourses.objects.filter(studentid__approval=False)
            return render(request, 'adminstrator/adminhome.html',
                          {'error': 'Faculty id was Not given', 'registers': registers,'students':students,'courses':courses})
    else:
        dreg = Register.objects.get(course=course)
        dreg.delete()
        registers = Register.objects.filter(approval=False)
        students = RegisterStudent.objects.filter(approval=False)
        courses = StudentCourses.objects.filter(studentid__approval=False)
        return render(request,'adminstrator/adminhome.html',{'registers':registers,'students':students,'courses':courses})



def sapproval(request):
    sid = request.POST['sid']
    status = request.POST['status']
    if status == 'approve':
        s = get_object_or_404(RegisterStudent,studid=sid)
        s.approval=True
        s.save()
        registers = Register.objects.filter(approval=False)
        students = RegisterStudent.objects.filter(approval=False)
        courses = StudentCourses.objects.filter(studentid__approval=False)
        return render(request,'adminstrator/adminhome.html',{'registers':registers,
                                                             'students':students,'courses':courses,'error_messages':'Approved'})
    else:
        sreg = RegisterStudent.objects.get(studid=sid)
        sreg.delete()
        registers = Register.objects.filter(approval=False)
        students = RegisterStudent.objects.filter(approval=False)
        courses = StudentCourses.objects.filter(studentid__approval=False)
        return render(request,'adminstrator/adminhome.html',{'registers':registers,'students':students,'courses':courses})

















