import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, Min, Avg
from django.test      import TestCase, Client

from .models          import Product, Image, Size, ProductSize 
from order.models     import Ask, Bid, OrderStatus, ExpirationType
from user.models      import User, SellerLevel, ShippingInformation

client = Client()
class ProductDetailTest(TestCase):
    def setUp(self):
        SellerLevel.objects.create(
            id              = 1,
            name            = '1',
            transaction_fee = 9.5
        )

        User.objects.create(
            id              = 1,
            name            = 'hyeyoon',
            email           = 'hyeyoon@gmail.com',
            seller_level_id = 1
        )

        ShippingInformation.objects.create(
            id                = 1,
            name              = 'ab',
            country           = 'korea',
            primary_address   = 'a',
            secondary_address = 'b',
            state             = 'c',
            postal_code       = '13133',
            phone_number      = '010-1010-1010',
            created_at        = '2020-10-20',
            updated_at        = '2020-01-20',
            user_id           = 1
        )

        self.product = Product.objects.create(
            id            = 1,
            name          = 'hehe',
            model_number  = '9050',
            ticker_number = 'AJ6-BI19',
            color         = 'blue',
            description   = 'hi',
            retail_price  = 200,
            release_date  = '2016-02-15'
        )

        Size.objects.create(
            id   = 1,
            name = '1'
        )

        ProductSize.objects.create(
            id         = 1,
            product_id = 1,
            size_id    = 1
        )

        Image.objects.create(
            id          = 1,
            image_url   = 'yaho.jpg',
            product_id  = 1
        )

        OrderStatus.objects.create(
            id = 1,
            name = 'current'
        )

        OrderStatus.objects.create(
            id = 3,
            name = 'history'
        )

        Bid.objects.create(
            id                      = 1,
            product_size_id         = 1,
            price                   = 223,
            user_id                 = 1,
            expiration_date         = '2021-01-03',
            matched_at              = '2021-01-18',
            created_at              = '2020-02-12',
            updated_at              = '2020-02-12',
            total_price             = 400,
            order_number            = 'a1230',
            shipping_information_id = 1,
            order_status_id         = 1
        )

        Ask.objects.create(
            id                      = 1,
            product_size_id         = 1,
            price                   = 413,
            user_id                 = 1,
            expiration_date         = '2021-03-03',
            matched_at              = '2021-04-18',
            created_at              = '2020-06-12',
            updated_at              = '2020-12-12',
            total_price             = 445,
            order_number            = 'a1267',
            shipping_information_id = 1,
            order_status_id         = 1
        )

        Ask.objects.create(
            id                      = 2,
            product_size_id         = 1,
            price                   = 400,
            user_id                 = 1,
            expiration_date         = '2021-03-03',
            matched_at              = '2021-07-18',
            created_at              = '2020-03-22',
            updated_at              = '2020-02-12',
            total_price             = 465,
            order_number            = 'a1269',
            shipping_information_id = 1,
            order_status_id         = 3
        )

        Ask.objects.create(
            id                      = 3,
            product_size_id         = 1,
            price                   = 463,
            user_id                 = 1,
            expiration_date         = '2021-03-03',
            matched_at              = '2021-09-18',
            created_at              = '2020-09-12',
            updated_at              = '2020-09-21',
            total_price             = 475,
            order_number            = 'a1268', 
            shipping_information_id = 1,
            order_status_id         = 3
        )

    def tearDown(self):
        User.objects.all().delete()
        SellerLevel.objects.all().delete()
        ShippingInformation.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()
        Image.objects.all().delete()
        Bid.objects.all().delete()
        Ask.objects.all().delete()
        OrderStatus.objects.all().delete()
        OrderStatus.objects.all().delete()

    def test_product_detail_get_success(self):
        response = client.get(f'/product/detail/{self.product.id}')

        self.assertEqual(response.json()['results']['product_name'],'hehe')
        self.assertEqual(response.json()['results']['product_ticker'],'AJ6-BI19')
        self.assertEqual(response.json()['results']['style'],'9050')
        self.assertEqual(response.json()['results']['color'],'blue')
        self.assertEqual(response.json()['results']['description'],'hi')
        self.assertEqual(response.json()['results']['retail_price'],'200.00')
        self.assertEqual(response.json()['results']['release_date'],'2016-02-15')
        self.assertEqual(response.json()['results']['image_url'][0],'yaho.jpg')
        self.assertEqual(response.json()['results']['sizes'][0]['size_id'],1)
        self.assertEqual(response.json()['results']['sizes'][0]['size_name'],'1')
        self.assertEqual(response.json()['results']['sizes'][0]['last_sale'],463)
        self.assertEqual(response.json()['results']['sizes'][0]['price_change'],63)
        self.assertEqual(response.json()['results']['sizes'][0]['price_change_percentage'],63)
        self.assertEqual(response.json()['results']['sizes'][0]['lowest_ask'],413)
        self.assertEqual(response.json()['results']['sizes'][0]['highest_bid'],223)
        self.assertEqual(response.json()['results']['sizes'][0]['total_sales'],2)
        self.assertEqual(response.json()['results']['sizes'][0]['price_premium'],131)
        self.assertEqual(response.json()['results']['sizes'][0]['average_sale_price'],431)
        self.assertEqual(response.json()['results']['sizes'][0]['sales_history'][0]['sale_price'],400)
        self.assertEqual(response.json()['results']['sizes'][0]['sales_history'][0]['date_time'],'2021-07-18')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_not_found(self):
        response = client.get('/product/detail/999')
        self.assertEqual(response.json(),
            {
                'message':'PAGE_NOT_FOUND'
            }
        )
        self.assertEqual(response.status_code, 404)