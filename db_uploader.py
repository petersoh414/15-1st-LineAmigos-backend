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
                if row[2]: #이미지
                    print(row[2])
                    product_image_csv = row[2]
                if row[3]:
                    print(row[3])
                    category_id_csv = row[3]
                
               # Image.objects.create(image_url=product_image_csv, product_id=category_id_csv)
                #category_pk = Category_CSV.objects.get(category_name=category_name_csv)
               # Drink_CSV.objects.create(drink_name=drink_name_csv, category=category_pk)
