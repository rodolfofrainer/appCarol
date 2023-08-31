from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.baseView, name='home'),
    path('market', views.marketPageView, name='market_page'),
    path('createItem' , views.createItemPageView, name='create_item'),
    path('mywage', views.myWagePageView, name='mywage_page'),
    path('comparison', views.comparisonPageView, name='comparison_page'),
]