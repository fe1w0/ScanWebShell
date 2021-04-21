# 介绍
ScanWebShell 为基于机器学习的PHP-WebShell扫描工具,该版本为web服务形式。支持多用户独立使用和利用`celery`来配合扫描任务。

* `index`![image-20210421173150850](http://img.xzaslxr.xyz/image-20210421173150850.png)

* `job/count`![image-20210421180506546](http://img.xzaslxr.xyz/image-20210421180506546.png)


# Usage

邮箱(用于注册和重置密码功能)需要在`settings.py`中配置如下参数:

![image-20210421180717445](http://img.xzaslxr.xyz/image-20210421180717445.png)

* 下载
```bash
git clone https://github.com/fe1w0/ScanWebShell.git
cd ScanWebShell
```

* 配置环境
```bash
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
```

在`celery`中设置`worker`为`redis`,需要 
```bash
docker pull redis:latest
docker run --name=redis -d -p 6379:6379 redis
```

* `celery`启动
```bash
celery -A ScanWebShell worker -l info # 可以配合tmux或后台运行工具
```
* runserver
```bash
python3 manage.py runserver 0.0.0.0:8000
```
