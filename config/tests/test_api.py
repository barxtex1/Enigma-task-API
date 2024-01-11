from rest_framework.test import APITestCase, override_settings
from django.urls import reverse
from rest_framework import status
from collections import defaultdict
import json
import tempfile
from pathlib import Path



class ProductTestCase(APITestCase):
    def setUp(self):
        '''
        Load credentials for Users and get authentication tokens to check permissions
        '''
        # Load credentials for users
        with open('credentials.json', 'r') as file:
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
        '''
        Display a list of all products
        - Access: all users, even not logged in
        '''
        url = reverse('product-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_product(self):
        '''
        Display the details of the indicated product (pk/id)
        - Access: all users, even not logged in
        '''
        product_id = "13"
        url = reverse('product-detail', args=[product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    @override_settings(MEDIA_ROOT=Path(tempfile.gettempdir()))
    def test_create_product(self):
        '''
        Adding a Product(name, description, price, category, image)
        Thumbnail image generates automatically
        - Access: vendor
        '''
        url = reverse('product-list')
        # Get an authorization token to access the endpoint
        vendor_token, customer_token = self.users.get('vendor'), self.users.get('customer')

        # Perform valid POST with vendor token (with permission)
        headers = {
            'Authorization': f'Token {vendor_token}'
        }
        with open('media/default.jpg', 'rb') as image:
            data = {
                'name': 'Laptop Asus',
                'description': 'Laptop specification',
                'price': 2500,
                'category': "Laptops",
                'image': image
            }
            response = self.client.post(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Perform invalid POST with customer token (without permission)
        headers['Authorization'] = f'Token {customer_token}'
        with open('media/default.jpg', 'rb') as image:
            data = {
                'name': 'Laptop Asus',
                'description': 'Laptop specification',
                'price': 2500,
                'category': "Laptops",
                'image': image
            }
            response = self.client.post(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    @override_settings(MEDIA_ROOT=Path(tempfile.gettempdir()))
    def test_update_product(self):
        '''
        Update a Product(name, description, price, category, image)
        - Access: vendor
        '''
        product_id = "13"
        url = reverse('product-detail', args=[product_id])
        # Get an authorization token to access the endpoint
        vendor_token, customer_token = self.users.get('vendor'), self.users.get('customer')

        # Perform valid PUT with vendor token (with permission)
        headers = {
            'Authorization': f'Token {vendor_token}'
        }
        with open('media/default.jpg', 'rb') as image:
            data = {
                'name': 'HP Pavilion x360',
                'description': 'HP Pavilion x360 updated',
                'price': 3000,
                'category': "Laptops",
                'image': image
            }
            response = self.client.put(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Perform invalid PUT with customer token (without permission)
        headers['Authorization'] = f'Token {customer_token}'
        with open('media/default.jpg', 'rb') as image:
            data = {
                'name': 'Laptop-updated',
                'description': 'Test laptop updated',
                'price': 3000,
                'category': "Laptops",
                'image': image
            }
            response = self.client.put(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_delete_product(self):
        '''
        Delete a Product(name, description, price, category, image)
        - Access: vendor
        '''
        product_id = "9"
        url = reverse('product-detail', args=[product_id])
        # Get an authorization token to access the endpoint
        vendor_token, customer_token = self.users.get('vendor'), self.users.get('customer')

        # Perform valid DELETE with vendor token (with permission)
        headers = {
            'Authorization': f'Token {vendor_token}'
        }
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Perform invalid DELETE with customer token (without permission)
        headers['Authorization'] = f'Token {customer_token}'
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class OrderTestCase(APITestCase):
    def setUp(self):
        '''
        Load credentials for Users and get authentication tokens to check permissions
        '''
        # Load credentials for users
        with open('credentials.json', 'r') as file:
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
        '''
        Create an Order(customer_name, delivery_address, products) -> total price, payment date
        - Access: customer
        'products' variable is a List of dictonary:
        {'product': pk/id, 'quantity': int}
        '''
        url = reverse('order-product')
        # Get an authorization token to access the endpoint
        vendor_token, customer_token = self.users.get('vendor'), self.users.get('customer')

        # Perform valid POST with customer token (with permission)
        headers = {
            'Authorization': f'Token {customer_token}',
        }
        data = {
            'customer_name': 'Jan Kowalski',
            'delivery_address': '1234 Elm Street',
            'products': [
                {"product": 18, "quantity": 1}, 
                {"product": 11, "quantity": 2}
            ]
        }
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Perform invalid POST with vendor token (without permission)
        headers['Authorization'] = f'Token {vendor_token}'
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_order_statistics(self):
        '''
        Statistics of the most frequently ordered products
        - Access: vendor
        Input: start_date, end_date, num_products
        Output: List of most frequently ordered products with number of items
        [
            {
                'id': pk/id,
                'name': product-name:str,
                'count': int
            },
        ]
        '''
        url = reverse('statistics-most-ordered')
        # Get an authorization token to access the endpoint
        vendor_token, customer_token = self.users.get('vendor'), self.users.get('customer')

        # Perform valid POST with vendor token (with permission)
        headers = {
            'Authorization': f'Token {vendor_token}',
        }
        data = {
            'start_date': '2024-01-09 00:00:00',
            'end_date': '2024-01-10 00:00:00',
            'num_products': 5
        }
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Perform invalid POST with customer token (without permission)
        headers['Authorization'] = f'Token {customer_token}'
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)