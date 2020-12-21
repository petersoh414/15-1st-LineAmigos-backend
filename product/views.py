import json

from django.http    import JsonResponse
from django.views   import View

from user.models    import User
from product.models import Category, Product, Image, Menu
from review.models  import Review, ReviewImage

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
                raise ValueError
            
            # Category validation
            if not Category.objects.filter(name = product_category).exists():
                return JsonResponse({'MESSAGE' : 'NO_CATEGORY'}, status=400)

            # Product validation
            if Product.objects.filter(name = product_name, price = product_price).exists():
                return JsonResponse({'MESSAGE' : 'EXIST_PRODUCT'}, status=409)
            category_id = Category.objects.get(name = product_category).id
            Product.objects.create(name = product_name, price = product_price, category_id =category_id)
            product_id = Product.objects.get(name = product_name).id
            Image.objects.create(image_url = product_image, product_id = product_id)
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        
        # Request validation
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'BAD_REQUEST'}, status=400)
        
        # Not enough info
        except ValueError:
            return JsonResponse({'MESSAGE' : 'NOT_ENOUGH_INFO'}, status=400)

class AllProductView(View):
    def get(self,request):
        products = Product.objects.all()

        all_product = [{
                    'product_menu'    : product.category.menu.name,
                    'product_category': product.category.name,
                    'product_id'      : product.id,
                    'name'            : product.name,
                    'price'           : product.price,
                    'created_time'    : product.created_at,
                    'product_image'   : product.image_set.get().image_url,
                    'sale_amount'     : 10,
                    } for product in products]

        return JsonResponse({'PRODUCTS': all_product}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        
            product_detail = {
                    'id'              : product.id,
                    'product_category': product.category.name,
                    'product_menu'    : product.category.menu.name,
                    'product_name'    : product.name,
                    'price'           : product.price,
                    'created_time'    : product.created_at,
                    'image'           : product.image_set.get().image_url,
                    }
            return JsonResponse({'product' :product_detail}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NO_PRODUCT'}, status=409)

class MenuView(View):
    def get(self, request):
        menus = Menu.objects.all()

        menu_category = [{
                'id'         : menu.id,
                'menu'       : menu.name,
                'categories' : [
                    category.name
                    for category  in menu.category_set.all()]
                } for menu in menus]

        return JsonResponse({'main' : menu_category}, status=200)
