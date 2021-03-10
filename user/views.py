import json
import calendar
from datetime import datetime

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg

from user.models    import Portfolio
from product.models import ProductSize
from user.utils     import login_decorator

ORDER_STATUS_HISTORY = 'history'

class PortfolioView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        portfolios = Portfolio.objects.select_related('product_size', 'product_size__product', 'product_size__size')\
                .filter(user=user).prefetch_related('product_size__ask_set')

        portfolio_products = [{
            'name'           : portfolio.product_size.product.name,
            'size'           : portfolio.product_size.size.name,
            'purchase_date'  : portfolio.purchase_date.strftime('%Y/%m/%d'),
            'purchase_price' : int(portfolio.purchase_price),
            'market_value'   : int(portfolio.product_size.product.productsize_set\
                    .filter(ask__order_status__name=ORDER_STATUS_HISTORY)\
                    .annotate(size_avg=Avg('ask__price')).aggregate(total_avg=Avg('size_avg'))['total_avg'])
            } for portfolio in portfolios
        ]

        return JsonResponse({'portfolio':portfolio_products}, status=200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        product_id     = int(data.get('product_id', 0))
        size_id        = int(data.get('size_id', 0))
        purchase_month = data.get('month', None)
        purchase_year  = data.get('year', None)
        purchase_price = data.get('purchase_price', None)
       
        if not (product_id and size_id and purchase_month and purchase_year and purchase_price):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if not ProductSize.objects.filter(product_id=product_id, size_id=size_id).exists():
            return JsonResponse({'message':'PRODUCT_SIZE_DOES_NOT_EXIST'}, status=404)

        product_size = ProductSize.objects.get(product_id=product_id, size_id=size_id)
        last_day     = calendar.monthrange(int(purchase_year), int(purchase_month))[1]

        Portfolio.objects.create(
            user           = user,
            product_size   = product_size,
            purchase_date  = datetime.strptime(f'{purchase_year}-{purchase_month}-{last_day}', '%Y-%m-%d'),
            purchase_price = purchase_price
        )

        return JsonResponse({'message':'SUCCESS'}, status=201)


