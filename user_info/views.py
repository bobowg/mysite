import string,random,time
from django.contrib.auth import authenticate,login as dj_login , logout as dj_logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from blog.dj_from import LoginForm,RegisterForm,ChangeNickNameForm,BindEmailForm,ChangePassWordForm,ForgotPassWordForm
from .models import Profile
def login(request):
    if request.method == "POST":
        login_from = LoginForm(request.POST)
        if login_from.is_valid():
            user = login_from.cleaned_data['user']
            dj_login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_from = LoginForm()
    context = {}
    context['login_from'] = login_from
    return render(request, 'userlogin.html', context)

def logout(request):
    dj_logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def register(request):
    if request.method == "POST":
        register_from = RegisterForm(request.POST,request=request)
        if register_from.is_valid():
            username = register_from.cleaned_data['username']
            email = register_from.cleaned_data['email']
            ewpassword = register_from.cleaned_data['ewpassword']
            user = User.objects.create_user(username,email,ewpassword)
            user.save()
            #clear session
            request.session.clear()
            user = authenticate(username= username,password = ewpassword)
            dj_login(request,user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_from = RegisterForm()
    context = {}
    context['register_from'] = register_from
    return render(request, 'register.html', context)

def login_for_medal(request):
    login_from = LoginForm(request.POST)
    data = {}
    if login_from.is_valid():
        user = login_from.cleaned_data['user']
        dj_login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def Change_nickname(request):
    if request.method == 'POST':
        login_from = ChangeNickNameForm(request.POST,user=request.user)
        if login_from.is_valid():
            new_nickname = login_from.cleaned_data['new_nickname']
            profile ,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangeNickNameForm()
    context={}
    context['form'] = form
    return render(request,'Chanage_Nickname.html',context)

def Change_Password(request):
    if request.method == 'POST':
        form = ChangePassWordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            new_password_again = form.cleaned_data['new_password_again']
            user.set_password(new_password)
            user.save()
            dj_logout(request)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangePassWordForm()
    context = {}
    context['form'] = form
    return render(request, 'Chanage_password.html', context)

def userInfo(request):
    context = {}
    return render(request,'user_info.html',context)

def BindEmail(request):
    if request.method == 'POST':
        login_from = BindEmailForm(request.POST, request = request)
        if login_from.is_valid():
            email = login_from.cleaned_data['email']
            request.user.email = email
            request.user.save()
            request.session.clear()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_from = BindEmailForm()
    context = {}
    context['form'] = login_from
    return render(request,'is_verti.html',context)
def FotgotPassword(request):
    if request.method == 'POST':
        form = ForgotPassWordForm(request.POST, request = request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            request.session.clear()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ForgotPassWordForm()
    context = {}
    context['form'] = form
    return render(request, 'Fotgotpassword.html', context)

def send_verification_code(request):
    email = request.GET.get('email','')
    send_for = request.GET.get('send_for','')
    data ={}
    if email != '':
        #生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)
        if now - send_code_time <30:
            data['status'] = 'ERROR'
        else:
            request.session['send_for'] = code
            request.session['send_code_time'] = now
            send_mail(
                '查收验证码',
                '验证码: %s' % code,
                'bobowg@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

