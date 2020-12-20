import json
from django.http             import JsonResponse
from django.views            import View
from django.core.serializers import serialize
from user.models             import User
from product.models          import Category, Product, Image, Menu

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_name     = data['name']
            product_price    = data['price']
            product_category = data['category']
            product_image    = data['image']

            # Key validation
            if data['name'] == '' or data['price'] == '' or data['category'] == '' or data['image'] == '':
                raise KeyError
            
            # Category validation
            if not Category.objects.filter(name = product_category).exists():
                return JsonResponse({'MESSAGE' : 'NO_CATEGORY'}, status=400)

            # Product validation
            if not Product.objects.filter(name = product_name, price = product_price).exists():
                category_id = Category.objects.get(name = product_category).id
                Product.objects.create(name = product_name, price = product_price, category_id =category_id)
                product_id = Product.objects.get(name = product_name).id
                Image.objects.create(image_url = product_image, product_id = product_id)
                return JsonResponse({'MESSAGE' : 'ALL_SUCCESS'}, status=201)
            return JsonResponse({'MESSAGE' : 'EXIST_PRODUCT'}, status=401)
        
        # Request validation
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'BAD_REQUEST'}, status=400)
        
        # Not enough info
        except KeyError:
            return JsonResponse({'MESSAGE' : 'NOT_ENOUGH_INFO'}, status=400)

class ProductView(View):
    def get(self,request):
        try:
            products = Product.objects.select_related('category', 'category__menu').prefetch_related('image_set').all()
            
            all_product = [{
                    'product_menu'    : product.category.menu.name,
                    'product_category': product.category.name,
                    'product_id'      : product.id,
                    'name'            : product.name,
                    'price'           : product.price,
                    'created_time'    : product.created_at,
                    'product_image'   : product.image_set.get().image_url,
                    'sale_amount'     : 10 # 추가 구현 예정
                    } for product in products] 

            return JsonResponse({'PRODUCTS': all_product}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NO_PRODUCT'}, status=500)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.select_related('category', 'category__menu').prefetch_related('image_set', 'productsize_set', 'wishlist_set').get(id=product_id)
        
            product_detail = {
                    'id'              : product.id,
                    'product_category': product.category.name,
                    'product_menu'    : product.category.menu.name,
                    'product_name'    : product.name,
                    'price'           : product.price,
                    'created_time'    : product.created_at,
                    'image'           : product.image_set.get().image_url,
                    #추후 리뷰 불러오기용도    : product.productdescription_set.get().content,
                    #추후 리뷰 불러오기용도     : product.detailedimage_set.get().product_image_url,
                    }
            return JsonResponse({'product_id' :product_detail}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NO_PRODUCT'}, status=401)

class MenuView(View):
    def get(self, request):
        try:
            menus = Menu.objects.prefetch_related('category_set').all()

            menu_category = [{
                'id'         : menu.id,
                'menu'       : menu.name,
                'categories' : [
                    category.name
                    for category  in menu.category_set.all()]
                } for menu in menus]

            return JsonResponse({'main' : menu_category}, status=200)
        except:
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=400)
