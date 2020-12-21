import re, json, jwt

from django.http import JsonResponse

from lineamigos.settings import SECRET_KEY, ALGORITHM

from .models import User, PhoneNumber, Gender


username_regex     = '^[a-z0-9_-]{5,20}$'  # 아이디 5-20자 영문소문자, 숫자, (-,_) 허용
name_regex         = '^[a-z가-힣A-Z]{1,}$'  # 이름 영문 대소문자 한글 가
#password_regex     = '^.*(?=^.{8,16}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[~,!,@,#,$,*,(,),=,+,_,.,|]).*$'
password_regex = '^[a-z]{1,}$'
phone_number_regex = '^\d{3}-\d{3,4}-\d{4}$'  # 전화번호


def validate_username(username):
    return re.match(username_regex, username)

def validate_name(name):
    return re.match(name_regex, name)

def validate_password(password):
    return re.match(password_regex, password)

def validate_phone_number(phone_number):
    return re.match(phone_number_regex, phone_number)

class SignInConfirm:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization", None)
        print(access_token)

        try:
            if access_token:
                token_payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                user          = User.objects.get(id = token_payload["username"])
                request.user  = user
                return self.original_function(self, request, *args, **kwargs)

            return JsonResponse({'message': "SIGNIN_REQUIRED"}, status = 401)

        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_USER"}, status = 401)

        except User.DoesNotExist:
            return JsonResponse({'message': "INVALID_USER"}, status = 401)
