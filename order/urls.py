from django.urls import path, include

from order.views import SellView,BuyView

urlpatterns = [
        path('/sell/<int:product_id>', SellView.as_view()), 
        path('/buy/<int:product_id>', BuyView.as_view()),
]

