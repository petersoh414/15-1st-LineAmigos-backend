from django.urls import path
from review.views import AllReviewView
#,ReviewByProduct

urlpatterns = [
    path('/reviews', AllReviewView.as_view()),
#    path('/<int:review_id>', ReviewByProduct.as_view()),

]
