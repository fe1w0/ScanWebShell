from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(
        # label="用户名",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autofocus': ''})
    )
    password = forms.CharField(
        # label="密码",
        max_length=256,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Password"
            }
        )
    )
    captcha = CaptchaField()


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        label="密码",
        max_length=256,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label="确认密码",
        max_length=256,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label="邮箱地址",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    captcha = CaptchaField(label="验证码")


class ForgetIndexForm(forms.Form):
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码")


class ForgetChangeForm(forms.Form):
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    code = forms.CharField(max_length=256)
    captcha = CaptchaField(label="验证码")
