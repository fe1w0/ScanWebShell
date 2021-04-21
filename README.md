# 介绍
ScanWebShell 为基于机器学习的PHP-WebShell扫描工具,该版本为web服务形式。支持多用户独立使用和利用`celery`来配合扫描任务。

* `index`![image-20210421173150850](http://img.xzaslxr.xyz/image-20210421173150850.png)

* `job/count`![image-20210421180506546](http://img.xzaslxr.xyz/image-20210421180506546.png)


# Usage


* 下载
```bash
git clone https://github.com/fe1w0/ScanWebShell.git
cd ScanWebShell
```

* 配置环境
    *  `php vld` 插件安装
       http://pecl.php.net/package/vld
    安装后`php -m`来确定是否安装   
    * `settings.py`
```bash
cp ScanWebShell/settings.example.py  ScanWebShell/settings.py 
```
出于安全角度,`SECRET_KEY`参数强烈建议修改,修改方法如下:
```python
#进入Django shell
#python3 manage.py shell
#加载utils模块
from django.core.management import utils
#生成密钥
utils.get_random_secret_key()
```
邮箱(用于注册和重置密码功能)还需要在`settings.py`中配置如下参数:

![image-20210421180717445](http://img.xzaslxr.xyz/image-20210421180717445.png)


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
