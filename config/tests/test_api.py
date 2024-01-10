from rest_framework.test import APITestCase, override_settings
from django.urls import reverse
from rest_framework import status
from collections import defaultdict
import json
import tempfile
from pathlib import Path


class ProductTestCase(APITestCase):
    def setUp(self):
        # Load credentials for users
        with open('tests/credentials.json', 'r') as file:
            credentials = json.loads(file.read())["Credentials"]
        
        # Get Authentication tokens
        url = reverse('api_token_auth')
        self.users = defaultdict(str)
        for user, cred in credentials.items():
            response = self.client.post(
                url, 
                data={
                    "username": cred["username"], 
                    "password": cred["password"]
                }
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.users[user] = response.json()["token"]


    def test_list_product(self):
        url = reverse('product-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_product(self):
        product_id = "1"
        url = reverse('product-detail', args=product_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    @override_settings(MEDIA_ROOT=Path(tempfile.gettempdir()))
    def test_create_product(self):
        url = reverse('product-list')
        vendor_token = self.users.get('vendor')
        self.assertIsNotNone(vendor_token)
        headers = {
            'Authorization': f'Token {vendor_token}'
        }
        with open('media/default.jpg', 'rb') as image:
            data = {
                'name': 'Laptop-request',
                'description': 'Test laptop',
                'price': 2500,
                'category': "Laptops",
                'image': image
            }
            response = self.client.post(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    @override_settings(MEDIA_ROOT=Path(tempfile.gettempdir()))
    def test_update_product(self):
        product_id = "1"
        url = reverse('product-detail', args=product_id)
        vendor_token = self.users.get('vendor')
        self.assertIsNotNone(vendor_token)
        headers = {
            'Authorization': f'Token {vendor_token}'
        }
        with open('media/default.jpg', 'rb') as image:
            data = {
                'name': 'Laptop-updated',
                'description': 'Test laptop updated',
                'price': 3000,
                'category': "Laptops",
                'image': image
            }
            response = self.client.put(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_delete_product(self):
        product_id = "1"
        url = reverse('product-detail', args=product_id)
        vendor_token = self.users.get('vendor')
        headers = {
            'Authorization': f'Token {vendor_token}'
        }
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderTestCase(APITestCase):
    def setUp(self):
        # Load credentials for users
        with open('tests/credentials.json', 'r') as file:
            credentials = json.loads(file.read())["Credentials"]
        
        # Get Authentication tokens
        url = reverse('api_token_auth')
        self.users = defaultdict(str)
        for user, cred in credentials.items():
            response = self.client.post(
                url, 
                data={
                    "username": cred["username"], 
                    "password": cred["password"]
                }
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.users[user] = response.json()["token"]


    def test_create_order(self):
        url = reverse('order-product')
        customer_token = self.users.get('customer')
        self.assertIsNotNone(customer_token)
        headers = {
            'Authorization': f'Token {customer_token}',
        }
        data = {
            'customer_name': 'Jan Kowalski',
            'delivery_address': '1234 Elm Street',
            'products': [
                {"product": 2, "quantity": 1}, 
                {"product": 3, "quantity": 2}
            ]
        }
        response = self.client.post(url, data, headers=headers, format='json')
        # print(f"Response after POST order:\n{response.json()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_order_statistics(self):
        url = reverse('statistics-most-ordered')
        vendor_token = self.users.get('vendor')
        self.assertIsNotNone(vendor_token)
        headers = {
            'Authorization': f'Token {vendor_token}',
        }
        data = {
            'start_date': '2024-01-09 00:00:00',
            'end_date': '2024-01-10 00:00:00',
            'num_products': 5
        }
        response = self.client.post(url, data, headers=headers, format='json')
        print(f"Response after POST statistics most ordered:\n{response.json()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)