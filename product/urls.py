from django.urls   import path
from product.views import PostView, AllProductView, ProductDetailView, MenuView #DetailView

urlpatterns = [
        path('/post', PostView.as_view()),
        path('/menu', MenuView.as_view()),
        path('/products_info', AllProductView.as_view()),
        path('/detail', ProductDetailView.as_view()),
        #path('/details/<int:category>', DetailView.as_view()),
]


