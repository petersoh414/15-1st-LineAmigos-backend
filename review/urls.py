from django.urls import path
from review.views import ReviewView, ReviewIDView

urlpatterns = [
    path('/reviews', ReviewView.as_view()),
    path('/<int:review_id>', ReviewIDView.as_view()),
]
