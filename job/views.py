from __future__ import absolute_import, unicode_literals
import json
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import ModelWithFileField, ScanTaskField
from user import models
from job.tasks import scanTask
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary[key][11:]


def upload_file(request):
    """
    上传文件
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/user/index/')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session.get('user_id')
            if user_id:
                tmp_user = models.User.objects.get(id=user_id)
                instance = ModelWithFileField(tmp_file=request.FILES['file'], file_user=tmp_user)
                instance.save()

                message = "上传成功!\n存储的文件名为:\n" + instance.tmp_file.name
                return render(request, 'job/upload.html', {'message_success': message})
            else:
                return render(request, 'job/upload.html', {'message_warning': "上传失败"})
    else:
        form = UploadFileForm()
    return render(request, 'job/upload.html', {'form': form})


def scan_file(request):
    """
    扫描文件,并将任务交给celery处理
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect('/user/index/')
    user_id = request.session.get('user_id')
    if user_id:
        tmp_user = models.User.objects.get(id=user_id)
    file_name = request.GET.get('file')

    def check(file_name):
        """
        检测是否已经存在相同的任务,有相同的返回True 反之 False
        :param file_name:
        :return:
        """
        try:
            model = ScanTaskField.objects.get(scan_file_name=file_name)
            return True
        except:
            return False

    if check(file_name):
        message = "已经有相同的扫描任务！"
        return render(request, 'job/scan.html', {'message_warning': '已经有相同的扫描任务！'})
    res = scanTask.delay(file_name=file_name)
    scantask = ScanTaskField(task_id=res.task_id, task_creator=tmp_user, scan_file_name=file_name)
    scantask.save()
    message_success = '''
    "Status":"successful","Task_id":{}
    '''.format(res.task_id)
    return render(request, 'job/scan.html', {'message_success': message_success})


def countResult(request):
    """
    统计该用户的上传文件信息和任务信息,并输出
    v1.2版 添加 按钮功能
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect('/user/index/')

    user_id = request.session.get('user_id')
    if user_id:
        current_user = models.User.objects.get(id=user_id)
    upload_file_all = current_user.modelwithfilefield_set.all()
    scan_task_all = current_user.scantaskfield_set.all()

    paginator_upload_file = Paginator(upload_file_all, 5)  # 5 个为一个表
    paginator_scan_task = Paginator(scan_task_all, 5)  # 5 个为一个表

    page_file = request.GET.get('page_file')
    page_task = request.GET.get('page_task')

    try:
        contacts_files = paginator_upload_file.page(
            page_file
        )
        contacts_tasks = paginator_scan_task.page(
            page_task
        )
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts_files = paginator_upload_file.page(1)
        contacts_tasks = paginator_scan_task.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts_files = paginator_upload_file.page(
            paginator_upload_file.num_pages
        )
        contacts_tasks = paginator_scan_task.page(
            paginator_scan_task.num_pages
        )
    try:
        page_file = int(page_file)
        page_task = int(page_task)
    except:
        page_file = 1
        page_task = 1
    return render(request, 'job/count.html', locals())


def searchResult(request):
    """
    根据task_id查看任务具体信息,同时有用户检验
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect('/user/index/')
    user_id = request.session.get('user_id')
    task_id = request.GET.get('task_id')
    scan_task = ScanTaskField.objects.get(task_id=task_id)
    print(scan_task.task_status)
    if scan_task.task_status != "SUCCESS":
        return render(request, 'job/search.html', {'message_warning': '未完成！'})
    if user_id == scan_task.task_creator.id:  # 此时放回 |文件名|任务创建时间|结果|
        try:
            scan_task_result = scan_task.task_result.result  # 结果类型为 array 经过 json序列化后的值
        except:
            return render(request, 'job/search.html', {'message_warning': '未完成！'})
    scan_task_result_array = json.loads(json.loads(scan_task_result))

    paginator_result = Paginator(scan_task_result_array, 15)
    page = request.GET.get('page')
    try:
        contacts_files = paginator_result.page(
            page
        )
    except PageNotAnInteger:
        contacts_files = paginator_result.page(
            1
        )
    except EmptyPage:
        contacts_files = paginator_result.page(
            paginator_result.num_pages
        )
    try:
        page = int(page)
    except:
        page = 1
    range_id = range(len(contacts_files.object_list))
    return render(request, 'job/search.html', locals())
