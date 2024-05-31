# store/urls.py
from django.urls import path
from .views.home import Index, store
from .views.signup import Signup, Activate
from .views.login import Login, logout
from .views.cart import Cart, update_cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .middlewares.auth import auth_middleware
from .views import search, product
from .views.comment import add_comment

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('store', store, name='store'),
    path('register/', Signup.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name='activate'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('update_cart', update_cart, name='update_cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('search/', search.search, name='search'),
    path('product/<int:product_id>/', product.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_comment/', add_comment, name='add_comment'),
]
