import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lineamigos.settings")
django.setup()

from product.models import *

CSV_PATH_PRODUCTS='./image.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
        box = []
        data_reader = csv.reader(in_file)
        next(data_reader, None) # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
        for row in data_reader:
                if row[0]: # 상품명
                    print(row[0])
                    product_name_csv = row[0]
                if row[1]: # 가격
                    print(row[1])
                    product_price_csv = row[1]
                if row[2]: #재고
                    print(row[2])
                    is_in_stock_csv = row[2]
                if row[3]: # 이미지
                    print(row[3])
                    image_url_csv = row[3]
                if row[4]:
                    print(row[4])
                    category_id_csv = row[4]
                if row[5]:
                    print(row[5])
                    discount_id_csv = row[5]

               # category_id=Category.objects.get(id=category_id_csv)
                Image.objects.create(image_url=image_url_csv, product_id=category_id_csv)
               # Product.objects.create(name=product_name_csv, price=product_price_csv, is_in_stock=is_in_stock_csv, category_id = category_id_csv, discount_id = discount_id_csv)
