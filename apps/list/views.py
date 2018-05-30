# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from datetime import date, datetime
from .models import User, WishList, Joint
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "list/index.html")

def register(request):
    errors = User.objects.register(request.POST)
    if errors:
        for tag,i in errors.iteritems():
            messages.error(request, i, extra_tags=tag)
        return redirect("/")
    else:
        pwHash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt().encode())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                   email=request.POST['email'], password=pwHash)
        messages.success(request, "Registered Successfully")
        return redirect("/")

def login(request):
    errors = User.objects.login(request.POST)
    if errors:
        for i in errors:
            print i
            messages.error(request, i)
        return redirect("/")
    else:
        request.session['user_id']=User.objects.get(email=request.POST['email']).id
        request.session['user_name'] = User.objects.get(email=request.POST['email']).first_name
        print request.session['user_name']
        return redirect('/to_wish_plans')

def logout(request):
    request.session.clear()
    return redirect('/')

def to_wish_plans(request):
    this_user = User.objects.get(id=request.session['user_id'])
    userwish = WishList.objects.filter(user=this_user)
    context = {
        'userwish': userwish,
        'others': WishList.objects.exclude(user=this_user)
    }
    return render(request, 'list/wishplans.html', context)

def to_add_wish_plan(request):
    return render(request, 'list/addwishplans.html')


def add_plan(request, id):
    if request.method == 'POST':
        messagesp = []
        if len(request.POST['item']) >= 3:
            this_user = User.objects.get(id=id)
            this_wish = WishList.objects.create(user=this_user, item=request.POST['item'])
            # print request.POST['item']
            Joint.jointManager.create(user=this_user, wishlist=this_wish)
            request.session['wish_id'] = this_wish.id
            return redirect('/to_dashboard')
        else:
            messagesp.append('The Item/Product field is required')
            for message in messagesp:
                messages.add_message(request, messages.ERROR, message)
            return redirect('/to_add_wish_plan')


def to_dashboard(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_wish = WishList.objects.get(id=request.session['wish_id'])
    joints = Joint.jointManager.all().filter(wishlist_id=this_wish.id)
    context = {
        'user': this_user.first_name,
        'this_wish': this_wish,
        'joints': joints
    }
    return render(request, 'list/dashboard.html', context)


def join(request, id, idt):
    this_user = User.objects.get(id=id)
    this_wish = WishList.objects.get(id=idt)
    this_wish.user = this_user
    this_wish.save()
    return redirect('/to_wish_plans')


def to_wish(request, idt, id):
    user = User.objects.get(id=id)
    wish = WishList.objects.get(id=idt)
    #?
    joints = Joint.jointManager.filter(wishlist_id=idt).all()
    print joints
    context = {
        'wish': wish,
        'user': user,
        'joints': joints
    }
    return render(request, 'list/wish.html', context)


def remove(request, id, idt):
    WishList.objects.get(id=idt).delete()
    return redirect('/to_wish_plans')

