# Generated by Django 3.2 on 2021-04-16 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
       # ('django_celery_results', '0009_auto_20210416_2010'), 该参数可能会有问题
    ]

    operations = [
        migrations.CreateModel(
            name='ScanTaskField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('scan_file_name', models.CharField(max_length=256, null=True)),
                ('task_id', models.CharField(max_length=256, null=True)),
                ('task_status', models.CharField(default='PENDING', max_length=256)),
                ('task_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('task_result', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_results.taskresult')),
            ],
            options={
                'verbose_name': '任务表单',
                'verbose_name_plural': '任务表单',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='ModelWithFileField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmp_file', models.FileField(upload_to='./FileUpload/')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('file_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'verbose_name': '文件',
                'verbose_name_plural': '文件',
                'ordering': ['-c_time'],
            },
        ),
    ]
