from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.dashboard_index, name='dashboard-index' ),
    path('manager/emplacements/', views.emplacements, name='dashboard-emplacements'),
    path('manager/emplacements/<int:emplacement_pk>/', views.emplacement_details, name='dashboard-emplacement-details'),
    path('manager/emplacements/add_emplacement/', views.add_emplacement, name='dashboard-add-emplacement'),
    path('manager/cities/add_city/', views.add_city, name='add-city'),
    path('manager/cities/cities_list/', views.cities_list, name='cities_list'),
    path('manager/staff/add_staff/', views.add_staff, name='dashboard-add-staff'),
    path('manager/orders/order_list', views.manager_order_list, name='manager-order-list'),
    path('manager/orders/new_orders', views.manager_new_orders, name='manager-new-orders'),
    # path('manager/orders/<int:order_pk>/order_details', views.manager_order_details, name='manager-order-details'),
    path('manager/orders/<int:order_pk>/order_pickup', views.order_pickup, name='order-pickup'),

    path('receiver/products/product/<int:pk>/validation/',views.product_validation, name='product-validation'),
    path('receiver/products/product/<int:product_pk>/print_barcode/',views.product_barcode, name='print-barcode'),
    path('vendor/products/add_product/', views.add_product, name='dashboard-add-product'),
    path('vendor/products/product/<int:pk>',views.product_detail, name='product-detail'),
    path('vendor/products/inventory/', views.product_list, name='dashboard-inventory'),
    path('vendor/orders/add_order', views.add_order, name='add-order'),
    path('vendor/orders/orders_list', views.orders_list, name='orders-list'),
    path('vendor/orders/<int:pk>/order_add_details', views.order_add_product, name='order-add-product'),
    path('vendor/orders/<int:pk>/order_validation', views.order_validation, name='order-validation'),
    path('vendor/orders/<int:order_pk>/<int:item_pk>/edit/', views.order_edit, name='order-edit'),
    path('vendor/orders/<int:order_pk>/<int:item_pk>/delete_item/', views.order_item_delete, name='order-item-delete'),
    path('vendor/orders/<int:pk>/delete', views.order_delete, name='order-delete'),
]
