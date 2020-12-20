import json,      re, bcrypt, jwt
from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from lineamigos.settings    import SECRET_KEY, ALGORITHM
from .models import User, PhoneNumber, Gender
from .utils  import SignInConfirm


username_regex     = '^[a-z0-9_-]{5,20}$'  # 아이디 5-20자 영문소문자, 숫자, (-,_) 허용
name_regex         = '^[a-z가-힣A-Z]{1,}$'  # 이름 영문 대소문자 한글 가
password_regex     = '^.*(?=^.{8,16}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[~,!,@,#,$,*,(,),=,+,_,.,|]).*$'
phone_number_regex = '^\d{3}-\d{3,4}-\d{4}$'  # 전화번호


def validate_username(username):
    return re.match(username_regex, username)


def validate_name(name):
    return re.match(name_regex, name)


def validate_password(password):
    return re.match(password_regex, password)


def validate_password(password):
    return re.match(password_regex, password)


def validate_phone_number(phone_number):
    return re.match(phone_number_regex, phone_number)


class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            username        = data.get("username")
            name            = data.get("name")
            gender_id       = data.get("gender_id")
            date_of_birth   = data.get("date_of_birth")
            password        = data.get("password")
            phone_number_id = data.get("phone_number_id")
            country_code    = data.get("country_code")
            phone_number    = data.get("phone_number")

            print(data)

            if not validate_username(username):
                return JsonResponse({'message': 'INVALID_USERNAME_FORMAT'}, status=400)
            if not validate_name(name):
                return JsonResponse({'message': 'INVALID_NAME_FORMAT'}, status=400)

            if not validate_password(password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)

            if not validate_phone_number(phone_number):
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER_FORMAT'}, status=400)

    # username 중복성 검사
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'ALREADY_TAKEN_USERNAME'}, status=409)

            hashed_password = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())
            gender_id = Gender.objects.get(name=data['gender']).id

            phone_number = PhoneNumber.objects.create(
                country_code=country_code,
                phone_number=phone_number)

            phone_number_id = PhoneNumber.objects.get(
                phone_number=data["phone_number"]).id
            print(phone_number_id)

            user = User.objects.create(
                name=name,
                username=username,
                password=hashed_password.decode(),
                date_of_birth=date_of_birth,
                gender_id=gender_id,
                phone_number_id=phone_number_id
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'FAILED_TO_DECODE_DATA'}, status=400)

        except ValidationError:
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(username=data['username']).exists():
                username = User.objects.get(username=data['username'])

                if bcrypt.checkpw(data["password"].encode('utf-8'), username.password.encode('utf-8')):
                    access_token = jwt.encode(
                        {'username': username.id}, SECRET_KEY, algorithm=ALGORITHM)

                    return JsonResponse({'message': 'SUCCESS', 'access_token': access_token.decode('utf-8')}, status=200)

                else:
                    return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
            else:  # ObjectDoesNotExist
                return JsonResponse({'message': 'USER_NOT_FOUND'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'FAILED_TO_DECODE_DATA'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
