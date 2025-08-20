import africastalking
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def send_new_order_email_to_admin(order_id):
    user = User.objects.filter(is_staff=True).first()
    order = Order.objects.get(pk=order_id)

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


@shared_task
def send_order_confirmation_SMS_to_customer(order_id):
    africastalking.initialize(
        settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY
    )
    sms = africastalking.SMS
    order = Order.objects.get(pk=order_id)
    sender = settings.AFRICASTALKING_SHORTCODE
    customer = order.user
    recepients = [customer.phone_number]
    message = f"Your order has been placed. Your order ID is {order.id}"
    try:
        response = sms.send(message, recepients, sender)
        print(response)
    except Exception as e:
        print("Encountered an error while sending: %s" % str(e))
