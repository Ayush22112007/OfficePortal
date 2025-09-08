from django.contrib import admin
from django.urls import path
from Home import views
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_http_methods

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'), 
    path('', views.index, name='index'),
    path('login/hr/', views.hr_login_view, name='hr_login'),
    path('login/emp/', views.emp_login_view, name='emp_login'),
    path('emp/dashboard/', views.emp_dashboard, name='emp_dashboard'),
    path('hr/manage/', views.manage_employees, name='manage_employees'),
    path('emp/view/', views.view_employee_data, name='view_employee_data'),
    path('no-permission/', views.no_permission, name='no_permission'),
    path('not-authorized/', views.not_authorized_view, name='not_authorized'),
    path('register/', views.register, name='register'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('student/',views.student, name='student'),
    path('home/', views.retrieve, name='home'), 
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('help/', views.help_view, name='help'),
    path('logout/', require_http_methods(["GET", "POST"])(LogoutView.as_view(next_page='index')), name='logout'),
    path('add/', views.index, name='add'),
    path('create/', views.create, name='create'),
    path('edit/<int:id>/', views.edit_employee, name='edit'),
    path('delete/<int:id>/', views.delete_employee, name='delete'),
]