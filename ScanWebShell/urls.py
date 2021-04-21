from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.views.static import serve
from ScanWebShell import views
from django.conf import settings


urlpatterns = [
    path('', views.index), # 首页
    path('index/', views.index), # 首页
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('job/',include('job.urls')),
    path('captcha/', include('captcha.urls')),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}, name='static'),
]
