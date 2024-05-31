from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models.product import Product
from store.models.category import Category
from django.views import View
from django.contrib import messages

class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                        messages.success(request, 'Removed from cart')
                    else:
                        cart[product] = quantity - 1
                        messages.success(request, 'Reduced quantity')
                else:
                    cart[product] = quantity + 1
                    messages.success(request, f'Added {Product.objects.get(id=product).name} to cart')
            else:
                cart[product] = 1
                messages.success(request, f'Added {Product.objects.get(id=product).name} to cart')
        else:
            cart = {}
            cart[product] = 1
            messages.success(request, f'Added {Product.objects.get(id=product).name} to cart')

        request.session['cart'] = cart
        return redirect('home')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {
        'products': products,
        'categories': categories
    }

    return render(request, 'index.html', data)
