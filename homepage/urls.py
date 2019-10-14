from . import views
from django.urls import path

app_name = 'homepage'

urlpatterns = [
    # url/
    path('',views.index, name='home'),

    #url/home/
    path('home/', views.index, name='home'),

    # url/signin/
    path('signin/', views.login, name='signin'),

    # url/signin/authenticate/
    path('signin/authusr', views.authusr, name='authusr'),
]