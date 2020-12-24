import json

from django.views import View
from django.http  import JsonResponse

from user.models    import User, Gender, PhoneNumber
from product.models import Menu, Category, Discount, Product, Size, Image
from review.models  import Review, ReviewImage

class ReviewView(View):
    def get(self, request):
        try:

            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 100))

            reviews = Review.objects.all()

            review = [{
                'user':             review.user.username,
                'product_name':     review.product.name,
                'reviewed_image':   review.reviewimage_set.get().image_url,
                'product_option':   review.product.productsize_set.name,
                'created_time':     review.created_at,
                'monthly_reviewed': review.is_monthly_reviewed,
                'rate':             review.rate,
                'reviewed_body':    review.contents,
            } for review in reviews[offset:limit]]

            return JsonResponse({'MESSAGE': 'SUCCEESS', 'review': review}, status=200)

        except Review.DoesNotExist:
            JsonResponse({'MESSAGE': 'NOOOOOO_REIVEW'}, stauts=404)

