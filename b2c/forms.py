from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from user.models import User


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',  'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password:
            raise ValidationError('用户名或密码不能为空')
        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError('用户不存在')
        exist_password = check_password(password, user.password)
        if not exist_password:
            raise ValidationError('密码错误')
        return self.cleaned_data

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     exist_user = User.objects.filter(username=username).first()
    #     if not exist_user:
    #         raise ValidationError('用户不存在')
    #     return username
    #
    # def clean_password(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = User.objects.filter(username=username).first()
    #     if not user:
    #         raise ValidationError('用户不存在')
    #     exist_password = check_password(password, user.password)
    #     if not exist_password:
    #         raise ValidationError('密码错误')
    #     return password
