import json
from django.http             import JsonResponse
from django.views            import View
from django.core.serializers import serialize
from user.models             import User
from product.models          import (
                                    Menu, 
                                    Category, 
                                    Product, 
                                    Image,
                                    Size,
                                    ProductSize,
                                    Wishlist
                                    )

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
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

class GetView(View):
    def get(self,request):
        data = json.loads(request.body)

       # 모든 제품정보 뿌려주기
        product_values = Product.objects.all().order_by('-id')
        product_data = json.loads(serialize('json', product_values))
        category_values = Category.objects.all().order_by('-id')
        category_data = json.loads(serialize('json', category_values))
        menu_values = Menu.objects.all().order_by('-id')
        menu_data = json.loads(serialize('json', menu_values))
        image_values = Image.objects.all().order_by('-id')
        image_data = json.loads(serialize('json', image_values))
        return JsonResponse(
            {'products':product_data, 
            'categories':category_data,
            'menus':menu_data,
            'images':image_data
            }
        )
