import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Count

from user.models      import User
from product.models   import Category, Product, Image, Menu 
from review.models    import Review, ReviewImage

class PostView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            price    = data['price']
            category = data['category']
            image    = data['image']
            assert Category.objects.filter(name = category).exists(), 'NO_CATEGORY'
            assert not Product.objects.filter(name = name).exists(), 'EXIST_PRODUCT'
            category_id = Category.objects.get(name = category).id
            Product.objects.create(
                    name        = name,
                    price       = price,
                    category_id = category_id
                    )
            product_id = Product.objects.get(name = name).id
            Image.objects.create(
                    image_url  = image,
                    product_id = product_id
                    )
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        # KeyError validation
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        # AssertionError validation
        except AssertionError as e:
            return JsonResponse({'MESSAGE' : f'{e}'}, status=401)

        # Request validation
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'BAD_REQUEST'}, status=400)
        
class ProductView(View):
    def get(self,request):
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 100))
        sort     = request.GET.get('sort', None)
        ordering = request.GET.get('ordering', None)
        search   = request.GET.get('search', None)

        products = Product.objects.all()

        if sort      == 'avg':
            products  = Product.objects.annotate(review_rate=Avg('review__rate')).order_by('-review_rate')
        if sort      == 'review' or sort == 'like':
            products  = Product.objects.annotate(contents=Count('review__contents')).order_by('-contents')
        if sort      == 'price':
            products  = Product.objects.order_by('price')
        if ordering  == '-id':
            products  = Product.objects.order_by('-id')
        if search:
            products  = Product.objects.filter(name__icontains=search)


        all_product = [{
                    'product_menu'      : product.category.menu.name,
                    'product_category'  : product.category.name,
                    'product_id'        : product.id,
                    'name'              : product.name,
                    'price'             : product.price,
                    'created_time'      : product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'image'             : product.image_set.get().image_url,
                    'discount'          : product.discount.rate,
                    'stock'             : product.is_in_stock,
                    'content_amount'    : product.review_set.filter().aggregate(Count('contents')),
                    'rate_average'      : product.review_set.filter().aggregate(Avg('rate')),
                    'product_likes'     : product.wishlist_set.filter().aggregate(Count('product_id'))
                    } for product in products[offset:(limit+offset)]]

        return JsonResponse({'PRODUCTS': all_product}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product    = Product.objects.get(id=product_id)

            product_detail = {
                    'id'                : product.id,
                    'product_category'  : product.category.name,
                    'product_menu'      : product.category.menu.name,
                    'name'              : product.name,
                    'price'             : product.price,
                    'created_time'      : product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'image'             : product.image_set.get().image_url,
                    'discount'          : product.discount.rate,
                    'stock'             : product.is_in_stock,
                    }

            return JsonResponse({'PRODUCT' :product_detail}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NO_PRODUCT'}, status=409)

class MenuView(View):
    def get(self, request):
        menus = Menu.objects.prefetch_related('category_set').all()

        menu_category = [{
                'id'         : menu.id,
                'menu'       : menu.name,
                'categories' : [
                    category.name
                    for category  in menu.category_set.all()]
                } for menu in menus]

        return JsonResponse({'MAIN' : menu_category}, status=200)

class BestProductView(View):
    def get(self, request):
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 100))
        products = Product.objects.all()

        best_product = [{
                    'name'            : product.name,
                    'price'           : product.price,
                    'created_time'    : product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'image'           : product.image_set.get().image_url,
                    'discount'        : product.discount.rate,
                    'stock'           : product.is_in_stock,
                    } for product in products[offset:(limit+offset)]]

        return JsonResponse({'PRODUCTS': best_product}, status=200)

