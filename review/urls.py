from django.urls import path
from review.views import ReviewView

urlpatterns = [
    path('/reviews', ReviewView.as_view()),
  #  path('/
]
