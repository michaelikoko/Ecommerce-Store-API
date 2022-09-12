from dataclasses import field
from main.models import Product, Category, User, Order
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'fullname': self.user.fullname})
        data.update({"email": self.user.email})
        return data

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(read_only=True, slug_field="email")
    class Meta:
        model = Order
        fields = ("cart_items", "cost", "customer", "status", "order_number", "date_ordered")

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only = True, slug_field="name")
    class Meta:
        model = Product
        fields = "__all__" 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all())],
        allow_blank=False,
        max_length=150
        )

    fullname = serializers.CharField(
        allow_blank = False,
        trim_whitespace = True,
        max_length=150

    )

    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
        )

    class Meta:
        model = User
        fields = ["email", "fullname", "password"]
        read_only_field = ['is_active', 'created', 'updated']

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializers, self).create(validated_data)