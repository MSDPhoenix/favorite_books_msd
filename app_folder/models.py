from django.db import models
import re

from django.db.models.fields import BooleanField
import bcrypt
from datetime import datetime,timedelta

class UserManager(models.Manager):
    def registerValidator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must use valid email address"
        if User.objects.filter(email=postData['email']):
            errors['email_already_exists'] = "Email already exists" 
        if len(postData['first_name']) <2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if len(postData['password']) <8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Confirm password does not match password"
        if postData['birthday']:
            now = datetime.now()
            birthday = datetime.strptime(postData['birthday'],"%Y-%m-%d")
            minimum_age = timedelta(days=4848)
            if now - birthday < minimum_age and birthday < now:
                errors['birthday2'] = "Must be at least 13 years old"
            if birthday > now:
                errors['birthday1'] = "Birthday must be in the past"
        else:
            errors['birthday3'] = "Birthday is required"
        return errors

    def loginValidator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must use valid email address"
        if not user:
            errors['user'] = "User not found"
        else:
            user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                errors['confirm_password'] = "Password does not match"
        return errors

    def bookValidator(self,postData):
        errors = {}
        if not postData['title']:
            errors['title'] = "Title is required"
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters"
        return errors

    def updateUserValidator(self,postData):
        errors = {}
        if len(postData['first_name']) <2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must use valid email address"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    added_by = models.ForeignKey(User,related_name="books_added_by_user",on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User,related_name="favorite_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



        
    