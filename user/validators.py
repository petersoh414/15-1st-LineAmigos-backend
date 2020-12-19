# import jwt
# import bcrypt
# import re

# from django.http import JsonResponse
# from user.models import User

# username_regex = '/[a-zA-Z0-9_-]{5,20}/'
# username_regex = '^[a-zA-Z0-9]{1,20}$'

# name_regex = '/[a-zA-Z가-힣]/'
# password_regex = '/[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/'
# phone_number_regex = '/([01]{2,})([01679]{1,})([0-9]{3,4})([0-9]{4})/'


# def validate_username(username):
#     return re.match(username_regex, username)


# def validate_name(name):
#     return re.match(name_regex, name)


# def validate_password(password):
#     return re.match(password_regex, password)


# def get_hashed_pw(password):
#     return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")

# if not validate_username(username):
#     return JsonResponse({'message': 'INVALID_USERNAME_FORMAT'}, status=400)
#     print("== == == == == ===1 == == == == == == == == ==")

# if not validate_name(name):
#     return JsonResponse({'message': 'INVALID_NAME_FORMAT'}, status=400)
#     print("== == == == == ===2 == == == == == == == == ==")

# if not validate_password(password):
#     return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)
#     print("== == == == == ===3 == == == == == == == == ==")

# if not re.match(phone_number_regex, phone_number):
#     return JsonResponse({'message': 'INVALID_PHONE_NUMBER_FORMAT'}, status=400)
#     print("== == == == == ===4 == == == == == == == == ==")
