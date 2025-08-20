from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        result = super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

        categories = [self.category]
        current_category = self.category
        while current_category.parent is not None:
            categories.append(self.category.parent)
            current_category = self.category.parent

        for category in categories:
            prices = [product.price for product in category.get_all_products()]
            category.average_price = sum(prices) / len(prices)
            category.save()

        return result


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_all_products(self):
        return self._get_products_for_category(self)

    def _get_products_for_category(self, category):
        products = Product.objects.filter(category=category)

        for child in category.children.all():
            products |= self._get_products_for_category(child)

        return products

    def __str__(self):
        return self.name
