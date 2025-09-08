from django.shortcuts import redirect
from functools import wraps
from django.shortcuts import render
from .models import Employee

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return render(request, 'not_authorized.html')
        return _wrapped_view
    return decorator

# Usage:
@role_required(['EMP'])
def emp_dashboard(request):
    employees = Employee.objects.all()
    return render(request, 'emp_dashboard.html', {'employees': employees})

def restrict_emp_role(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user is authenticated and has profile with role
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.role == 'EMP':
                # Redirect to not authorized page
                return render(request, 'not_authorized.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def restrict_to_non_emp(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'role', '') == 'emp':
            return render(request, 'not_authorized.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def hr_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        role = getattr(getattr(request.user, 'profile', None), 'role', None)
        if role and role.strip().upper() == 'HR':
            return view_func(request, *args, **kwargs)
        return render(request, 'not_authorized.html')
    return _wrapped_view