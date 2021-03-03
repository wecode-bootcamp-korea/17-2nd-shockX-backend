from jwt                import DecodeError
from json               import JSONDecodeError

import json
import bcrypt
import jwt
import re

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q
from django.utils       import timezone

from .models            import User, SellerLevel, ShippingInfomation
from utils              import login_decorator
from my_settings        import ALGORITHM, SECRET_KEY

MINIMUM_PASSWORD_LENGTH = 8

class SignIpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try :
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'INVALID_USER_ID'}, status=401)

            user            = User.object.get(email = email)
            hashed_password = user.password
            
            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER_PASSWORD'}, status=401)

            access_token = jwt.encode({'userPk' : user.pk}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'accessToken' : access_token}, status=200)
           
        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)
