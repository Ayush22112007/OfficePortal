from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from datetime import datetime
from .models import Contact, Student, Details, Employee
from .forms import DetailsForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from .decorators import restrict_emp_role, role_required, restrict_to_non_emp, hr_only
from functools import wraps

# Create your views here.

def about(request):
    return HttpResponse("Welcome to About!")        

def demo(request):
    context = {
        'name': 'abcd'
    }
    return render(request, 'demo.html',context)

def child(request):
    return render(request, 'child.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc,date=datetime.today())
        contact.save()

    return render(request, 'contact.html')

def student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dept = request.POST.get('dept')
        roll_no = request.POST.get('roll_no')
        student = Student(name=name, email=email, phone=phone, dept=dept,roll_no=roll_no)
        student.save()

    return render(request, 'student.html')

def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        details = Details(
            name=name,
            age=age,
            email=email,
            address=address,
            state=state,
            city=city,
            pincode=pincode
        )
        details.save()

        messages.success(request, "Employee saved successfully!")
        return redirect('home')

    return render(request, 'index.html')

@login_required
@hr_only
def retrieve(request):
    details = Details.objects.all()
    return render(request, 'retrieve.html', {'details': details})

@login_required
@hr_only
def edit_employee(request, id):
    employee = get_object_or_404(Details, id=id)
    if request.method == 'POST':
        form = DetailsForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully!")
            return redirect('home')
    else:
        form = DetailsForm(instance=employee)
    return render(request, 'edit.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    # Default role
    role = "Unknown"
    
    # Check user groups
    if user.groups.filter(name="HR").exists():
        role = "HR"
        template = "hr_profile.html"
    elif user.groups.filter(name="EMP").exists():  # make sure group is exactly "EMP"
        role = "Employee"
        template = "emp_profile.html"
    else:
        template = "emp_profile.html"  # fallback
    
    return render(request, template, {"user": user, "role": role})

@login_required
def settings_view(request):
    return render(request, 'settings.html')

@login_required
def help_view(request):
    return render(request, 'help.html')

def delete_employee(request, id):
   if not request.user.has_perm('some_permission'):
        return render(request, 'not_authorized.html')
   employee=Details.objects.get(id=id)
   employee.delete()
   return redirect('home')  

def create_employee(request):
    if not request.user.has_perm('some_permission'):
        return render(request, 'not_authorized.html')
    if request.method == 'POST':
        messages.success(request, 'Employee added successfully!')
        return redirect('create')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # logs in the user
                messages.success(request, f"Welcome {username}!")
                return redirect('home')  # redirect to the retrieve page
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

from django.contrib.auth.decorators import login_required

def hr_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'HR':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('not_authorized')  # or any page you want to redirect unauthorized users
    return wrapper


@login_required
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

@login_required
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def no_permission(request):
    return render(request, 'no_permission.html')

@hr_only
def manage_employees(request):
    if not request.user.has_perm('some_permission'):
        return render(request, 'not_authorized.html')
    pass

@role_required(allowed_roles=['EMP'])
def view_employee_data(request):
    pass

def hr_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.profile.role == 'HR':
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials or you are not HR.")
    return render(request, 'login_hr.html')

def emp_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # use 'username' not hardcoded
        password = request.POST.get('password')  # use 'password'
        user = authenticate(request, username=username, password=password)
        if user is not None and user.profile.role == 'EMP':
            login(request, user)
            return redirect('emp_dashboard')
        else:
            messages.error(request, "Invalid credentials or you are not an Employee.")
    return render(request, 'login_emp.html')

@login_required
def emp_dashboard(request):
    try:
        # Fetch employee details matching logged-in username (adjust field as needed)
        employee = Details.objects.get(name=request.user.username)
    except Details.DoesNotExist:
        employee = None

    context = {
        'employee': employee,
    }
    return render(request, 'emp_dashboard.html', context)

def not_authorized_view(request):
    return render(request, 'not_authorized.html')