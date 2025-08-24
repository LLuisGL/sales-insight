from django.urls import path
from . import data

urlpatterns = [
    path('clients/', data.best_clients, name='best_clients'),
    path('products/', data.best_products, name='best_products'),
    path('charts/', data.chart_generator, name='chart_generator'),
    path('filters/', data.get_filters, name='get_filters'),
    path('sales/', data.get_sales_info, name='get_sales_info'),
    path('count/', data.get_sales_count, name='get_sales_count')
]