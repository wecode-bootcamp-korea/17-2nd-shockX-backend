from django.urls import path
from .views import PortfolioView, KakaoSocialLogin

urlpatterns = [
        path('/kakao', KakaoSocialLogin.as_view()),        
        path('/portfolio', PortfolioView.as_view()),
]
