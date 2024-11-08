from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('hod','HOD'),
        ('faculty','Faculty'),
        ('student','Student'),
    ]


    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,choices = ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email

class Course(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description =models.TextField()

class Batch(models.Model):
    name = models.CharField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

class Faculty(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    batches = models.ManyToManyField(Batch)

class Student(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description =models.TextField()
    

