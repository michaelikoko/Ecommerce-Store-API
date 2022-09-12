import email
from django.shortcuts import render
from main.models import Product, Category, User, Order
from main.serializers import ProductSerializer, CategorySerializer, UserSerializers, OrderSerializer, CustomTokenObtainPairSerializer
from rest_framework import generics, filters, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AllProducts(generics.ListAPIView):
    search_fields = ('name', 'description', 'category__name')
    filter_backends = [filters.SearchFilter,]
    permission_classes = [AllowAny,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LatestProducts(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Product.objects.order_by("-date_created")[:15]
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleProduct(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    lookup_field = "id"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer = self.request.user)

class ResgiterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializers
    queryset = User.objects.all()


