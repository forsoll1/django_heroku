"""projekti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from gallery import views

from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', accounts_views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    
    path('upload/', views.upload, name="upload"),
    path('gallery/<int:image_id>', views.show_image, name="show_image"),
    path('gallery/<int:image_id>/delete', views.delete, name="delete"), 
    
    path('', views.home, name="home"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
