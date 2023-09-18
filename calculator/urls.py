from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.basePageView.as_view(), name='home'),
    path('createMarket/', views.MarketPageView.as_view(), name='market_page'),
    path('createMarket/<int:pk>/favorite/', views.MarketPageView.favorite_market, name='favorite_market'),
    path('createMarket/<int:pk>/unfavorite/', views.MarketPageView.unfavorite_market, name='unfavorite_market'),
    path('createItem/', views.CreateItemView.as_view(), name='create_item'),
    path('items/', views.ProductListView.displayAllItems , name='display_items'),
    path('items/<int:pk>', views.ProductListView.displayItem , name='display_single_item'),
    path('mywage/', views.myWagePageView.as_view(), name='mywage_page'),
    path('comparison/', views.comparisonPageView, name='comparison_page'),
]