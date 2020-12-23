from django.urls import path
from review.views import AllReviewView

urlpatterns = [
    path('/reviews', AllReviewView.as_view()),
]
