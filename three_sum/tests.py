from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from three_sum.models import Transactions
import json

# Create your tests here.

class ThreeSumSolution(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='raghvendrasingh',email= 'raghvendra@api.test')
        self.user.set_password('random')
        self.client.login(username='raghvendra', password='random')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_query_three_sum_solution(self):
        response = self.client.post('/api/calculate-three-sum/',
                                    {"input_list": [1, 3, 4, 5, 6, 7, -1, -4, 12, 1],
                                        "sum": 12}, format='json')
        self.assertEqual("[[1, 5, 6], [1, 4, 7], [1, -1, 12]]", response.json())
        self.assertEqual("[[1, 5, 6], [1, 4, 7], [1, -1, 12]]", Transactions.objects.last().result)

    def test_invalid_sum_value(self):
        response = self.client.post('/api/calculate-three-sum/',
                                    {"input_list": [1, 3, 4, 5, 6, 7, -1, -4, 12, 1],
                                     "sum": None}, format='json')
        self.assertEqual({'sum': ['This field may not be null.']}, response.json())
        self.assertEqual(0, Transactions.objects.all().count())  # No entry created in db

    def test_empty_list(self):
        response = self.client.post('/api/calculate-three-sum/',
                                    {"input_list": [],
                                     "sum": 8}, format='json')
        self.assertEqual({'non_field_errors': ['Invalid Input List']}, response.json())
        self.assertEqual(0, Transactions.objects.all().count())

    def test_no_combination_possible(self):
        response = self.client.post('/api/calculate-three-sum/',
                                    {"input_list": [1, 3, 4, 5, 6, 7, -1, -4, 12, 1],
                                     "sum": 30}, format='json')
        self.assertEqual('No combination found', json.loads(response.content))
        self.assertEqual(0, Transactions.objects.all().count())

    def test_transaction_history(self):
        self.client.post('/api/calculate-three-sum/',
                                    {"input_list": [1, 3, 4, 5, 6, 7, -1, -4, 12, 1],
                                     "sum": 12}, format='json')
        self.assertEqual(1, Transactions.objects.all().count())

