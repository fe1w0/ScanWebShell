from django_celery_results.models import TaskResult
from user.models import User
import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings


class ModelWithFileField(models.Model):
    tmp_file = models.FileField(upload_to = './FileUpload/')
    file_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    '''
    值得注意的一点是,FileUpload中已经存在相同文件名的文件时,会对上传文件的文件名重命名 
    如 1.png 转为 1_fIZVhN3.png
    且存储的文件为 1_fIZVhN3.png
    '''
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tmp_file.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "文件"
        verbose_name_plural = "文件"


# 添加装饰器
@receiver(post_delete, sender=ModelWithFileField)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'tmp_file')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT, str(files))
    if os.path.isfile(fname):
        os.remove(fname)


class ScanTaskField(models.Model):
    # 创建时间
    c_time = models.DateTimeField(auto_now_add=True)
    # ScanFileName
    scan_file_name = models.CharField(max_length=256, null=True)
    # task_id task_status 虽然增加了整个系统的复杂度,但目前没有找到好一点的方法。
    # AsyncResult 中 得到的 task_id
    task_id = models.CharField(max_length=256, null=True)
    # task_status,可以通过AsyncResult(task_id).status 查询
    task_status = models.CharField(max_length=256, default="PENDING")
    # celery 中的 taskResult,等任务执行后添加进去
    task_result = models.OneToOneField(
        TaskResult,
        on_delete=models.CASCADE,
        null=True
    )
    # ScanTask 与 User 进行多对一绑定
    task_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.scan_file_name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "任务表单"
        verbose_name_plural = "任务表单"