from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men', 'Мужчинам'),
        ('women', 'Женщинам'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True)

    def str(self):
        return self.name
