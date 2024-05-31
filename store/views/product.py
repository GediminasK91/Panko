from django.shortcuts import render, get_object_or_404
from store.models.product import Product
from store.models.comment import Comment
from store.forms import CommentForm

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()
    form = CommentForm()
    return render(request, 'product_detail.html', {'product': product, 'comments': comments, 'form': form})
