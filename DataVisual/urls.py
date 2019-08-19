"""DataVisual URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.staticfiles.views import serve as static_serve
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView


def return_static(request, path, insecure=True, **kwargs):
    return static_serve(request, path, insecure, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="infos/index"), name='main'),
    path('infos/', include('infos.urls', namespace='infos')),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    # re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = 'infos.views.page_not_found'
handler500 = 'infos.views.page_error'
