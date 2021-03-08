import json
from datetime import datetime, timedelta

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from user.models    import ShippingInformation
from product.models import ProductSize
from order.models   import Bid, OrderStatus, Order
from user.utils     import login_decorator

ORDER_STATUS_CURRENT = 'current'
ORDER_STATUS_PENDING = 'pending'
ORDER_NUMBER_LENGTH  = 5

class BuyView(View):
    @login_decorator
    def get(self, request, product_id):
        size_id = request.GET.get('size', None)
        user    = request.user

        if not ProductSize.objects.filter(product_id=product_id, size_id=size_id).exists():
            return JsonResponse({'message':'PRODUCT_SIZE_DOES_NOT_EXIST'}, status=404)

        ProductSize.objects.select_related('product', 'size').prefetch_related('ask_set', 'bid_set', 'product__image_set')
        
        product_size = ProductSize.objects.get(product_id=product_id, size_id=size_id)
        highest_bid  = product_size.bid_set.filter(order_status__name=ORDER_STATUS_CURRENT).order_by('-price').first()
        lowest_ask   = product_size.ask_set.filter(order_status__name=ORDER_STATUS_CURRENT).order_by('price').first()

        product_detail = {
            'id'         : product_size.id,
            'name'       : product_size.product.name,
            'highestBid' : highest_bid.price if highest_bid else 0,
            'lowestAsk'  : lowest_ask.price if lowest_ask else 0,
            'size'       : product_size.size.name,
            'image'      : product_size.product.image_set.first().image_url,
        }

        shipping_information = ShippingInformation.objects.filter(user=user).last()
        shipping_information_detail = {
            'name'             : shipping_information.name if shipping_information else None,
            'country'          : shipping_information.country if shipping_information else None,
            'primaryAddress'   : shipping_information.primary_address if shipping_information else None,
            'secondaryAddress' : shipping_information.secondary_address if shipping_information else None,
            'city'             : shipping_information.city if shipping_information else None,
            'state'            : shipping_information.state if shipping_information else None,
            'postalCode'       : shipping_information.postal_code if shipping_information else None,
            'phoneNumber'      : shipping_information.phone_number if shipping_information else None,
        }
       
        return JsonResponse({'data': {'product' : product_detail, 'shippingInfo' : shipping_information_detail}}, status=200)
    
    @login_decorator
    def post(self, request, product_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            size_id = request.GET.get('size', None)

            if not ProductSize.objects.filter(product_id=product_id, size_id=size_id).exists():
                return JsonResponse({'message':'PRODUCT_SIZE_DOES_NOT_EXIST'}, status=404)

            is_bid            = data.get('isBid', None)
            price             = data.get('price', None)
            name              = data.get('name', None)
            country           = data.get('country', None)
            primary_address   = data.get('primaryAddress', None)
            secondary_address = data.get('secondaryAddress', None)
            city              = data.get('city', None)
            state             = data.get('state', None)
            postal_code       = data.get('postalCode', None)
            phone_number      = data.get('phoneNumber', None)
            expiration_date   = data.get('expirationDate', None)
            total_price       = data.get('totalPrice', None)

            if not is_bid:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            if not (is_bid == '1' or is_bid == '0'):
                return JsonResponse({'message':'INVALID_VALUE'}, status=400)
            
            if not (name and country and primary_address and city and postal_code and phone_number and price):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            product_size = ProductSize.objects.get(product_id=product_id, size_id=size_id)
            
            with transaction.atomic():
                shipping_information, created = ShippingInformation.objects.get_or_create(
                    user              = user,
                    name              = name,
                    country           = country,
                    primary_address   = primary_address,
                    secondary_address = secondary_address,
                    city              = city,
                    state             = state,
                    postal_code       = postal_code,
                    phone_number      = phone_number
                )

                order_status_current = OrderStatus.objects.get(name=ORDER_STATUS_CURRENT)
                order_status_pending = OrderStatus.objects.get(name=ORDER_STATUS_PENDING)
                
                if bool(int(is_bid)):
                    if not expiration_date:
                        raise KeyError
                    
                    Bid.objects.create(
                        user                 = user,
                        product_size         = product_size,
                        price                = price,
                        expiration_date      = datetime.now() + timedelta(days=int(expiration_date)),
                        order_status         = order_status_current,
                        shipping_information = shipping_information
                    )

                    return JsonResponse({'message':'SUCCESS'}, status=201)
                
                if not total_price:
                    raise KeyError

                bid = Bid.objects.create(
                    user                 = user,
                    product_size         = product_size,
                    price                = price,
                    order_status         = order_status_pending,
                    matched_at           = datetime.now(),
                    total_price          = total_price,
                    shipping_information = shipping_information
                )

                bid.order_number = datetime.now().strftime('B' + '%y%m%d' + str(bid.id).zfill(ORDER_NUMBER_LENGTH))
                bid.save()
                
                if not product_size.ask_set.filter(price=price, order_status__name=ORDER_STATUS_CURRENT).exists():
                    raise ProductSize.DoesNotExist

                lowest_ask  = product_size.ask_set.filter(price=price,  order_status__name=ORDER_STATUS_CURRENT).order_by('created_at').first()

                lowest_ask.order_status = order_status_pending
                lowest_ask.matched_at   = datetime.now()
                lowest_ask.total_price  = total_price
                lowest_ask.order_number = datetime.now().strftime('A' + '%y%m%d' + str(lowest_ask.id).zfill(ORDER_NUMBER_LENGTH))
                lowest_ask.save()

                Order.objects.create(bid=bid, ask=lowest_ask)
                
                return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ProductSize.DoesNotExist:
            return JsonResponse({'message':'ASK_DOES_NOT_EXIST'}, status=404)

