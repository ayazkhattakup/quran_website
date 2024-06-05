from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('verses/', views.verses, name='verses'),
    path('surahs/', views.surahs, name='surahs'),
    path('listen/', views.listen, name='listen'),
    path('products/', views.books, name='books'),
    path('place-order/<book_id>', views.order, name='order'),
    path('donate/', views.donate, name='donate'),
    path('paypal-checkout/', views.paypal_checkout, name='paypal-checkout'),
    path('payment-done/', views.checkout_complete, name='payment-done'),
    path('get-audio/', views.get_audio, name='get-audio'),
    path('order-placed/', views.order_placed, name='order-placed'),
    path('reciter/', views.reciter, name='reciter'),
    path('reciters/', views.reciters, name='reciters'),
    path('search/', views.search, name='search'),
]