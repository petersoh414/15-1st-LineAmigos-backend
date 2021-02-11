import json
from django.utils   import timezone
from django.test    import TestCase, Client
from user.models    import Gender, PhoneNumber, User
from product.models import Menu, Category, Product, Image, Discount, Wishlist
from review.models  import Review

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.maxDiff = None

        Menu.objects.create(
                id   = 1,
                name = '용품'
                )

        Category.objects.create(
                id      = 1,
                menu_id = 1,
                name    = '열쇠고리'
                )

        Product.objects.create(
                category_id = 1,
                name        = '베스파 열쇠고리',
                price       = 10000
                )

    def tearDown(self):
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_product_post_success(self):
        product_info = {
                'name'     : '오리지날',
                'price'    : 100000,
                'category' : '열쇠고리',
                'image'    : 'test'
                }
        response = self.client.post('/product/post', json.dumps(product_info), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'SUCCESS'
                })
    
    def test_product_post_name_keyerror(self):
        product_no_name_info = {
                'price'    : 100000,
                'category' : '열쇠고리',
                'image'    : 'test'
                }
        response = self.client.post('/product/post', json.dumps(product_no_name_info), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'KEY_ERROR'
                })

    def test_product_post_price_keyerror(self):
        product_no_price_info = {
                'name'     : '오리지날',
                'category' : '열쇠고리',
                'image'    : 'test'
                }
        response = self.client.post('/product/post', json.dumps(product_no_price_info), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'KEY_ERROR'
                })
    
    def test_product_post_image_keyerror(self):
        product_no_image_info = {
                'name'     : '오리지날',
                'price'    : 100000,
                'category' : '열쇠고리'
                }
        response = self.client.post('/product/post', json.dumps(product_no_image_info), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'KEY_ERROR'
                })

    def test_product_post_category_keyerror(self):
        product_no_image_info = {
                'name'  : '오리지날',
                'price' : 100000,
                'image' : 'test'
                }
        response = self.client.post('/product/post', json.dumps(product_no_image_info), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'KEY_ERROR'
                })

    def test_product_post_no_categoryerror(self):
        product_no_category_info = {
                'name'     : '오리지날',
                'price'    : 10000,
                'category' : '이상한 카테고리',
                'image'    : 'test'
                }
        response = self.client.post('/product/post', json.dumps(product_no_category_info), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'NO_CATEGORY'
                })

    def test_product_post_exist_product(self): 
        product_exist_product_info = {
                'name'     : '베스파 열쇠고리',
                'price'    : 10000,
                'category' : '열쇠고리',
                'image'    : 'test'
                }
        response = self.client.post('/product/post', json.dumps(product_exist_product_info), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'EXIST_PRODUCT'
                })
    
class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.maxDiff = None

        Menu.objects.create(
                id   = 1,
                name = '용품'
                )

        Category.objects.create(
                id      = 1,
                menu_id = 1,
                name    = '열쇠고리'
                )

    def tearDown(self):
        Menu.objects.all().delete()
        Category.objects.all().delete()

    def test_product_get_menu_success(self):
        print('menu_success')
        response = self.client.get('/product/menu', content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    'MAIN' : response.json()['MAIN']                    
                })

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.maxDiff = None

        Gender.objects.create(
                id   = 1,
                name = 'men'
                )
        PhoneNumber.objects.create(
                id           = 1,
                country_code = 82,
                phone_number = '010-9999-8888'
                )
        User.objects.create(
                id              = 1,
                name            = 'Mun',
                password        = 1233123,
                date_of_birth   = '2020-01-11',
                gender_id       = 1,
                phone_number_id = 1
                )
        Menu.objects.create(
                id   = 1,
                name = '용품'
                )
        Category.objects.create(
                id      = 1,
                menu_id = 1,
                name    = '열쇠고리'
                )
        Discount.objects.create(
                id   = 1,
                rate = 15.00
                ) 
        self.product = Product.objects.create(
                id          = 1,
                category_id = 1,
                name        = '베스파 열쇠고리',
                price       = 10000,
                is_in_stock = True,
                discount_id = 1,
                )
        Image.objects.create(
                id          = 1,
                product_id  = 1,
                image_url   = 'test'
                )
        Review.objects.create(
                id         = 1,
                user_id    = 1,
                product_id = 1,
                rate       = 4.8,
                contents   = 'test',
                )
        Wishlist.objects.create(
                product_id = 1,
                user_id    = 1
                )

    def tearDown(self):
        Gender.objects.all().delete()
        PhoneNumber.objects.all().delete()
        User.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Image.objects.all().delete()
        Discount.objects.all().delete()
        Review.objects.all().delete()
        Wishlist.objects.all().delete()

    def test_product_get_product_view_success(self):
        response = self.client.get('/product/products_info', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    'PRODUCTS': [{
                        'product_menu'          : '용품',
                        'product_category'      : '열쇠고리',
                        'product_id'            : 1,
                        'name'                  : '베스파 열쇠고리',
                        'price'                 : '10000.00',
                        'created_time'          : self.product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'image'                 : 'test',
                        'discount'              : '15.00',
                        'stock'                 : True,
                        'content_amount'        : {
                            'contents__count'   : 1
                        },
                        'rate_average'          : {
                            'rate__avg'         : 4.8
                        },
                        'product_likes'         : {
                            'product_id__count' : 1
                        }
                }]})

    def test_product_get_product_detail_view_success(self):
        self.product_id = 1
        response = self.client.get(f'/product/{self.product_id}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    'PRODUCT': {
                        'product_menu'     : '용품',
                        'product_category' : '열쇠고리',
                        'id'               : 1,
                        'name'             : '베스파 열쇠고리',
                        'price'            : '10000.00',
                        'created_time'     : self.product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'image'            : 'test',
                        'discount'         : '15.00',
                        'stock'            : True,
                }})

    def test_product_get_best_product_view_success(self):
        response = self.client.get('/product/best', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    'PRODUCTS': [{
                        'name'         : '베스파 열쇠고리',
                        'price'        : '10000.00',
                        'created_time' : self.product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'image'        : 'test',
                        'discount'     : '15.00',
                        'stock'        : True,
                }]})
