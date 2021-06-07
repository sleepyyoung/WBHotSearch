from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    nickname = forms.CharField(
        required=True,
        label="请输入昵称:",
        max_length=11,
        error_messages={"invalid": "昵称最长只能输入11位！"}
    )
    username = forms.EmailField(
        required=True,
        label="请输入邮箱(用户名):",
    )
    first_password = forms.CharField(
        required=True,
        min_length=8,
        label="请输入密码:",
        widget=forms.PasswordInput(),
    )
    second_password = forms.CharField(
        required=True,
        # min_length=8,
        label="请确认密码:",
        widget=forms.PasswordInput(),
    )
    captcha = CaptchaField(
        label="请输入验证码结果:",
        required=True,
        error_messages={"invalid": "验证码输入有误,请重新输入"}
    )
    captcha_email = forms.CharField(
        label="请输入邮箱验证码:",
        required=True,
        error_messages={"invalid": "验证码错误"}
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LoginForm(forms.Form):
    user = forms.CharField(
        required=True,
        label="请输入账号(邮箱):",
        widget=forms.TextInput(attrs={'placeholder': '账号'}),
    )
    password = forms.CharField(
        required=True,
        label="请输入密码:",
        widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
    )
    captcha = CaptchaField(
        label="请输入验证码结果:",
        required=True,
        error_messages={"invalid": "验证码输入有误,请重新输入"}
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ForgotPasswordForm(forms.Form):
    username = forms.EmailField(
        required=True,
        label="用户名(邮箱):",
    )
    captcha_email = forms.CharField(
        label="请输入邮箱验证码:",
        required=True,
        error_messages={"invalid": "验证码错误"}
    )
    first_password = forms.CharField(
        required=True,
        min_length=8,
        label="请输入密码:",
        widget=forms.PasswordInput(),
    )
    second_password = forms.CharField(
        required=True,
        label="请确认密码:",
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
