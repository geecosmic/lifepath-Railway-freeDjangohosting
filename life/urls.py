# api/urls.py reduce_digit_view,index,
from django.urls import path
from .views import path_numbers,destiny_number_view,privacy_page
from . import views

urlpatterns = [
  
    path('path_numbers/', path_numbers, name='path_numbers'),
    # path('list',index2 , name='list'),


    # path('jewishbirthday/', views.all_period, name='all_period'),
    path('jewishbirthday/', views.all_period, name='jewishbirthday'),

    path('donate/', views.donate, name='donate'),

    


    path('', views.tikkun, name='tikkun'),
    path('privacy/', views.privacy_page, name='privacy-page'),

    # path('period/<int:id>/', views.detail_page, name='detail_page'),

    
    # path('main_page', views.main_page, name='main_page'),
    # path('get_period/', views.get_period_view, name='get_period'),
    path('get_period/', views.get_period_view, name='get_period'),

    path('get-period/', views.get_period, name='get_period'),
    path('main_page', views.main_page, name='main_page'),  # Default view without a selected period
    # path('<int:id>/', views.main_page, name='main_page_with_detail'),  
    path('<str:type>/<int:id>/', views.main_page, name='main_page_with_detail'),  


    # path('period/<int:id>/', views.detail_page, name='detail_page'), 



    # path('<int:id>/', views.main_page, name='main_page'),


    # path('yearly_cycle_view/', views.yearly_cycle_view, name='yearly_cycle2'),

    # path('hebrew_date_view/', views.hebrew_date_view, name='hebrew_date'),
    # path('display_period/', views.display_period, name='dispaly_period'),
    path('destiny-number/', destiny_number_view, name='destiny_number'),

    # path('destiny-number/', destiny_number_view, name='destiny_number'),

    # path('list',current_year , name='list'),
]
