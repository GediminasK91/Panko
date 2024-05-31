from django.shortcuts import render, redirect
from store.models.product import Product
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

class Cart(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return render(request, 'cart.html', {'products': []})
        
        ids = list(cart.keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})

@login_required(login_url='login')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        remove_all = request.POST.get('remove_all')
        cart = request.session.get('cart', {})

        if product_id:
            quantity = cart.get(product_id, 0)
            if remove:
                if quantity > 1:
                    cart[product_id] = quantity - 1
                    messages.success(request, f'Reduced quantity of {Product.objects.get(id=product_id).name}')
                else:
                    cart.pop(product_id, None)
                    messages.success(request, f'Removed {Product.objects.get(id=product_id).name} from cart')
            elif remove_all:
                cart.pop(product_id, None)
                messages.success(request, f'Removed {Product.objects.get(id=product_id).name} from cart')
            else:
                cart[product_id] = quantity + 1
                messages.success(request, f'Added {Product.objects.get(id=product_id).name} to cart')

        request.session['cart'] = cart

    return redirect('cart')
