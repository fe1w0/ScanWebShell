from __future__ import absolute_import, unicode_literals

import json
import os
import zipfile
import shutil
from celery import shared_task
from utils.scanFile import webshellScan
from celery import Task
from job.models import ScanTaskField
from django_celery_results.models import TaskResult


def unzip_function(zip_file_name, path="."):
    with zipfile.ZipFile(zip_file_name, "r") as zip_obj:
        zip_obj.extractall(path=path)


class processTask(Task):
    """
    更新数据库
    """
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        scan_task = ScanTaskField.objects.get(task_id=task_id)
        scan_task.task_result = TaskResult.objects.get(task_id=task_id)
        scan_task.task_status = TaskResult.objects.get(task_id=task_id).status
        scan_task.save()


@shared_task(base=processTask)
def scanTask(file_name):
    """
    创建扫描任务
    :param file_name:
    :return:
    """
    if file_name.endswith("zip"):
        unzip_path = file_name[:-4]
        os.mkdir(unzip_path)
        unzip_function(file_name, unzip_path)
        result_array = webshellScan(unzip_path)
        result_json = json.dumps(result_array)
        # 任务完成后,删除解压后的文件夹
        shutil.rmtree(unzip_path)  # 递归删除文件夹，即：删除非空文件夹
    if file_name.endswith("php"):
        result_array = webshellScan(file_name)
        result_json = json.dumps(result_array)
    return result_json
