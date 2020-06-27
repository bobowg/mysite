from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名或邮箱',
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名或邮箱'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'})
    )

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password =self.cleaned_data['password']
        user = authenticate( username = username_or_email, password=password)
        if  user is None:
            if User.objects.filter(email = username_or_email).exists():
                username = User.objects.get(email = username_or_email).username
                user = authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码出错')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegisterForm(forms.Form):
    username =  forms.CharField(
        label='用户名',
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入３至３０位的用户'})
    )
    email = forms.EmailField(
        label='电子邮件',
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入电子邮件'})
    )
    verification_code = forms.CharField(
        label='验证码',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '请输入验证码"查收邮件！"'})
    )
    password = forms.CharField(
        label='密码',min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'})
    )
    ewpassword = forms.CharField(
        label='请再次输入密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入密码'})
    )
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('send_for', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code == verification_code and code != ''):
            raise forms.ValidationError('验证码不正确，请查看邮件！')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用已经存在！')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise  forms.ValidationError('电子邮件已经存在！')
        return email
    def clean_password_again(self):
        password = self.cleaned_data['password']
        ewpassword = self.cleaned_data['ewpassword']
        if password != ewpassword:
            raise forms.ValidationError('两次输入的密码不一致！！')
        return password
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == '':
            raise forms.ValidationError("验证码不能为空！")
        return verification_code

class ChangeNickNameForm(forms.Form):
    new_nickname = forms.CharField(
        label= '新昵称',
        max_length= 20,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入昵称'})
    )
    def clean_new_nickname(self):
        new_nickname = self.cleaned_data.get('new_nickname', '').strip()
        if new_nickname == '':
            raise forms.ValidationError('新的昵称不能为空')
        return new_nickname
    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNickNameForm,self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户没有登陆！')
        return self.cleaned_data

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='电子邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入电子邮箱'})
    )
    verification_code = forms.CharField(
        label='验证码',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '请输入验证码"查收邮件！"'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登陆
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户没有登陆！')
        #判断用户是否绑定
        if self.request.user.email !="":
            raise forms.ValidationError('用户已经绑定邮箱！')
        #判断验证码
        code = self.request.session.get('bind_email_code','')
        verification_code = self.cleaned_data.get('verification_code','')
        if not ( code == verification_code and code != ''):
            raise forms.ValidationError('验证码不正确，请查看邮件！')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("改邮箱已经存在！")
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == '':
            raise forms.ValidationError("验证码不能为空！")
        return verification_code

class ChangePassWordForm(forms.Form):
    old_password = forms.CharField(
        label='旧密码',min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入原密码'})
    )
    new_password = forms.CharField(
        label='新密码',min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'})
    )
    new_password_again = forms.CharField(
        label='再次密码',min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePassWordForm, self).__init__(*args, **kwargs)

    def clean(self):
        #验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password','')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError("两次输入密码不一致！")
        return self.cleaned_data

    def clean_old_password(self):
        #验证旧密码
        old_password = self.cleaned_data.get('old_password','')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码不对，请重新输入')
        return old_password

class ForgotPassWordForm(forms.Form):
    email = forms.EmailField(
        label='电子邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入绑定过的电子邮箱'})
    )
    verification_code = forms.CharField(
        label='验证码',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入验证码"查收邮件！"'})
    )
    new_password = forms.CharField(
        label='新密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPassWordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('些邮箱没有绑定过!')
        return email
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("验证码不能为空！")
            # 判断验证码
            code = self.request.session.get('forget_password_code', '')
            verification_code = self.cleaned_data.get('verification_code', '')
            if not (code == verification_code and code != ''):
                raise forms.ValidationError('验证码不正确，请查看邮件！')
        return verification_code







