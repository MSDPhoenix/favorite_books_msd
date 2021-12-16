from django.shortcuts import render,redirect,HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from datetime import datetime
import pytz

def mainpage(request):
    return render(request,"page_1.html")

def success(request):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            'user' : User.objects.get(id=user_id),
            'books' : Book.objects.all(),
        }
        return render(request,"page_2.html",context)
    else:
        return redirect('/')

def register(request):
    errors = User.objects.registerValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthday = request.POST['birthday']
        email = request.POST['email']
        password = request.POST['password']
        password_bcrypt = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name,last_name=last_name,birthday=birthday,email=email,password=password_bcrypt)
        request.session['user_id'] = user.id
        return redirect('/success')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)[0]
        request.session['user_id'] = user.id
        return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_favorite_book(request):
    user_id = request.session.get('user_id')
    if user_id:
        errors = User.objects.bookValidator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/success')
        else:        
            user = User.objects.get(id=user_id)
            title = request.POST['title']
            description = request.POST['description']
            book = Book.objects.create(title=title,description=description,added_by=user)
            book.save()
            book.favorited_by.add(user)
            return redirect('/view_book_information/'+str(book.id))
    else:
        return redirect('/')

def view_book_information(request,book_id):
    user_id = request.session.get('user_id')
    if user_id:
        book = Book.objects.get(id=book_id)
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
            'book' : book,
        }
        return render(request,'page_3.html',context)
    else:
        return redirect('/')

def edit_book_information(request,book_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        context = {
            'user' : user,
            'book' : book,
        }
        return render(request,'page_4.html',context)
    else:
        return redirect('/')

def update_book_information(request,book_id):
    user_id = request.session.get('user_id')
    if user_id:
        errors = User.objects.bookValidator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/edit_book_information/'+str(book_id))
        else:        
            book = Book.objects.get(id=book_id)
            book.title = request.POST['title']
            book.description = request.POST['description']
            book.save()
            return redirect('/view_book_information/'+str(book_id))
    else:
        return redirect('/')

def delete_book_information(request,book_id):
    user_id = request.session.get('user_id')
    if user_id:
        Book.objects.get(id=book_id).delete()
        return redirect('/success')
    else:
        return redirect('/')
        
def remove_book_from_favorites(request,book_id,page_number):
    user_id = request.session.get('user_id')
    if user_id:
        book = Book.objects.get(id=book_id)
        user = User.objects.get(id=user_id)
        book.favorited_by.remove(user)
        book.save()
        if page_number == 2:
            return redirect('/success')
        elif page_number == 3:
            return redirect('/view_book_information/'+str(book_id))
        elif page_number == 4:
            return redirect('/edit_book_information/'+str(book_id))
        elif page_number == 6:
            return redirect('/edit_user_information')
        else:
            return redirect('/')
    else:
        return redirect('/')

def add_book_to_favorites(request,book_id,page_number):
    user_id = request.session.get('user_id')
    if user_id:
        book = Book.objects.get(id=book_id)
        user = User.objects.get(id=user_id)
        book.favorited_by.add(user)
        book.save()
        if page_number == 2:
            return redirect('/success')
        elif page_number == 3:
            return redirect('/view_book_information/'+str(book_id))
        elif page_number == 4:
            return redirect('/edit_book_information/'+str(book_id))
        else:
            return redirect('/')
    else:
        return redirect('/')

def display_user_info(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
        }
        return render(request,'page_5.html',context)
    else:
        return redirect('/')

def edit_user_information(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'birthday' : str(user.birthday),
            'email' : user.email,        
        }
        return render(request,'page_6.html',context)
    else:
        return redirect('/')

def update_user_information(request):
    user_id = request.session.get('user_id')
    if user_id:
        errors = User.objects.updateUserValidator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/edit_user_information')
        else:  
            user = User.objects.get(id=user_id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.birthday = datetime.strptime(request.POST['birthday'],'%Y-%m-%d')
            user.email = request.POST['email']
            user.save()
            return redirect('/display_user_info')
    else:
        return redirect('/')

