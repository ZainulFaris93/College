from django.shortcuts import render, redirect
from .models import Course,Student,Teacher
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout


# Create your views here.
def index(request):
    return render(request,'index.html')

def login_page(request):
    return render(request,'login_page.html')

def login_function(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        pass_word = request.POST['password']
        user = auth.authenticate(username=user_name, password=pass_word)
        if user is not None:
            if user.is_authenticated: # Check if the user is authenticated
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    return redirect('admin_home')
                else:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    # messages.info(request, f'Welcome {user}')
                    return redirect('teacher_home')  # Redirect to teacher_home after login
            else:
                messages.info(request, 'User is not authenticated')
                return redirect('login_page')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_page')
    return render(request, 'login_page.html')

def logout_function(request):
    logout(request)
    if 'user' in request.session:
        del request.session['user']  # Clear user session variable
    return redirect('login_page')

def admin_home(request):
    if 'user' in request.session:
        return render(request, 'admin_home.html')
    else:
        return redirect('login_page')

def teacher_home(request):
    if 'user' in request.session:
        teacher = Teacher.objects.get(user=request.user)
        return render(request, 'teacher_home.html', {'teacher': teacher})
    else:
        return redirect('login_page')
    
def teacher_details(request):
    tchr = Teacher.objects.all()
    return render(request,'teacher_details.html', {'teacher': tchr})

def signup_page(request):
    c = Course.objects.all()
    return render(request,'signup_page.html', {'course':c})

def signup_function(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        age = request.POST['age']
        address = request.POST['address']
        phone = request.POST['phno']
        profile = request.FILES.get('profile')
        email = request.POST['mail']
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        c_id = request.POST['crs']
        c = Course.objects.get(id=c_id)

        if password == cpassword:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exists')
                return redirect('signup_page')
            # 1️⃣ Create User first
            user = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                username=uname,
                email=email,
                password=password
            )

            # 2️⃣ Create Teacher and link the User instance
            Teacher.objects.create(
                user=user,      
                age=age,
                address=address,
                phone=phone,
                image=profile,
                course=c
            )

            messages.success(request, "Account created successfully.")
            return redirect('signup_page')

        else:
            messages.info(request, 'Password not matching')
            return redirect('signup_page')

def teacher_card(request):
    tchr=Teacher.objects.get(user=request.user)
    return render(request,'teacher_card.html',{'tcr':tchr})
    
def teacher_update(request,id):
    tch=Teacher.objects.get(id=id)
    crcs=Course.objects.all()
    return render(request,'teacher_update.html',{'teacher':tch, 'course':crcs})

def teacher_update_function(request,id):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=id)
        user = teacher.user

        teacher.age = request.POST['age']
        teacher.address = request.POST['address']
        teacher.phone = request.POST['phno']
        profile = request.FILES.get('profile')
        if profile:
            teacher.image = profile
        course_id = request.POST['crs']
        teacher.course = Course.objects.get(id=course_id)
        teacher.save()

        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.username = request.POST['uname']
        user.email = request.POST['mail']
        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('teacher_card')

def delete_teacher(request, id):
    teacher=Teacher.objects.get(id=id)
    user = teacher.user
    teacher.delete()
    user.delete()  # Also delete the associated User instance
    return redirect('teacher_details')
def course(request):
    return render(request,'course.html')

def add_course(request):
    if request.method=='POST':
        cname=request.POST['course']
        fe=request.POST['fee']
        sp=Course(coursename=cname,fees=fe)
        sp.save()
        messages.success(request, "Course added successfully.")
        return redirect('course')
    
def student(request):
    c = Course.objects.all()
    return render(request,'student.html', {'course':c})

def add_std_details(request):
    if request.method=='POST':
        nam=request.POST['name']
        add=request.POST['address']
        ag=request.POST['age']
        dt=request.POST['date']
        dp=request.POST['c']
        cc=Course.objects.get(id=dp)
        std=Student(studentname=nam,address=add,age=ag,joiningdate=dt,course=cc)
        std.save()
        messages.success(request, "Student details added successfully.")
    return redirect('student')

def show_details(request):
    s = Student.objects.all()
    return render(request,'show_details.html', {'student':s})

def edit(request, id):
    student = Student.objects.get(id=id)
    courses = Course.objects.all()
    return render(request, 'edit.html', {'student': student, 'courses': courses})

def edit_details(request, id):
    if request.method == 'POST':
        student = Student.objects.get(id=id)
        student.studentname = request.POST['name']
        student.address = request.POST['address']
        student.age = request.POST['age']
        student.joiningdate = request.POST['date']
        course_id = request.POST['c']
        student.course = Course.objects.get(id=course_id)
        student.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('show_details')

def delete_student(request, id):
    student=Student.objects.get(id=id)
    student.delete()
    return redirect('show_details')