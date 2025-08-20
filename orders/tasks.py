from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def send_new_order_email_to_admin(order_id):
    user = User.objects.filter(is_staff=True).first()
    order = Order.objects.get(pk=order_id)
    print(f"Sending new order email to admin for order {order_id}")

    text_content = render_to_string("emails/order-created.txt", {"order": order})
    html_content = render_to_string("emails/order-created.html", {"order": order})

    msg = EmailMultiAlternatives(
        subject="Order Created",
        body=text_content,
        from_email=user.email,
        to=[order.user.email],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
