from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product  # Предположим, что Product находится в app catalog

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40,null=True)
    quantity = models.PositiveIntegerField(default=1)

    def str(self):
        return f"{self.product.name} x {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def str(self):
        return f"{self.product.name} x {self.quantity}"
