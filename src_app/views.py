from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.paginator import Paginator
import json
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Order


def home(request):
    context = {}

    verses = Audio.objects.filter(kind='few_verses')[:6]
    surahs = Audio.objects.filter(kind='surah')[:6]
    reciters = Reciter.objects.all()[0:6]
    books = Book.objects.all()[0:6]
    context['paypal_client_id'] = settings.PAYPAL_CLIENT_ID
    context['verses'] = verses
    context['surahs'] = surahs
    context['books'] = books
    context['reciters'] = reciters

    return render(request, 'index.html', context)


def verses(request):
    context = {}
    all_audios = None
    classification = request.GET.get('classi')
    print(classification)
    
    if classification == 'male':
        all_audios = Audio.objects.filter(kind='few_verses', reciter__gender='Male')
    elif classification == 'female':
        all_audios = Audio.objects.filter(kind='few_verses', reciter__gender='Female')
    else:
        all_audios = Audio.objects.filter(kind='few_verses')

    paginator = Paginator(all_audios, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['audios'] = page_obj
    context['gender'] = classification
    return render(request, 'verses.html', context)


def surahs(request):
    context = {}
    all_audios = None
    classification = request.GET.get('classi')
    print(classification)
    
    if classification == 'male':
        all_audios = Audio.objects.filter(kind='surah', reciter__gender='Male').order_by('chapter_number')
    elif classification == 'female':
        all_audios = Audio.objects.filter(kind='surah', reciter__gender='Female').order_by('chapter_number')
    else:
        all_audios = Audio.objects.filter(kind='surah').order_by('chapter_number')

    paginator = Paginator(all_audios, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['audios'] = page_obj
    context['gender'] = classification
    return render(request, 'surahs.html', context)


def listen(request):

    context = {}

    audio_que = request.GET.get('audio_que')
    if audio_que:
        audio = Audio.objects.get(title=audio_que)
        context['audio'] = audio
    return render(request, 'listen.html', context)

def books(request):
    context = {}

    books = Book.objects.all()
    paginator = Paginator(books, 30)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['books'] = page_obj

    return render(request, 'books.html', context)


def order(request, book_id):
    context = {}

    if book_id:
        book_id = int(book_id)
        book = Book.objects.get(id=book_id)
        context['book'] = book

    if request.method == 'POST':
        book_id = request.POST.get('book-id')
        if book_id:
            quantity = request.POST.get('quantity')
            if quantity:
                quantity = int(quantity)
                book_id = int(book_id)
                book = Book.objects.get(id=book_id)
                address = request.POST.get('address')
                contact = request.POST.get('contact')
                email = request.POST.get('email')
                payment_method = request.POST.get('payment-method')
                price = quantity * book.price

                if address and contact and quantity and payment_method:
                    new_order = Order.objects.create(
                        book=book,
                        address=address,
                        quantity=quantity,
                        payment_method=payment_method,
                        total_price=price,
                        contact=contact,
                        email=email
                    )
                    new_order.save()

                    if payment_method == 'Paypal':
                        return redirect(reverse('paypal-checkout') + f'?order-id={new_order.id}')
                    if payment_method == 'Cash on delivery':
                        # Implement sending email feature here.
                        pass
    return render(request, 'order.html', context)

def donate(request):
    context = {}
    context['paypal_client_id'] = settings.PAYPAL_CLIENT_ID
    return render(request, 'donate.html', context)


def paypal_checkout(request):

    order_id = request.GET.get('order-id')
    if order_id:
        order = Order.objects.get(id=order_id)
    if not order_id:
        return redirect('homepage')
    return render(request, 'paypal_checkout.html', { 'order':order, 'order_id': order_id, 'paypal_client_id':settings.PAYPAL_CLIENT_ID, 'order':order})

def checkout_complete(request):

    message = None

    if request.method == 'POST':
        request_body = json.loads(request.body)
        order_id = request_body.get('orderId')
        paypal_order_id = request_body.get('paypalOrderId')
        if order_id:
            order_id = int(order_id)
            order = Order.objects.get(id=order_id)
            order.payment_done = True
            order.save()
            message = f"Payment Successful. Your Order Id is {order.id}"
        else:
            message = "Something went wrong"

    return render(request, 'paypal_checkout.html', {'order_id': order_id, 'order':order, 'message':message})


def get_audio(request):

    audio = None 
    message = None 
    print(request)
    audio_id = request.GET.get('audio_id')
    if audio_id:
        audio_id = int(audio_id)
        audio = Audio.objects.filter(id=audio_id).values()
        audio = list(audio)
        audio = audio[0]
        message = "Success"

    return JsonResponse({'message':message, 'audio':audio})


def order_placed(request):
    try:
        request_body = json.loads(request.body)

        order_id = request_body.get('orderId')
        if order_id:
            order_id = int(order_id)
        order = Order.objects.get(id=order_id)
        order.payment_done = True
        order.paypal_transaction_id = request_body.get('paypalOrderId')
        order.save()

        customer_email = order.customer.email
        subject = 'Order Confirmation'
        message = f'Your order with order ID {order_id} has been placed successfully.'
        from_email = 'welcome.noorulquraan@gmail.com'

        send_mail(subject, message, from_email, [customer_email])

        # Send email to welcome.noorulquraan@gmail.com
        send_mail(subject, f'You have received an order from {order.email} for Book {order.book.title}. <br />Total Price: {order.total_price}', from_email, ['welcome.noorulquraan@gmail.com'])

        return JsonResponse({'message': 'Order Placed Successfully'})
    except Exception as e:
        print(e)
        return JsonResponse({'message': str(e)})



def reciters(request):
    context = {}

    reciters = Reciter.objects.all()
    paginator = Paginator(reciters, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['reciters'] = page_obj

    return render(request, 'reciters.html', context)

def reciter(request):
    context = {}

    reciter_id = request.GET.get('reciter-id')
    if reciter_id:
        reciter_id = int(reciter_id)
    else:
        return JsonResponse({'Error Message':'Bad Request'})
    reciter = Reciter.objects.get(id=reciter_id)
    context['reciter'] = reciter
    audios = Audio.objects.filter(reciter=reciter)

    paginator = Paginator(audios, 1)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context['audios'] = page_obj

    return render(request, 'reciter.html', context)


def search(request):
    context = {}
    query = request.GET.get('query')
    
    classification = request.GET.get('classi')
    if query:
        all_audios = Audio.objects.filter(title__icontains=query)
        context['audios'] = all_audios

        if classification == 'male':
                all_audios = Audio.objects.filter(title__icontains=query, reciter__gender='Male')
        elif classification == 'female':
                all_audios = Audio.objects.filter(title__icontains=query, reciter__gender='Female')
        else:
                all_audios = Audio.objects.filter(title__icontains=query)

        paginator = Paginator(all_audios, 30)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        context['audios'] = page_obj
        context['query'] = query
        context['gender'] = classification
    else:
        context['message'] = 'Search Query was not provided'

    return render(request, 'search.html', context)


def about_us(request):

    return render(request, 'about.html')