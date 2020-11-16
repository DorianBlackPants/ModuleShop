from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class UserProfile(AbstractUser):
    funds = models.FloatField(blank=True, null=True, default=1000.00)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'MyUser'


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='media', default='default.png')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.id)])


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)

    def get_total_item_price(self):
        return self.amount * self.item.price

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])


class Refund(models.Model):
    purchase = models.ForeignKey(Order, on_delete=models.CASCADE)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    request_time = models.DateTimeField(auto_now_add=True)
