# store/views/checkout.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from store.models.product import Product
from store.models.orders import Order
from store.models.customer import Customer

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        order_details = []
        for product in products:
            quantity = cart.get(str(product.id))
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=quantity,
            )
            order.save()
            order_details.append(f'{product.name} - {quantity} x {product.price} = {quantity * product.price}')

        # Send confirmation email
        customer_email = Customer.objects.get(id=customer).email
        order_details_str = '\n'.join(order_details)
        email_body = (
            f'Thank you for your purchase. Your order for {len(products)} items has been received and is being processed.\n\n'
            f'Order Details:\n{order_details_str}\n\n'
            f'Delivery Address: {address}\nPhone: {phone}'
        )
        send_mail(
            'Order Confirmation',
            email_body,
            settings.EMAIL_HOST_USER,
            [customer_email],
            fail_silently=False,
        )

        # Clear the cart
        request.session['cart'] = {}

        # Respond with JSON for the success message
        return redirect('home')

