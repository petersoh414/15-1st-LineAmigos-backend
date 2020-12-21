from django.urls import path
from order.views import OrderView

urlpatterns = [
    ('/order, OrderView.as_view())
]
