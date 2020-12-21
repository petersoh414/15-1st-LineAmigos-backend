import json

from django.views import View
from django.http import JsonResponse

from user.models import User,
from user.utils import SignInConfirm


from .models import DeliveryInformation, Status, PaymentMethod, Order, Cart

class OrderView(View):
    @SignInConfirm
    def get(self, request):
        data = json.loads(request.body)
        list = [{


        }]
