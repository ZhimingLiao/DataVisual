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

from django.urls import path

from . import views

app_name = 'infos'

urlpatterns = [
    path('', views.index, name='index'),
    path('count_data', views.count_data, name='count_data'),
    path('ranking_data', views.rank_data, name='rank_data'),
    path('regions_data', views.region_data, name='regions_data'),
    path('csrc_data', views.csrc_data, name='csrc_data'),
    path('month_data', views.month_data, name='month_data'),
]
