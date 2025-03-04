from django.urls import path

from . import views


urlpatterns = [
    
    path('checkout', views.checkout, name="order.checkout"),
    path('complete-order', views.complete_order, name="order.complete-order"),

    path('success', views.order_success, name="order.success"),
    path('failed', views.order_failed, name="order.failed")

]
