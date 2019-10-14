from django.urls import path, include
from . import views

app_name = 'testapp'
urlpatterns = [
    path('', views.index, name='upload'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('chkimgs/', views.chkimgs, name='imgchker'),
]