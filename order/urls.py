from django.urls import path

from .views import BuyView

urlpatterns = [
    path('/buy/<int:product_id>', BuyView.as_view()),
]
