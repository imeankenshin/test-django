from django.urls import path
# blog ディレクトリの中の views.py を import
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail', views.detail, name='detail'),
]