from django.conf import global_settings
from django.db import models

ORDER_STATES = (
    ("P", "Pending"),
    ("C", "Completed"),
    ("D", "Cancelled"),
)


class Order(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    state = models.CharField(max_length=1, choices=ORDER_STATES, default="P")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        is_new = self.pk is None
        existing_item = self.order.item_set.filter(product=self.product).first()
        has_existing_item = existing_item is not None

        if is_new and has_existing_item:
            existing_item.quantity += 1
            return existing_item.save()

        result = super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

        total = sum(
            [item.quantity * item.product.price for item in self.order.item_set.all()]
        )

        self.order.total = total
        self.order.save()

        return result

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
