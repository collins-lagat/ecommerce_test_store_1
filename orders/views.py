from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from orders.models import Item, Order
from orders.serializers import ItemSerializer, OrderSerializer
from orders.tasks import (
    send_new_order_email_to_admin,
    send_order_confirmation_SMS_to_customer,
)


def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "order-single.html", {"order": order})


def checkout(request):
    cart_items = []
    cart_total = 0

    try:
        order = (
            Order.objects.prefetch_related("item_set")
            .filter(state="P", user=request.user)
            .order_by("-created_at")
            .get()
        )
    except Order.DoesNotExist:
        return render(
            request,
            "checkout.html",
            {"cart_items": cart_items, "cart_total": cart_total},
        )

    cart_items = order.item_set.all()

    return render(
        request, "checkout.html", {"cart_items": cart_items, "cart_total": order.total}
    )


class CartViewSet(viewsets.GenericViewSet):
    queryset = (
        Order.objects.prefetch_related("item_set")
        .filter(state="P")
        .order_by("-created_at")
    )
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {
            "user": self.request.user,
        }

        try:
            order = get_object_or_404(queryset, **filter_kwargs)
        except queryset.model.MultipleObjectsReturned:
            for o in queryset.filter(**filter_kwargs)[1:]:
                o.state = "D"
                o.cancelled_at = timezone.now()
                o.save()
            order = get_object_or_404(queryset, **filter_kwargs)

        return order

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = "D"
        instance.cancelled_at = timezone.now()
        instance.save()
        return Response(status=204)

    @action(detail=False, methods=["post"])
    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = "C"
        instance.completed_at = timezone.now()
        instance.save()
        send_new_order_email_to_admin.delay_on_commit(instance.id)
        send_order_confirmation_SMS_to_customer.delay_on_commit(instance.id)
        return Response(status=200)


class CartItemViewSet(viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def add(self, request, *args, **kwargs):
        order_queryset = Order.objects.filter(
            user=self.request.user, state="P"
        ).order_by("-created_at")
        try:
            order = order_queryset.get()
        except Order.DoesNotExist:
            order = Order(user=self.request.user)
            order.save()
        except Order.MultipleObjectsReturned:
            for o in order_queryset.all()[1:]:
                o.state = "D"
                o.cancelled_at = timezone.now()
                o.save()
            order = order_queryset.get()

        data = request.data
        data["order"] = order.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(detail=True, methods=["delete"])
    def remove(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
