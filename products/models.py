from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
