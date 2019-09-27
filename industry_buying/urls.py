from django.urls import path
from industry_buying.views import HomeView, filter_industry_data

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', filter_industry_data, name='search'),
]