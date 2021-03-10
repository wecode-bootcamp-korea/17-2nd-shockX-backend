from django.urls import path, include

from order.views import SellView, BuyView, BuyStatusView, SellStatusView

urlpatterns = [
    path('/buy/<int:product_id>', BuyView.as_view()),
    path('/sell/<int:product_id>', SellView.as_view()), 
    path('/account/buying', BuyStatusView.as_view()),
    path('/account/selling', SellStatusView.as_view()),
    ]
