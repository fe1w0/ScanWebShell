# Usage

邮箱功能需要在`settings.py`中配置如下参数:

```bash


```

![image-20210421180717445](http://img.xzaslxr.xyz/image-20210421180717445.png)

配置环境
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

在`settings.py`添加
```python
ALLOWED_HOSTS = ['*']
```

`celery`启动
```bash
celery -A ScanWebShell worker -l info
```

```bash
python manage.py runserver
```
