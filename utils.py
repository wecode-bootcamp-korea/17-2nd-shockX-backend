import jwt
from json     import JSONDecodeError

from django.http import JsonResponse

from my_settings import ALGORITHM
from my_settings import SECRET_KEY
from user.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({'message':'NEED_LOGIN'}, status=400)

        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(email=payload['email'])
            request.user = user

            return func(self, request, *args, **kwargs)
        

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

    return wrapper
