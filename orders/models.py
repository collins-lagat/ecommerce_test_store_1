from django.db import models
from django.conf import global_settings

ORDER_STATES = (
    ("P", "Pending"),
    ("C", "Completed"),
    ("D", "Cancelled"),
)


class Order(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    state = models.CharField(max_length=1, choices=ORDER_STATES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.pk is not None:
            total = sum(
                [item.quantity * item.product.price for item in self.item_set.all()]
            )
            self.total = total
        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


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
        **kwargs,
    ):
        item = super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

        found = self.order.item_set.filter(product=self.product).first()
        if found and not kwargs.get("skip_found_check", False):
            found.quantity += self.quantity
            found.save(skip_found_check=True)
            return found

        total = sum(
            [item.quantity * item.product.price for item in self.order.item_set.all()]
        )

        total += self.quantity * self.product.price

        self.order.total = total
        self.order.save()

        return item

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
