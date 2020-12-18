from django.urls import path
from product.views import PostView

urlpatterns = [
        path('/post', PostView.as_view()),
]

