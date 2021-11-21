import json
import jwt

from django.test import TestCase, Client
from ledgers.models import Ledger
from users.models import User
from config_settings import SECRET_KEY


class TestLedgerView(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            email = 'test@test.com',
            password = 'Test123!',
            last_name = 'Potter',
            first_name = 'Harry',
        )

    def tearDown(self):
        User.objects.all().delete()
        Ledger.objects.all().delete()

    def test_post_ledger_success(self):
        client = Client()

        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm='HS256')
        header = {'HTTP_Authorization' : access_token}

        ledger = {
            'note'     : 'This is test note',
            'income'   : 50000,
            'expense'  : 0,
            'total'    : 0,
            'category' : 'Food'
        }
        print('===============================')
        print(ledger)
        print('===============================')

        response = client.post('/ledgers', json.dumps(ledger), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 201)
