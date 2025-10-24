from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    provider = models.CharField(max_length=100, default='hubtel')
    provider_reference = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    
    # Hubtel specific fields
    checkout_url = models.URLField(max_length=500, blank=True)
    checkout_token = models.CharField(max_length=100, blank=True)
    response_code = models.CharField(max_length=10, blank=True)
    response_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status} - Order {self.order_id}"

    class Meta:
        ordering = ['-created_at']
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.provider} - {self.status}"
