from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from django.conf import settings
import pytz


def send_forget_email(email, code):
    """
    发送 忘记密码确认邮件
    :param email:
    :param code:
    :return:
    """
    from django.core.mail import EmailMultiAlternatives

    subject = '来自site.com的忘记密码确认邮件'

    text_content = '''该邮件为忘记密码确认邮件！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>该链接<a href="http://{}/user/forget/confirm/?code={}" target=blank>为忘记密码确认链接</a>,</p>
                    <p>请点击站点链接确认从而重置密码！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email(email, code):
    """
    注册确认邮件
    :param email:
    :param code:
    :return:
    """
    from django.core.mail import EmailMultiAlternatives

    subject = '来自site.com的注册确认邮件'

    text_content = '''感谢注册site.com，这里是WebShell查杀平台！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/user/confirm/?code={}" target=blank>注册链接</a>，\
                    这里是WebShell查杀平台！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def make_confirm_string(user):
    """
    依据user,注册ConfirmString模型,并返回code
    :param user:
    :return:
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def hash_code(s, salt="mysite"):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    """
    首页
    :param request:
    :return:
    """
    if not request.session.get('is_login', None): # 未登录情况下
        return redirect('/user/login/')
    return redirect('/index/')


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.session.get('is_login', None):  # 根据 session 来检测是否登录
        return redirect('/index/') # 若已经登录,跳转到index 页面
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'user/login.html', locals())
            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'user/login.html', locals())

            if user.password == hash_code(password):
                '''
                注意此处session的存储,在整个处理过程中很重要
                '''
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'user/login.html', locals())

        else:
            return render(request, 'user/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'user/login.html', locals())


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'user/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'user/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'user/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'user/confirm.html', locals())
        else:
            return render(request, 'user/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'user/register.html', locals())


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    if not request.session.get('is_login', None): # 未登录,先转到 user/login
        return redirect("/user/login")
    request.session.flush() # 已登录,也要转到 user/login
    return redirect("/user/login/")


def user_confirm(request):
    """
    邮箱确认
    :param request:
    :return:
    """
    code = request.GET.get('code', None)
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message_warning = '无效的确认请求!'
        return render(request, 'user/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()  # 删除用户,可以影响到关联的User
        message_warning = '您的邮件已经过期！请重新注册!'
        return render(request, 'user/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message_success = '感谢确认，请使用账户登录！'
        return render(request, 'user/confirm.html', locals())


def forget_index(request):
    """
    忘记密码视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        forget_index_form = forms.ForgetIndexForm(request.POST)

        if forget_index_form.is_valid():
            email = forget_index_form.cleaned_data.get('email')
            # same_email_user = models.User.objects.filter(email=email)
            same_email_user = models.User.objects.get(email=email)
            if not same_email_user:
                message = "不存在使用该邮箱的用户！"
                return render(request, 'user/forget_index.html', locals())
            else:
                code = make_confirm_string(same_email_user)
                send_forget_email(email, code)
                message = '请前往邮箱进行确认！'
                return render(request, 'user/confirm.html', locals())
        else:
            message = "请检查填写的内容！"
            return render(request, 'user/forget_index.html', locals())
    forget_index_form = forms.ForgetIndexForm()
    return render(request, 'user/forget_index.html', locals())


def forget_confirm(request):
    """
    忘记密码邮箱确认
    :param request:
    :return:
    """
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'user/forget_confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.clear()
        confirm.delete()
        message = '您的邮件已经过期！请重新使用忘记密码功能!'
        return render(request, 'user/forget_confirm.html', locals())
    else:
        confirm.user.has_confirmed = False
        confirm.user.save()
        return redirect('/user/forget/change/?code=' + str(code))


def forget_change(request):
    """
    进行修改密码
    :param request:
    :return:
    """
    code = request.GET.get('code', None)
    if code:
        request.session['code'] = code
    if request.method == 'POST':
        forget_change_form = forms.ForgetChangeForm(request.POST)
        if forget_change_form.is_valid():
            password1 = forget_change_form.cleaned_data.get('password1')
            password2 = forget_change_form.cleaned_data.get('password2')
            code = forget_change_form.cleaned_data.get('code')
            try:
                confirm = models.ConfirmString.objects.get(code=code)
            except:
                message = '无效重置密码请求!'
                return render(request, 'user/forget_change.html', locals())
            message = '两次输入的密码不同！'
            if password1 != password2:
                return render(request, 'user/forget_change.html', locals())
            confirm.user.password = hash_code(password1)
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            message = '密码重置成功！'
            request.session.flush()
            return render(request, 'user/forget_change.html', locals())
        else:
            message = '请检查填写的内容！'
            return render(request, 'user/forget_change.html', locals())
    forget_change_form = forms.ForgetChangeForm()
    return render(request, 'user/forget_change.html', locals())
