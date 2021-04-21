from django.urls import path

from . import views

app_name = 'job'
urlpatterns = [
    path('upload/', views.upload_file),
    path('scan/', views.scan_file),
    path('search/',views.searchResult),
    path('count/',views.countResult)
]