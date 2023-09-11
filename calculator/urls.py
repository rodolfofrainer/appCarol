from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.baseView, name='home'),
    path('market', views.MarketPageView.as_view(), name='market_page'),
    path('createItem', views.CreateItemView.as_view(), name='create_item'),
    path('mywage', views.myWagePageView.as_view(), name='mywage_page'),
    path('comparison', views.comparisonPageView, name='comparison_page'),
]