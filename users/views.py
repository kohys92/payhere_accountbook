import json
import re
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from config_settings import SECRET_KEY
from .models import User


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            # Email Validation using regex
            if not re.search('[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+', data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            # Email duplication : to prevent from server goes 500
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'DUPLICATED_EMAIL'}, status = 400)

            # Password validation
            if not re.fullmatch('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

            User.objects.create(
                email      = data['email'],
                password   = bcrypt.hashpw(data['password'].encode('utf-8'), salt=bcrypt.gensalt()).decode(),
                last_name  = data['last_name'],
                first_name = data['first_name'],
            )

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) or data['password'] is None:
                    access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = 'HS256')

                    return JsonResponse({'message' : 'Login Success!', 'access_token' : access_token}, status = 200)

                return JsonResponse({'message' : 'INVALID PASSWORD'}, status = 400)

            return JsonResponse({'message' : 'INVALID USER'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)