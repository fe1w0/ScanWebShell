from django.shortcuts import render


def index(request):
    """
    根据session 放回不同的首页[已登录,未登录]
    :param request:
    :return:
    """
    if request.session.get('is_login'):
        is_login = True # 在模板层启用不同的 引导航
    return render(request, 'ScanWebShell/index.html', locals())
