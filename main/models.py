from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
import random

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.FloatField(default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    image = models.ImageField(upload_to="images/")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password):
        if not email:
            return ValueError("User must have a valid email address")
        if not fullname:
            return ValueError("User's full name must be specified")
        if not password:
            return ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email), fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password):
        if not email:
            return ValueError("Superuser must have a valid email address")
        if not fullname:
            return ValueError("Superuser's full name must be specified")
        if not password:
            return ValueError("Superuser must have a password")        

        user = self.create_user(email, fullname, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    def get_full_name(self):
        return self.fullname

    def __str__(self):
        return self.email

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("delivered", "delivered"),
        ("cancelled", "cancelled")
    )

    def create_new_ref_number():
        not_unique = True
        while not_unique:
            unique_ref = random.randint(1000000000, 9999999999)
            if not Order.objects.filter(order_number=unique_ref):
                not_unique = False
        return str(unique_ref)

    cart_items = models.JSONField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default="pending", choices=STATUS_CHOICES)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(
        max_length = 10,
        blank=False,
        editable=False,
        unique=True,
        default=create_new_ref_number
    )

    def __str__(self) -> str:
        return self.order_number

    class Meta:
        ordering = ["-date_ordered"]

