# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import user, review, book
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'loginregapp/index.html')
def register(request):
    if request.method == 'POST':
        errors =  user.objects.validation(request.POST)
        if len(errors):
            for register,error in errors.iteritems():
                messages.error(request, error, extra_tags=register)
            return redirect('/')
        else:
            bcryptpassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=bcryptpassword)
            currentuser=user.objects.get(email=request.POST['email'])
            request.session['currentuser']=currentuser
            return redirect('/books')
    else:
        return redirect('/')
def login(request):
    loginerrors = user.objects.loginvalidation(request.POST)
    if len(loginerrors):
        for login, error in loginerrors.iteritems():
            messages.error(request,error,extra_tags=login)
            return redirect('/')
    else:
        currentuser=user.objects.get(email=request.POST['email'])
        request.session['currentuser']=currentuser
        return redirect('/books')
def books(request):
    if "currentuser"  in request.session:
        info={
            "user": request.session['currentuser'],
            "booklist":book.objects.all(),
            "recentreview": review.objects.raw("SELECT * FROM loginregapp_review JOIN loginregapp_book ON loginregapp_review.book_id=loginregapp_book.id ORDER BY loginregapp_review.created_at DESC LIMIT 3")
        }
        return render(request, 'loginregapp/books.html',info)
    else:
        return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')
def addpage(request):
    return render(request, "loginregapp/add.html")
def showbook(request,id):
    bookinfo={
        "user": request.session['currentuser'],
        "book":book.objects.get(id=id),
        "bookreview":review.objects.raw("SELECT * FROM loginregapp_review JOIN loginregapp_book ON loginregapp_review.book_id = loginregapp_book.id JOIN loginregapp_user ON loginregapp_book.uploader_id=loginregapp_user.id WHERE loginregapp_book.id= %s",[id])
    }
    return render(request, "loginregapp/show.html",bookinfo)
def profile(request,id):
    showuser = user.objects.get(id=id)
    reviewed_booklist = book.objects.raw(
        "SELECT * FROM loginregapp_book JOIN loginregapp_review ON loginregapp_review.book_id=loginregapp_book.id JOIN loginregapp_user ON loginregapp_user.id = loginregapp_review.user_id WHERE user_id = %s", [id])
    userinfo={
        "userinfo": showuser,
        "count":review.objects.filter(user_id=id).count(),
        "reviewed_booklist":reviewed_booklist
    }
    return render(request, "loginregapp/profile.html",userinfo)
def addbookprocess(request):
    book.objects.create(title=request.POST['title'],author=request.POST['author'],uploader=request.session['currentuser'])
    review.objects.create(review=request.POST['review'],rating=request.POST['rating'],user=request.session['currentuser'],book=book.objects.get(title=request.POST['title']))
    bookid = book.objects.get(title=request.POST['title']).id
    return redirect('/books/%s' %bookid)
def addreviewprocess(request,id):
    review.objects.create(review=request.POST['review'], rating=request.POST['rating'],user=request.session['currentuser'], book=book.objects.get(id=id))
    return redirect('/books/'+id)
def deletereview(request,id):
    bookid = review.objects.get(id=id).book_id
    reviewdel = review.objects.get(id = id)
    reviewdel.delete()
    return redirect('/books/%s' %bookid)

    
        


    

               
               
               


