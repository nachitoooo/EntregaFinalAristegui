from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.home, name='home'),
    path('registro', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog_list, name='blog_list'), 
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'), 
    path('about/', views.about, name='about'), 
    path('profile/', views.profile, name='profile'), 
    path('create_blog/', views.create_blog, name='create_blog'), 
    path('update_blog/<int:blog_id>/', views.update_blog, name='update_blog'),  
    path('album/', views.album_view, name='album'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)