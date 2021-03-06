from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from product.models import Category

from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from order.models import Order

from order.models import OrderProduct

from product.models import Comment


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'profile': profile,
    }
    return render(request,'user_profile.html',context)

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # Redirect to a success page.
            return  HttpResponseRedirect('/')
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
        else:
        # Return an 'invalid login' error message.
            messages.warning(request, 'Login error ! Username or Password is incorrect')
            return  HttpResponseRedirect('/user/login')
    category = Category.objects.all()
    context = {
                 'category':category,
              }
    return render(request,'login.html',context)

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user.id = current_user.id
            data.image = "images/users/DSC_0009.JPG"
            data.save()
            messages.success(request, "your account has been created successfully")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/user/signup')
    form = SignUpForm()

    category = Category.objects.all()
    context = {
                 'category':category,
                 'form':form,
              }
    return render(request, 'signup.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "your account has been updated successfully")
            return HttpResponseRedirect('/user/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        context = {
                'category': category,
                'user_form': user_form,
                'profile_form': profile_form,

            }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, "your password has been changed successfully")

            return HttpResponseRedirect('/user/user')
        else:
            messages.error(request, 'Please correct the error below!! <br>'+str(form.errors))
            return HttpResponseRedirect('/user/password')

    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return  render(request,'user_password.html',{'category':category , 'form':form})
@login_required(login_url='/login')
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'orders': orders,
    }
    return render(request, 'orders.html', context)
@login_required(login_url='/login')
def user_orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)

    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }

    return render(request, 'user_orderdetail.html', context)

@login_required(login_url='/login')
def user_orders_product(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'order_product': order_product,
    }
    return render(request, 'user_order_products.html', context)

@login_required(login_url='/login')
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id )

    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }

    return render(request, 'user_orderdetail.html', context)


def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id )

    context = {
        'category': category,
        'comments': comments,

    }

    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomments(request,id):
    current_user = request.user
    comments = Comment.objects.filter(id=id, user_id=current_user.id ).delete()
    messages.success(request, "comment deleted !")
    return HttpResponseRedirect('/user/comments')
