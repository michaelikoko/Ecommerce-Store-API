from django.urls import path
from main.views import AllProducts, LatestProducts, CategoryList, SingleProduct, ResgiterUserView, OrderView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'main'
urlpatterns = [
    path("all_products/", AllProducts.as_view()),
    path("latest_products/", LatestProducts.as_view()),
    path("categories/", CategoryList.as_view()),
    path("single_product/<int:id>", SingleProduct.as_view()),
    path("orders/", OrderView.as_view()),
    path("token/obtain/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("register/", ResgiterUserView.as_view()),
]