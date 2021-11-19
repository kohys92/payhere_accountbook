import json
import re
import bcrypt

from django.views import View
from django.http import JsonResponse
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