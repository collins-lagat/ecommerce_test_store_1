from orders.models import Order


def load_cart(request):
    if not request.user.is_authenticated:
        return {"cart_item_count": 0}

    order = (
        Order.objects.filter(user=request.user, state="P")
        .order_by("-created_at")
        .first()
    )
    count = sum([item.quantity for item in order.item_set.all()])
    return {"cart_item_count": count}
