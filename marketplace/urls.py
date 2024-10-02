from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    # path('deposit', views.process_deposit, name='deposit'),
    # path('checkout', views.process_deposit, name='checkout'),
    # path('errors', views.process_deposit, name='errors'),
    # path('success', views.process_deposit, name='success'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('signup/farmer/', views.farmer_signup, name='farmer_signup'),
    path('signup/customer/', views.customer_signup, name='customer_signup'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/list/', views.product_list, name='product_list'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('products/purchase/<uuid:product_id>/', views.purchase_product, name='purchase'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('mark_order_done/<uuid:order_id>/', views.mark_order_done, name='mark_order_done'),
]
