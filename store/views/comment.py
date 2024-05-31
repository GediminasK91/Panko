from django.shortcuts import render, get_object_or_404, redirect
from store.models.product import Product
from store.models.comment import Comment
from store.forms import CommentForm

def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                # Handle anonymous comments here if needed
                comment.user = None
            comment.save()
            return redirect('product_detail', product_id=product_id)
    return redirect('product_detail', product_id=product_id)
