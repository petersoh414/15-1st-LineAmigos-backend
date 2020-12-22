import json

from django.views import View
from django.http import JsonResponse

from user.models import User, Gender, PhoneNumber
from product.models import Menu, Category, Discount, Product, Size, Image
from review.models import Review, ReviewImage, Question, Answer


class AllReviewView(View):
    def get(self, request):
        try:
            reviews = Review.objects.all()
            #reviews = Review.objects.select_related('user','product')
            print(reviews)

            review = [
                {
                    'user': review.user.username,
                    'product_name': review.product.name,
                    'image': review.reviewimage_set.get().image_url,
                    'prodcut_option': review.product.size_set().,
                    'created_time': review.created_at,
                    'monthly_rivewed': review.is_monthly_reviewed,
                    'rate': review.rate,
                    'review_body': review.contents,
                } for review in reviews
            ]

            return JsonResponse({'MESSAGE': 'all_Review'}, status=200)

        except Review.DoesNotExist:
            JsonResponse({'MESSAGE': "NOOOOOO_REIVEW"})
