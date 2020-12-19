from django.urls   import path
from product.views import PostView, ProductView, ProductDetailView

urlpatterns = [
        path('/post', PostView.as_view()),
        path('/get', ProductView.as_view()),
        path('/<int:product_id>', ProductDetailView.as_view()),
]

