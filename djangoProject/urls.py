"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from djangoProject.app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('promo/', promo_list),
    path('promo/<int:pk>/', promo_by_id),
    path('promo/<int:pk>/participant/', promo_by_id_post_participant),
    path('promo/<int:pk>/participant/<int:participant_pk>/', promo_by_id_participant),
    path('promo/<int:pk>/prize/', promo_by_id_post_prize),
    path('promo/<int:pk>/participant/<int:prize_pk>/', promo_by_id_prize),
    path('promo/<int:pk>/raffle/', raffle),
]
