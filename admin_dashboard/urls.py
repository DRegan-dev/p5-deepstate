from django.urls import path
from . import views

app_name= 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('get_product_stats', views.get_product_stats, name='get_product_stats'),
    path('handle_category_update_ajax', views.handle_category_update_ajax, name='handle_category_update_ajax')
]