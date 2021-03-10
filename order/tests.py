import json
import jwt
from datetime import datetime, timedelta

from django.test    import TestCase, Client
from unittest.mock  import patch, MagicMock

from user.models    import SellerLevel, User, ShippingInformation
from product.models import Product, Size, ProductSize, Image
from order.models   import Bid, Ask, Order, OrderStatus
from my_settings    import SECRET_KEY, ALGORITHM

ORDER_STATUS_CURRENT = 'current'
ORDER_STATUS_PENDING = 'pending'

client = Client()

class BuyTest(TestCase):
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
            name          = 'Yordan',
            model_number  = 'A1234',
            ticker_number = 'AJ89',
            color         = 'black',
            description   = 'Gooood',
            retail_price  = 300.00,
            release_date  = '2020-11-10'
        )
        cls.size = Size.objects.create(
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
        cls.order_status_current = OrderStatus.objects.create(
            name = 'current'
        )
        cls.order_status_pending = OrderStatus.objects.create(
            name = 'pending'
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
        cls.ask = Ask.objects.create(
            product_size         = product_size,
            price                = 100.00,
            user                 = user,
            expiration_date      = '2020-03-31',
            order_status         = cls.order_status_current,
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
        OrderStatus.objects.all().delete()
        ShippingInformation.objects.all().delete()
        Bid.objects.all().delete()
        Ask.objects.all().delete()

    def test_buy_get_success(self):
        headers = {'HTTP_Authorization':self.token}
        
        response = client.get(f'/order/buy/{self.product.id}?size={self.size.id}', **headers)

        self.assertEqual(response.json()['data']['product']['id'], 1)
        self.assertEqual(response.json()['data']['product']['name'], "Yordan")
        self.assertEqual(response.json()['data']['product']['lowestAsk'], "100.00")
        self.assertEqual(response.json()['data']['product']['highestBid'], "100.00")
        self.assertEqual(response.json()['data']['product']['size'], "1")
        self.assertEqual(response.json()['data']['product']['image'], "a.jpg")
        self.assertEqual(response.json()['data']['shippingInfo']['name'], "shock")
        self.assertEqual(response.json()['data']['shippingInfo']['city'], "Seoul")
        self.assertEqual(response.json()['data']['shippingInfo']['country'], "South Korea")
        self.assertEqual(response.json()['data']['shippingInfo']['postalCode'], "123456")
        self.assertEqual(response.json()['data']['shippingInfo']['phoneNumber'], "123123123")
        self.assertEqual(response.status_code, 200)

    def test_buy_get_does_not_exist1(self):
        headers = {'HTTP_Authorization':self.token}

        response = client.get('/order/buy/12?size=34', **headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_SIZE_DOES_NOT_EXIST'})

    def test_buy_get_does_not_exist2(self):
        headers = {'HTTP_Authorization':self.token}

        response = client.get(f'/order/buy/{self.product.id}', **headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_SIZE_DOES_NOT_EXIST'})

    def test_buy_post_is_bid_true_success(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})

    def test_buy_post_is_bid_false_success(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"          : "0",
            "price"          : self.ask.price,
            "name"           : "sua",
            "country"        : "South Korea",
            "primaryAddress" : "Gangnam-gu",
            "city"           : "Seoul",
            "state"          : "Seoul",
            "postalCode"     : "123456",
            "phoneNumber"    : "01012341234",
            "totalPrice"     : "125.00"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})

    def test_buy_post_product_size_does_not_exist1(self): 
        headers = {'HTTP_Authorization':self.token}

        response = client.get('/order/buy/12?size=34', **headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_SIZE_DOES_NOT_EXIST'})

    def test_buy_post_product_size_does_not_exist2(self):
        headers = {'HTTP_Authorization':self.token}

        response = client.get(f'/order/buy/{self.product.id}', **headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_SIZE_DOES_NOT_EXIST'})

    def test_buy_post_is_bid_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_is_bid_invalid_value(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
                "isBid"            : "3",
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_VALUE'})

    def test_buy_post_name_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_country_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "name"             : "sua",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_primary_address_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_city_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_postal_code_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "phoneNumber"      : "01012341234",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_phone_number_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"            : "1",
            "price"            : self.ask.price,
            "name"             : "sua",
            "country"          : "South Korea",
            "primaryAddress"   : "Gangnam-gu",
            "secondaryAddress" : "427, Teheran-ro",
            "city"             : "Seoul",
            "state"            : "Seoul",
            "postalCode"       : "123456",
            "expirationDate"   : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_expiration_date_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"          : "1",
            "name"           : "sua",
            "country"        : "South Korea",
            "primaryAddress" : "Gangnam-gu",
            "city"           : "Seoul",
            "postalCode"     : "123456",
            "phoneNumber"    : "01012341234",
            "totalPrice"     : "120.00"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_total_price_key_error(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"          : "0",
            "price"          : self.ask.price,
            "name"           : "sua",
            "country"        : "South Korea",
            "primaryAddress" : "Gangnam-gu",
            "city"           : "Seoul",
            "postalCode"     : "123456",
            "phoneNumber"    : "01012341234",
            "expirationDate" : "3"
        }

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_buy_post_ask_does_not_exist(self):
        headers = {'HTTP_Authorization':self.token}
        
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user = User.objects.get(email=payload['email'])
        
        data = {
            "isBid"          : "0",
            "price"          : self.ask.price,
            "name"           : "sua",
            "country"        : "South Korea",
            "primaryAddress" : "Gangnam-gu",
            "city"           : "Seoul",
            "postalCode"     : "123456",
            "phoneNumber"    : "01012341234",
            "totalPrice"     : "125.00"
        }

        Ask.objects.all().delete()

        response = client.post(f'/order/buy/{self.product.id}?size={self.size.id}', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'ASK_DOES_NOT_EXIST'})
        
