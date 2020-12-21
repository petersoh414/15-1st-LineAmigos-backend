import json, re, bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from lineamigos.settings import SECRET_KEY, ALGORITHM

from .models import User, PhoneNumber, Gender
from .utils  import validate_username, validate_name, validate_password, validate_phone_number, SignInConfirm

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            username      = data.get("username")
            name          = data.get("name")
            gender        = data.get("gender")
            date_of_birth = data.get("date_of_birth")
            password      = data.get("password")
            country_code  = data.get("country_code")
            phone_number  = data.get("phone_number")

            if not validate_username(username):
                return JsonResponse({'message': 'INVALID_USERNAME_FORMAT'}, status=401)

            if not validate_name(name):
                return JsonResponse({'message': 'INVALID_NAME_FORMAT'}, status=401)

            if not validate_password(password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=401)

            if not validate_phone_number(phone_number):
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER_FORMAT'}, status=401)

    # username 중복성 검사
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'ALREADY_TAKEN_USERNAME'}, status=409)

            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            gender_id = Gender.objects.get(name=gender).id

            phone_number_id = PhoneNumber.objects.create(
                phone_number= phone_number).id

            user = User.objects.create(
                name            = name,
                username        = username,
                password        = hashed_password.decode(),
                date_of_birth   = date_of_birth,
                gender_id       = gender_id,
                phone_number_id = phone_number_id
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
            data     = json.loads(request.body)
            username = User.objects.get(username=data['username'])

            if not User.objects.filter(username=data['username']).exists():
                return JsonResponse({'message': 'USER_NOT_FOUND'}, status=401)

            if bcrypt.checkpw(data['password'].encode('utf-8'), username.password.encode('utf-8')):
                access_token = jwt.encode({'username': username.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'message': 'SUCCESS', 'access_token': access_token.decode('utf-8')}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'FAILED_TO_DECODE_DATA'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
