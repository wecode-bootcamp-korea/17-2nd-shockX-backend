import json
import jwt
from datetime import datetime

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from user.models    import SellerLevel, User, ShippingInformation, Portfolio
from product.models import Product, Size, ProductSize, Image
from order.models   import Bid, Ask, Order, OrderStatus
from my_settings    import SECRET_KEY, ALGORITHM

ORDER_STATUS_CURRENT = 'current'
ORDER_STATUS_PENDING = 'pending' 
ORDER_STATUS_HISTORY = 'history' 

client = Client()

class PortfolioTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        seller_level = SellerLevel.objects.create(
            name            = '1',
            transaction_fee = 9.5
        )
        user = User.objects.create(
            email        = 'shockx@wecode.com',
            name         = 'shocking',
            seller_level = seller_level
        )
        cls.product = Product.objects.create(
            id            = 1,
            name          = 'Yordan',
            model_number  = 'A1234',
            ticker_number = 'AJ89',
            color         = 'black',
            description   = 'Gooood',
            retail_price  = 300.00,
            release_date  = '2020-11-10'
        )
        cls.size = Size.objects.create(
            id   = 1,
            name = '1'
        )
        product_size = ProductSize.objects.create(
            product = cls.product,
            size    = cls.size
        )
        Image.objects.create(
            image_url = 'a.jpg',
            product   = cls.product
        )
        Portfolio.objects.create(
            user           = user,
            product_size   = product_size,
            purchase_date  = '2020-01-30',
            purchase_price = '500'
        )
        cls.order_status_current = OrderStatus.objects.create(
            name = 'current'
        )
        cls.order_status_pending = OrderStatus.objects.create(
            name = 'pending'
        )
        cls.order_status_history = OrderStatus.objects.create(
            name = 'history'
        )
        shipping_information = ShippingInformation.objects.create(
            name            = 'shock',
            country         = 'South Korea',
            primary_address = 'Gangnam-gu',
            city            = 'Seoul',
            postal_code     = '123456',
            phone_number    = '123123123',
            user            = user
        )
        Bid.objects.create(
            product_size         = product_size,
            price                = 100.00,
            user                 = user,
            expiration_date      = '2020-03-31',
            order_status         = cls.order_status_current,
            shipping_information = shipping_information
        )
        Ask.objects.create(
            product_size         = product_size,
            price                = 100.00,
            user                 = user,
            expiration_date      = '2020-03-31',
            order_status         = cls.order_status_history,
            shipping_information = shipping_information
        )
        Ask.objects.create(
            product_size         = product_size,
            price                = 200.00,
            user                 = user,
            expiration_date      = '2020-05-15',
            order_status         = cls.order_status_history,
            shipping_information = shipping_information
        )

        cls.token = jwt.encode({'email':user.email}, SECRET_KEY, algorithm=ALGORITHM)
    
    def tearDown(self):
        SellerLevel.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()
        Image.objects.all().delete()
        Portfolio.objects.all().delete()
        OrderStatus.objects.all().delete()
        ShippingInformation.objects.all().delete()
        Bid.objects.all().delete()
        Ask.objects.all().delete()

    def test_portfolio_get_success(self):
        headers = {'HTTP_Authorization':self.token}
        
        response = client.get('/user/portfolio', **headers)

        self.assertEqual(response.json(), 
            {
                "portfolio": [
                    {
                        "name"           : "Yordan",
                        "size"           : "1",
                        "purchase_date"  : "2020/01/30",
                        "purchase_price" : 500,
                        "market_value"   : 150
                        }
                ]
            } 
        )
        self.assertEqual(response.status_code, 200)

    def test_portfolio_post_success(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 1,
            "size_id"        : 1,
            "month"          : "10",
            "year"           : "2020",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})

    def test_portfolio_post_product_id_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "size_id"        : 1,
            "month"          : "10",
            "year"           : "2020",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_portfolio_post_size_id_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 1,
            "month"          : "10",
            "year"           : "2020",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_portfolio_post_month_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 1,
            "size_id"        : 1,
            "year"           : "2020",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_portfolio_post_year_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 1,
            "size_id"        : 1,
            "month"          : "10",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_portfolio_post_purchase_price_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 1,
            "size_id"        : 1,
            "month"          : "10",
            "year"           : "2020",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_portfolio_post_product_size_does_not_exist1(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 2,
            "size_id"        : 1,
            "month"          : "10",
            "year"           : "2020",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_SIZE_DOES_NOT_EXIST'})

    def test_portfolio_post_product_size_does_not_exist2(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])

        data = {
            "product_id"     : 1,
            "size_id"        : 2,
            "month"          : "10",
            "year"           : "2020",
            "purchase_price" : "150",
        }

        response = client.post('/user/portfolio', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_SIZE_DOES_NOT_EXIST'})

