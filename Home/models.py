from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig
from datetime import time


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    desc = models.TextField()
    date = models.DateTimeField()
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    dept = models.TextField()
    roll_no = models.IntegerField()
    
    def __str__(self):
        return self.name


class Details(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    address = models.TextField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    in_time = models.TimeField(default=time(9, 0), null=True, blank=True)
    out_time = models.TimeField(default=time(17, 0), null=True, blank=True)
    weekly_off = models.CharField(default="Saturday,Sunday", max_length=100, null=True, blank=True)


    
    def __str__(self):
        return self.name
    
class DetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        fields = ['name', 'email', 'age', 'address', 'city', 'state', 'pincode']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    login_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        login_password = cleaned_data.get("login_password")

        if not username or not login_password:
            raise forms.ValidationError("Both fields are required.")
        return cleaned_data
    
class Profile(models.Model):
    ROLE_CHOICES = (
        ('HR', 'Human Resources'),
        ('EMP', 'Employee'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='EMP')  
    instance.profile.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home'

def ready(self):
    import Home.signals

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name
