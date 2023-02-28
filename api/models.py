from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'F'
    
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    identity_number = models.CharField(null=True, blank=True, max_length=11)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    address = models.TextField()
    
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'birth_date', 'address', 'password']

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class Video(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} | {self.url}"

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    
    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} | {self.user.first_name} {self.user.last_name}'

class VisitRequest(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitor', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visited')
    datetime = models.DateTimeField(default=datetime.now())
    location = models.TextField()
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} | {self.datetime}'