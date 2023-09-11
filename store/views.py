from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm, User)
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .serializers import  UserSerializer,ArticleSerializer, CounterSerializer,CommentsSerializer,CheckoutSerializer
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,Sum,F
from django.http import QueryDict

from random import seed
from random import sample, choice

import json

from itertools import chain
from operator import attrgetter

from datetime import datetime, timedelta

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.utils import translation
from .forms import *
from numpy import random
import re

from io import BytesIO
from django.core.files.base import ContentFile
from django.views.generic import TemplateView

from django import template
import base64
import requests
from django.views.generic.base import View
from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash



def change_currency_symbol(request, new_currency_symbol):
    
    
    # You may optionally store the new currency symbol in the user's session or database for future use
    # ...
    response  =redirect(request.META.get('HTTP_REFERER'), new_currency_symbol)
    expiration = datetime.now() + timedelta(days=360)
    response.set_cookie(settings.DEFAULT_CURRENCY_CODE, new_currency_symbol,expires=expiration)
    #response.set_cookie('currency_code', new_currency_symbol)
    settings.CURRENCIES_RATES['USD']=2
    
    



    
    return response
   

def set_language(request):
    language = request.POST.get('language', settings.LANGUAGE_CODE)
    translation.activate(language)
    
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    request.session.save()

    return redirect('accounts:home')

class ActivateLanguageView(View):
    language_code = ''
    redirect_to   = ''

    def get(self, request, *args, **kwargs):
        self.redirect_to   = request.META.get('HTTP_REFERER')
        self.language_code = kwargs.get('language_code')
        
        
        translation.activate(self.language_code)

        request.session[translation.LANGUAGE_SESSION_KEY] = self.language_code
        
        self.line_redirect = str(self.redirect_to).split("/")
        
        response =redirect(self.redirect_to, self.language_code)
        
        expiration = datetime.now() + timedelta(days=360)
        
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, self.language_code,expires=expiration)
        if self.language_code=='hy':
            response.set_cookie(settings.DEFAULT_CURRENCY_CODE, "ARM",expires=expiration)
        elif self.language_code=='ru':
            response.set_cookie(settings.DEFAULT_CURRENCY_CODE, "RUR",expires=expiration)
        else:
            response.set_cookie(settings.DEFAULT_CURRENCY_CODE, "ENG",expires=expiration)
        

        

        
        
        

        return response
def home(request):
    if not request.method == 'POST':



        try:
            visit = models.Visit.objects.get()
        except models.Visit.DoesNotExist:
            visit = models.Visit.objects.create(visits=0, visits_last=0)

        visit.visits = F('visits') + 1
        visit.visits_last = F('visits_last') + 1

        time_threshold = timezone.now() - timedelta(days=1)
        visit_one_day = models.Visit.objects.filter(timestamp__lte=time_threshold)

        if visit_one_day.exists():
            visit.timestamp = timezone.now()
            visit.visits_one_day = visit.visits_last
            visit.visits_last = 0

        visit.save()
        

            


    
    products = models.products.objects.filter(active = True).only('id', 'name_ru', 'name_am', 'name_en', 'price', 'price_pcs','price_size', 'sale_price_size','sale_price_pcs', 'counter_props', 'avatar_p','sale_price', 'sale').order_by('-created_at')
    home_slides = models.home_slide.objects.all()
    
    

    
    brands = models.Brand.objects.all()

    
    number_of_item = 12
    paginatorr = Paginator(products, number_of_item)
    
    
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range
    

    if request.method == 'POST':
        
        pag_ajax = paginatorr
        page_n = request.POST.get('page_n', None)
        results = pag_ajax.page(page_n).object_list.filter()
        statuss_se=ArticleSerializer(results, many=True)

        
        if (int(page_n)-2>=0):
            page_range = page_range[int(page_n)-2:int(page_n)+2]
        else:
            page_range = page_range[0:int(page_n)+3]
        
        
        
        return JsonResponse({"results":statuss_se.data, "page_range":list(page_range)})
    return render(request, "template_rus/home.html", {"brands":brands, "home_slides":home_slides,'paginatorr':paginatorr,'products':first_page,'page_range':page_range})

def pagination_ajax(request):
    my_model = models.products.objects.filter()
    number_of_item = 5
    paginatorr = Paginator(my_model, number_of_item)
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range

    context = {
        'paginatorr':paginatorr,
        'first_page':first_page,
        'page_range':page_range
    }

    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)
        results = list(paginatorr.page(page_n).object_list.values('id', 'title'))
        return JsonResponse({"results":results})


    return render(request, 'index.html',context)
def add_order(request):
    products = request.user.profile.product_cart.all()
    profile = get_object_or_404(models.Profile,pk=request.user.profile.pk ) 
    profile.checkout_products_list.clear()

    for index,product_cart in enumerate(products):
        cart_pk = int(request.POST.get(f'cart_pk{index}'))
        
        if int(product_cart.pk) != cart_pk:
            profile.checkout_products_list.clear()
            profile.save()
            break
        
        cart_count = int(re.findall(r'\d+', request.POST.get(f'count{index}'))[0])

        

        if product_cart.indicator=="size":
            
            count = product_cart.count_size
            if (int(count)!=int(cart_count)):
                count = cart_count
            
            


            if product_cart.product.sale_price_size:
                price = (count/product_cart.product.min_size)*product_cart.product.sale_price_size
            else:
                price = (count/product_cart.product.min_size)*product_cart.product.price_size

            

        elif product_cart.indicator=="counter":
            price=None
            

            for j in  product_cart.product.counter_props.all().order_by('counter_prop'):
                if (int(product_cart.count) >= int(j.counter_prop)):
                    price = float(j.counter_price)
                    if(j.counter_price_sale):
                        price = float(j.counter_price_sale)
                    else:
                        price = float(j.counter_price)
            count = product_cart.count
            if int(cart_count) != int(count):
                count = cart_count

                    
            
            price = count*price
            
        elif product_cart.indicator=="count":
            count = product_cart.count
            if int(cart_count) != int(count):
                count = cart_count
            if product_cart.product.sale_price:

                price = count*product_cart.product.sale_price
            else:
                price = count*product_cart.product.price
            
        elif product_cart.indicator=="size_pcs":
            count = product_cart.count
            if int(cart_count) != int(count):
                count = cart_count
            if product_cart.product.sale_price_pcs:
                price = count*product_cart.product.sale_price_pcs
            else:
                price = count*product_cart.product.price_pcs
            
            

            #orders = models.products_Order.objects.create(product=product_cart.product, customer=request.user.profile,count_size=count,price=price)
        else:
            pass
        

        if product_cart.indicator=="size":
            orders = models.products_Order.objects.create(product=product_cart.product, customer=request.user.profile,count_size=count,price=price,indicator=product_cart.indicator, name_ru = product_cart.product.name_ru, name_am = product_cart.product.name_am, name_en = product_cart.product.name_am, avatar_p = product_cart.product.avatar_p)
        else:
            orders = models.products_Order.objects.create(product=product_cart.product, customer=request.user.profile,count=count,price=price,indicator=product_cart.indicator, name_ru = product_cart.product.name_ru, name_am = product_cart.product.name_am, name_en = product_cart.product.name_am, avatar_p = product_cart.product.avatar_p)
        profile.checkout_products_list.add(orders)
    profile.save()
    return JsonResponse("data", safe=False)

def shop_product_detail(request):
    return render(request, "template_rus/product_page.html")

def checkout(request):
    profile = get_object_or_404(models.Profile, pk=request.user.profile.pk)
    order_products = profile.checkout_products_list.filter()
    price_total = sum( int(product.product.sale_price)*product.count if product.product.sale > 0 else int(product.product.price)*product.count  for product in order_products)
    shipping_address = order_products[0].shipping_address
    user_info = models.my_contacts_info.objects.filter(profile=request.user.profile)
    zone_countries = models.zone_countries.objects.all()
    return render(
        request,
        "template_rus/checkout.html",
        {
            "profile": profile,
            "order_products": order_products,
            "shipping_address": shipping_address,
            "price_total": price_total,
            "user_info": user_info,
            "zone_countries": zone_countries,
        },
    )



def delete_product(request):
    pk = request.POST.get("pk")
    models.products.objects.filter(pk=pk).delete()
    data={"success":1}
    return JsonResponse(data, safe=False)
def orders(request):
    profile = request.user.profile
    checkouts = models.checkout_products.objects.filter(profile = profile).only('status', 'assembled', 'order_id', 'delivery_check','price', 'id').order_by('-date_ordered')
    page = request.GET.get('page', 1)
    paginator = Paginator(checkouts, 2)
    Visit = models.Visit.objects.filter()
    
    


    try:
        checkouts = paginator.page(page)
    except PageNotAnInteger:
        checkouts = paginator.page(1)
    except EmptyPage:
        checkouts = paginator.page(paginator.num_pages)
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    template_name = f"template_arm/my_account_scroll.html" if lang == "hy" else f"template{'_eng' if lang == 'en' else '_rus'}/my_account_scroll.html"

    return render(
        request,
        template_name,
        {
            "profile": profile,
            
            "checkouts": checkouts,
        },
    )
def my_account(request):
    profile = request.user.profile

    shipping_address = models.shipping_address.objects.filter(profile=profile)
    Visit = models.Visit.objects.filter()
    Profiles_count = models.Profile.objects.filter().count()
    
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if not request.user.is_superuser:
        template_name = f"template_arm/my_account.html" if lang == "hy" else f"template{'_eng' if lang == 'en' else '_rus'}/my_account.html"
    else:
        template_name = f"template_rus/my_account.html" 

    return render(
        request,
        template_name,
        {
            "profile": profile,
            "Visit": Visit,
            "shipping_address": shipping_address,
            "Profiles_count":Profiles_count,
            
        },
    )

def send_recovery_via_email(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    if not User.objects.filter(username=username).exists():
            data = {
                "data": "error"
            }
    else:
        user = get_object_or_404(User, username=username)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build the confirmation URL
        current_site = get_current_site(request)
        confirmation_url = f'http://{current_site.domain}/confirm_reset/{uid}/{token}/'

            # Send a confirmation email
        subject = 'Confirm your email'
        message = render_to_string('layouts/email_conf.html', {
            'user': user,
            'confirmation_url': confirmation_url,
        })
            
        recipient_list = [user.profile.email]
        if (str(email) != str(user.profile.email)):
            data = {
            "data": "error"
            }
            return JsonResponse(data, safe=False)

        print(recipient_list)
        plain_message = strip_tags(message)
        print(recipient_list)
        send_mail(
            subject,
            plain_message,
            'boutique.broderie.am@gmail.com',
            recipient_list,
            fail_silently=False,
            html_message=message,
                

        )
            

        data = {
            "data": "confirmation_sent"
        }
    return JsonResponse(data, safe=False)








def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            data = {
                "data": "error"
            }
        else:
            # Create a user with a unique email confirmation token
            user = User.objects.create_user(username, password=password, is_active=False)
            user.profile.first_name = first_name
            user.profile.email = email
            user.profile.last_name = lastname
            user.profile.phone_number = phone
            user.password = password
            user.profile.save()

            # Generate an email confirmation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build the confirmation URL
            current_site = get_current_site(request)
            confirmation_url = f'http://{current_site.domain}/confirm/{uid}/{token}/'

            # Send a confirmation email
            subject = 'Confirm your email'
            message = render_to_string('layouts/email_conf.html', {
                'user': user,
                'confirmation_url': confirmation_url,
            })
            
            recipient_list = [user.profile.email]
            plain_message = strip_tags(message)
            print(recipient_list)
            send_mail(
                subject,
                plain_message,
                'boutique.broderie.am@gmail.com',
                recipient_list,
                fail_silently=False,
                html_message=message,
                

                )
            

            data = {
                "data": "confirmation_sent"
            }

    else:
        data = {
            "data": "error"
        }

    return JsonResponse(data, safe=False)
def new_register_password(request):
    new_password = request.POST.get("new_password")
    print(request.method)
    uid = request.COOKIES.get("user_recovery_id")
    user = User.objects.get(id=uid)
    print(new_password, "new_password", user)
    if new_password is None:
        return JsonResponse({"success":"error"})
    user.set_password(new_password)
    user.save()
    
    a=update_session_auth_hash(request, user)
    
    login(request, user)
    profile = get_object_or_404(models.Profile, user=user)
    profile.password = new_password
    profile.save()
    
    return JsonResponse({"success":"success"})

def confirm_reset_password(request, uidb64, token):
    try:
        # Decode the user ID from base64
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Verify the email confirmation token
        if default_token_generator.check_token(user, token):
            # Activate the user's account
            
            # Optional: Log the user in

            # Display a success message
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been confirmed!')
            response  =redirect('accounts:new_password_page')
            
            response.set_cookie("user_recovery_id", user.id)
            return response  # Redirect to a success page

        else:
            # Token is invalid
            messages.error(request, 'Invalid token. Please try again.')
            return redirect('accounts:sign_in')  # Redirect to login page or another error page

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Handle exceptions if the user ID cannot be decoded or user does not exist
        messages.error(request, 'Invalid token. Please try again.')
        return redirect('accounts:login')  # Redirect to login page or another error page




def confirm_email(request, uidb64, token):
    try:
        # Decode the user ID from base64
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Verify the email confirmation token
        if default_token_generator.check_token(user, token):
            # Activate the user's account
            user.is_active = True
            user.save()
            login(request, user)  # Optional: Log the user in

            # Display a success message
            messages.success(request, 'Your email has been confirmed!')
            return redirect('accounts:home')  # Redirect to a success page

        else:
            # Token is invalid
            messages.error(request, 'Invalid token. Please try again.')
            return redirect('accounts:login')  # Redirect to login page or another error page

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Handle exceptions if the user ID cannot be decoded or user does not exist
        messages.error(request, 'Invalid token. Please try again.')
        return redirect('accounts:login')  # Redirect to login page or another error page

from django.contrib.auth.hashers import check_password
def sign_in(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)
    

    
    
    user = authenticate(username=username, password=password)
    print(user)
    
    if user is not None:
        login(request, user)
        data = {
            "data":1
        }
    else:
        data = {
            "data":0
        }
        # No backend authenticated the credentials


    return JsonResponse(data,safe=False)   

def shop_products(request):
    category_choeses=models.category_choeses.objects.filter(parent = None)
    return  render(request, "template_rus/products_all.html", {"category_choeses":category_choeses})

def shop_products_category(request, categoryid):
    
    for i in models.category_choeses.objects.all():
        print(i.category_id_main)

    try:

        
        category_choeses=get_object_or_404(models.category_choeses, category_id_main=categoryid)

        if len(category_choeses.category_id)>0:
            category_main = get_object_or_404(models.category_choeses, pk=category_choeses.category_id)
        else:

            category_main =category_choeses

        products = models.products.objects.filter(Q(sub_categories=category_choeses) | Q(category_choeses=category_choeses)).filter(active = True)
        category_choeses = models.category_choeses.objects.filter(parent=category_choeses)
        number_of_item = 12
        
        
        
        
        search_text = request.POST.get('search_text')
        
            
        if search_text is not None and search_text != u"":
            



            
            text = re.escape(search_text)
            if request.user.is_superuser:
                products = products.filter(name_ru__iregex = r"(^|\s)%s" % text).exclude().order_by()
            else:
                products = products.filter(Q(name_ru__iregex = r"(^|\s)%s" % text)).exclude().order_by()
            

        paginatorr = Paginator(products, number_of_item)
        
        
        first_page = paginatorr.page(1).object_list
        page_range = paginatorr.page_range

        if request.method == 'POST':

            
            
            if request.POST.get('page_n', None) is  None:
                page_n=1
            else:
                page_n = request.POST.get('page_n', None)
            results = paginatorr.page(page_n).object_list.filter()
            statuss_se=ArticleSerializer(results, many=True)

            
            if (int(page_n)-2>=0):
                page_range = page_range[int(page_n)-2:int(page_n)+2]
            else:
                page_range = page_range[0:int(page_n)+3]
            
            
            
            return JsonResponse({"results":statuss_se.data, "page_range":list(page_range)})
        return  render(request, "template_rus/products_all.html", {"category_choeses":category_choeses, "products":first_page, "category_main":category_main, "page_range":page_range, "categoryid":categoryid})

    except:
        return  redirect("accounts:home")

    
    

    

   
    
def products_of_day(request):
    products = models.products.objects.filter(sale__gt=0,active = True)
    number_of_item = 12
    paginatorr = Paginator(products, number_of_item)

    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range

    

    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)
        results = paginatorr.page(page_n).object_list.filter()
        statuss_se=ArticleSerializer(results, many=True)

        
        if (int(page_n)-2>=0):
            page_range = page_range[int(page_n)-2:int(page_n)+2]
        else:
            page_range = page_range[0:int(page_n)+3]

        return JsonResponse({"results":statuss_se.data, "page_range":list(page_range)})

    return render(request, "template_rus/products_all.html", {"products":first_page,"day_products":True, "page_range":page_range })
def all_brands_product(request):
    Brands = models.Brand.objects.all()
    products = models.products.objects.filter(Brand__in=Brands,active = True)
    number_of_item = 12
    search_text = request.POST.get('search_text')
    
        
    if search_text is not None and search_text != u"":
        



        
        text = re.escape(search_text)
        if request.user.is_superuser:
            products = products.filter(name_ru__iregex = r"(^|\s)%s" % text).exclude().order_by()
        else:
            products = products.filter(Q(name_ru__iregex = r"(^|\s)%s" % text)).exclude().order_by()
            
        
    paginatorr = Paginator(products, number_of_item)

    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range
    
    if request.method == 'POST':
        print(search_text, "search_text")
        if request.POST.get('page_n', None) is  None:
            page_n=1
        else:
            page_n = request.POST.get('page_n', None)
        results = paginatorr.page(page_n).object_list.filter()
        statuss_se=ArticleSerializer(results, many=True)

        
        if (int(page_n)-2>=0):
            page_range = page_range[int(page_n)-2:int(page_n)+2]
        else:
            page_range = page_range[0:int(page_n)+3]
        return JsonResponse({"results":statuss_se.data,  "page_range":list(page_range)})


    return render(request, "template_rus/products_all.html", {"products":first_page,"Brands":True, "page_range":page_range })
def brand_products(request, Brand_id):
    Brand = get_object_or_404(models.Brand, pk=Brand_id)
    products = models.products.objects.filter(Brand=Brand,active = True)
    number_of_item = 12
    search_text = request.POST.get('search_text')
        
    if search_text is not None and search_text != u"":
        



        
        text = re.escape(search_text)
        if request.user.is_superuser:
            products = products.filter(name_ru__iregex = r"(^|\s)%s" % text).exclude().order_by()
        else:
            products = products.filter(Q(name_ru__iregex = r"(^|\s)%s" % text)).exclude().order_by()
            
        
    paginatorr = Paginator(products, number_of_item)

    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range
    

    

    if request.method == 'POST':
        
        if request.POST.get('page_n', None) is  None:
            page_n=1
        else:
            page_n = request.POST.get('page_n', None)
        results = paginatorr.page(page_n).object_list.filter()
        statuss_se=ArticleSerializer(results, many=True)

        
        if (int(page_n)-2>=0):
            page_range = page_range[int(page_n)-2:int(page_n)+2]
        else:
            page_range = page_range[0:int(page_n)+3]
        return JsonResponse({"results":statuss_se.data,  "page_range":list(page_range)})


    return render(request, "template_rus/products_all.html", {"products":first_page,"Brand":Brand, "page_range":page_range })
def new_products(request):
    
    products = models.products.objects.filter(active = True)
    number_of_item = 12
    paginatorr = Paginator(products, number_of_item)
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)
        results = paginatorr.page(page_n).object_list.filter()
        statuss_se=ArticleSerializer(results, many=True)

        
        if (int(page_n)-2>=0):
            page_range = page_range[int(page_n)-2:int(page_n)+2]
        else:
            page_range = page_range[0:int(page_n)+3]
        return JsonResponse({"results":statuss_se.data,  "page_range":list(page_range)})

    return render(request, "template_rus/products_all.html", {"products":first_page, "new_products":True, "page_range":page_range})
def send_email(request):
    checkout = models.checkout_products.objects.filter()
    checkout = checkout[14]


    html_message = render_to_string('layouts/email_template.html',{"checkout":checkout, "request":request})
    email  = "david.hovhannisyan445@gmail.com"
    
    
    
    
    plain_message = strip_tags(html_message)
    send_mail(
        'Ապրանքը վերադարձնելու հայտ',
        plain_message,
        'boutique.broderie.am@gmail.com',
        ["david.hovhannisyan445@gmail.com"],
        fail_silently=False,
        html_message=html_message,
        

        )
def order_detalis(request,pk):
    checkout = get_object_or_404(models.checkout_products, order_id=pk)
    return render(request, "template_rus/order_detalis.html", {"checkout":checkout})
def add_brand(request):
    if request.method=="POST":
        brand_name = request.POST.get("Brand_name")
        brand_picture = request.FILES.get(f'images{0}')
        brand=models.Brand.objects.create(brand=brand_name, brand_picture=brand_picture)
        data = {
            "pk":brand.pk,
            "picture":brand.brand_picture.url
        }

        
        return JsonResponse(data, safe=False)
    barnds = models.Brand.objects.all().order_by("-pk")

    return render(request, "template_rus/add_brand.html", {"barnds":barnds})
def delete_brand(request):
    pk = request.POST.get("pk")
    brand = get_object_or_404(models.Brand, pk=pk)
    brand.delete()
    return JsonResponse("data", safe=False)

def add_images_for_categories(request):
    pk = request.POST.get("pk")
    category_choeses=get_object_or_404(models.category_choeses, pk=pk)
    category_choeses.image = request.FILES.get("image")
    category_choeses.save()
    data = {"success":1}
    return JsonResponse(data, safe=False)

def add_images_for_home_page_slide(request):
    pk = request.POST.get("pk")
    slide_len = request.POST.get("slide_len")
    slide_len_delete = request.POST.get("del_length")
    
    for i in range(0, int(slide_len_delete)):
        
        
        models.home_slide.objects.filter(pk=request.POST.get(f'img_num_del{i}')).delete()
       
    for i in range(0, int(slide_len)):

        
        data = request.FILES.get(f'images{i}')
        
        models.home_slide.objects.create(image=data)
    
    data = {"success":1}
    return JsonResponse(data, safe=False)
def add_price_for_shipping(request):
    Mass_and_money = models.Mass_and_money.objects.filter()

    return render(request, "template_rus/add_shipping_price.html", {"Mass_and_money":Mass_and_money})
def price_of_deliverybox(request):
    price_of_deliverybox = models.price_of_deliverybox.objects.filter()
    return render(request, "template_rus/add_delivery_box_price.html", {"price_of_deliverybox":price_of_deliverybox})
def change_delivery_box_mass(request):

    pk = request.POST.get("pk")
    mass_start = request.POST.get("mass_start")
    mass_end = request.POST.get("mass_end")
    total_mass = request.POST.get("total_mass")
    
    price_of_deliverybox =  get_object_or_404(models.price_of_deliverybox, pk=pk) 
    price_of_deliverybox.mass_start =mass_start
   
    price_of_deliverybox.mass_end=mass_end
    price_of_deliverybox.total_mass=total_mass
   
    price_of_deliverybox.save()
    data = {
    "pk":price_of_deliverybox.pk
    }
    return JsonResponse(data, safe=False)
def add_delivery_box_price(request):
    mass_start = request.POST.get("mass_start")
    mass_end = request.POST.get("mass_end")
    total_mass = request.POST.get("total_mass")
   
    
    price_of_deliverybox = models.price_of_deliverybox.objects.create(mass_start =mass_start, mass_end=mass_end , total_mass=total_mass)
    data = {
    "pk":price_of_deliverybox.pk
    }
    return JsonResponse(data, safe=False)
def add_zones(request):
    zones = models.zone.objects.all()

    return render(request, "template_rus/add_zones.html", {"zones":zones})

def api_add_zones(request):
    countries = request.POST.get("countries")
    zones = request.POST.get("zones")
    print(countries.split(","))
    print(zones)
    zone = models.zone.objects.create(zone_number=int(zones))

    country = ""

    for i in countries.split(","):
        if i[0]==' ':

            country=i[1:]
        else:

            country=i
        zone.zone_countries.add(models.zone_countries.objects.create(country=country))
    zone.save()

    
    return JsonResponse("data", safe=False)
def remove_zones(request):
    pk = request.POST.get("pk")
    models.zone.objects.filter(pk=pk).delete()
    return JsonResponse("data", safe=False)
def change_shipping_price(request):
    pk = request.POST.get("pk")
    mass_start = request.POST.get("mass_start")
    mass_end = request.POST.get("mass_end")
    price = request.POST.get("price")
    select_zones = request.POST.get("select_zones")
    select_type = request.POST.get("select_type")
    zone = get_object_or_404(models.zone, zone_number=int(select_zones))
    Mass_and_money =  get_object_or_404(models.Mass_and_money, pk=pk) 
    Mass_and_money.mass_start =mass_start
    Mass_and_money.type=select_type
    Mass_and_money.mass_end=mass_end
    Mass_and_money.money=price
    Mass_and_money.zones=zone
    Mass_and_money.save()
    data = {
    "pk":Mass_and_money.pk
    }
    return JsonResponse(data, safe=False)

def api_add_shipping_price(request):

    mass_start = request.POST.get("mass_start")
    mass_end = request.POST.get("mass_end")
    price = request.POST.get("price")
    select_zones = request.POST.get("select_zones")
    select_type = request.POST.get("select_type")
    zone = get_object_or_404(models.zone, zone_number=int(select_zones))
    Mass_and_money = models.Mass_and_money.objects.create(mass_start =mass_start,type=select_type, mass_end=mass_end , money=price, zones=zone)
    data = {
    "pk":Mass_and_money.pk
    }
    return JsonResponse(data, safe=False)
def remove_shipping_price(request):
    pk = request.POST.get("pk")

    Mass_and_money = models.Mass_and_money.objects.filter(pk=pk).delete()
    
    return JsonResponse("data", safe=False)

def remove_delivery_box_mass(request):
    pk = request.POST.get("pk")

    price_of_deliverybox = models.price_of_deliverybox.objects.filter(pk=pk).delete()
    
    return JsonResponse("data", safe=False)
def add_slides(request):
    slides = models.home_slide.objects.all()
    
    return render(request, "template_rus/add_slides.html", {"slides":slides, "slides_len":len(slides)})
def check_max_count_product(request):
    pk = request.POST.get("pk")
    size = request.POST.get("size")
    product = get_object_or_404(models.products, pk=pk)
    
    
    if size is not None:
        max_count = int(product.max_size)
    else:
        max_count = int(product.pcs)
    
    data = {
    "max_count":max_count
    }
    return JsonResponse(data, safe=False)
def cart_page(request):
    profile = get_object_or_404(models.Profile, pk=request.user.profile.pk)
    cart_products = profile.product_cart.all()
    sums = 0



    for i in cart_products:
        if i.indicator=="size":
            if i.product.sale_price_size:
                sums+=(i.count_size/i.product.min_size)*i.product.sale_price_size
            else:

                sums+=(i.count_size/i.product.min_size)*i.product.price_size
        elif i.indicator=="counter":
            price=None
            

            for j in  i.product.counter_props.all().order_by('counter_prop'):
                if (int(i.count) >= int(j.counter_prop)):
                    price = float(j.counter_price)
                    if(j.counter_price_sale):
                        price = float(j.counter_price_sale)
                    else:
                        price = float(j.counter_price)

                    
            sums+=i.count*price
            
        elif i.indicator=="size_pcs":
            if i.product.sale_price_pcs:
                sums+=i.count*i.product.sale_price_pcs
            else:

                sums+=i.count*i.product.price_pcs
            
        elif i.indicator=="count":
            if i.product.sale_price:
                sums+=i.count*i.product.sale_price
            else:

                sums+=i.count*i.product.price
            
        else:
            continue

        
        

    
    count = cart_products.count()
    max_per = models.max_cart_price.objects.filter()
    #avelacru   
    max_per=max_per[0].price
    
    if cart_products:

        return  render(request, "template_rus/cart.html", {"cart":cart_products, "sums":sums, "count":count,"max_per":int(max_per)})
    else:
        return  render(request, "template_rus/cart.html", {"cart":cart_products, "sums":0, "count":0,"max_per":int(max_per)})

def checkout_page(request):
    profile = get_object_or_404(models.Profile, pk=request.user.profile.pk)
    

    order_products = profile.checkout_products_list.filter()

    #sums = [i.product.sale_price * i.count if i.product.sale > 0 else i.product.price * i.count for i in order_products ]
    mass = [(int(i.count_size) * float(i.product.mass))/100 if i.product.max_size>0 else int(i.count) * float(i.product.mass) for i in order_products]

    sums = 0
    for i in order_products:
        
        sums+=i.price

       
    #sums = sum(sums)
    mass = sum(mass)
    
    delyvery_box_mass = models.price_of_deliverybox.objects.filter(Q(mass_start__lte=mass) & Q(mass_end__gte=mass))[0]
    box_mass = delyvery_box_mass.total_mass
    mass+=box_mass
    
    user_info = models.my_contacts_info.objects.filter(profile=profile).order_by('-pk')
    shipping_price=None
    if user_info:
        user_info_zero = user_info[0]
        zone_countries = models.zone_countries.objects.filter()
        zone_shipping = models.zone_countries.objects.filter(country=user_info_zero.country)
        
        zone = models.zone.objects.filter(zone_countries__in = zone_shipping)
        Mass_and_money = models.Mass_and_money.objects.filter(Q(zones__in = zone) & Q(mass_start__lte=mass) &  Q(mass_end__gte=mass))
        

        if len(Mass_and_money)==1:
            shipping_price = Mass_and_money[0].money
        else:
            if Mass_and_money:
                minimum = Mass_and_money[0].money
                if minimum>Mass_and_money[1].money:
                    minimum = Mass_and_money[1].money
                shipping_price = minimum
    else:
        zone_countries = models.zone_countries.objects.filter()

    
    collection  = models.collection.objects.filter(profile = profile)
    collection_status = 2
    if collection:
        if len(collection[0].checkout_products.all())>0:
            collection_status = 1
        else:
            collection_status = 0



    if user_info:

        return render(request, "template_rus/checkout.html",{"profile":profile,"collection":collection,"user_info":user_info,"user_info_len":len(user_info), "order_products":order_products, "sums":sums, "zone_countries":zone_countries,"collection_status":collection_status, "shipping_price":shipping_price, "mass":int(mass), "box_mass":box_mass})
    else:
        return render(request, "template_rus/checkout.html",{"profile":profile,"collection":collection,"user_info":user_info, "order_products":order_products, "sums":sums, "mass":int(mass), "collection_status":collection_status,"zone_countries":zone_countries, "box_mass":box_mass})
def delete_address_book(request):
    key = request.POST.get("key")
    models.my_contacts_info.objects.filter(pk=key).delete()
    return JsonResponse("data", safe=False)
def checkout_collection_page(request, pk):
    profile = request.user.profile
    collection = get_object_or_404(models.collection, pk=pk)
    models.collection.objects.filter().delete()
    

    mass = [(int(i.count_size) * float(i.product.mass))/100 if i.product.max_size>0 else int(i.count) * float(i.product.mass)  for i in collection.orders.all()]
    
    mass = sum(mass)



    return render(request, "template_rus/checkout_shipping.html",{"mass":mass, "product_order":collection.orders.all()})
def get_ship_price(request):
    pk = request.POST.get("pk")
    my_contacts_info = get_object_or_404(models.my_contacts_info, pk=int(pk))
    zone_shipping = models.zone_countries.objects.filter(country= my_contacts_info.country)


    zone = models.zone.objects.filter(zone_countries__in =zone_shipping)
    mass = int(request.POST.get("mass"))
    
    Mass_and_money = models.Mass_and_money.objects.filter(Q(zones__in = zone) & Q(mass_start__lte=mass) &  Q(mass_end__gte=mass))
    
    if len(Mass_and_money)==1:
        shipping_price = Mass_and_money[0].money
        money_pk = Mass_and_money[0].pk
    elif len(Mass_and_money)>1:
        minimum = int(Mass_and_money[0].money)
        money_pk = Mass_and_money[0].pk
        if minimum>int(Mass_and_money[1].money):
            minimum = Mass_and_money[1].money
            money_pk = Mass_and_money[1].pk
        shipping_price = minimum

    else:
        shipping_price=0
        money_pk=0
    
    

    
    data = {
    "price":shipping_price,
    "money_pk":money_pk
    }
    return JsonResponse(data, safe=False)
def add_max_per(request):
    max_per = request.POST.get("max_per")
    max_per_order = models.max_cart_price.objects.filter()
    if len(max_per_order)>0:

        max_per_order=max_per_order[0]
        max_per_order.price=float(max_per)
        max_per_order.save()


    else:
        max_per_order = models.max_cart_price.objects.create(price=float(max_per))

    return JsonResponse("data", safe=False)

def add_day_of_products_api(request):
    count_product = request.POST.get("count_products")
    saleinf = request.POST.get("saleinf")
    salesup = request.POST.get("salesup")
    
    
    
    product_sales = models.products.objects.filter(sale__gt = 0)
    for product_sale in product_sales:
        product_sale.sale = 0
        
        product_sale.save()
    products = models.products.objects.filter().order_by('?')[:int(count_product)]
    
    for product in products:
        sales = random.randint(int(salesup), int(saleinf))
        product.sale = sales
        if product.counter_props.all():
            for i in product.counter_props.all():
                if int(sales)==0:
                    i.counter_price_sale = 0
                else:
                    i.counter_price_sale = int(int(i.counter_price)*((100-int(sales))))/100
                i.save()
        
        if product.price_pcs:
            
            product.sale_price_pcs = int(int(product.price_pcs)*(100-int(sales)))/100
        if product.price_size:
            
            product.sale_price_size = int(int(product.price_size)*(100-int(sales)))/100
        if product.price:
            product.sale_price = int(int(product.price)*(100-int(sales)))/100
            
        
        product.save()
        

    
    return JsonResponse("data", safe=False)

def max_per_order(request):
    max_per = models.max_cart_price.objects.filter()
    
    if len(max_per)>0:
        max_per=max_per[0].price
    else:
        max_per=0
    
    return render(request, "template_rus/max_per_order.html",{"max_per":int(max_per)})
def add_day_of_products(request):
    
    return render(request, "template_rus/add_day_of_products.html")


def collection_view(request):
    collection = get_object_or_404(models.collection, profile=request.user.profile)
    



    return render(request, "template_rus/collection_view.html",{"collection":collection})

def remove_collection(request):
    order_pk = request.POST.get("order_pk")
    collection_pk=request.POST.get("collection_pk")
    print(order_pk, collection_pk, "collection_pk")
    order = get_object_or_404(models.products_Order, pk=order_pk)
    collection = get_object_or_404(models.collection, pk=collection_pk)
    collection.orders.remove(order)
    collection.save()
    return JsonResponse("data", safe=False)
def create_delivery(request, pk):
    profile = request.user.profile

    
    collection = get_object_or_404(models.collection, profile=profile)
    checkouts = collection.checkout_products.all()

    mass = sum([i.mass for i in checkouts ])
    delyvery_box_mass = models.price_of_deliverybox.objects.filter(Q(mass_start__lte=mass) & Q(mass_end__gte=mass))[0]
    mass+=delyvery_box_mass.total_mass
    user_info = models.my_contacts_info.objects.filter(profile=profile).order_by('-pk')
    user_info_zero = user_info[0]
    

    zone_countries = models.zone_countries.objects.filter()
    zone_shipping = models.zone_countries.objects.filter(country=user_info_zero.country)
    
    
    zone = models.zone.objects.filter(zone_countries__in = zone_shipping)
    Mass_and_money = models.Mass_and_money.objects.filter(Q(zones__in = zone) & Q(mass_start__lte=mass) &  Q(mass_end__gte=mass))
    if len(Mass_and_money)==1:
        shipping_price = Mass_and_money[0].money
        
    else:
        minimum = Mass_and_money[0].money
        if int(minimum)>int(Mass_and_money[1].money):
            minimum = Mass_and_money[1].money
        shipping_price = minimum
        

    delivery = get_object_or_404(models.delivery_check, pk=pk)
    delivery.mass=mass
    delivery.price=shipping_price
    delivery.save()
    collection.delivery_check = delivery
    collection.save()
    for checkout in  checkouts:
        checkout.delivery_check = delivery
        

        checkout.save()


    
    return redirect("accounts:checkout_delivery", pk=delivery.id)
def create_joint_delivery(request, pk):
    profile = request.user.profile
    
    
    collection = get_object_or_404(models.collection, profile=profile)
    checkouts = collection.checkout_products.all()

    mass = sum([i.mass for i in checkouts ])
    delyvery_box_mass = models.price_of_deliverybox.objects.filter(Q(mass_start__lte=mass) & Q(mass_end__gte=mass))[0]
    mass+=delyvery_box_mass.total_mass
    user_info = models.my_contacts_info.objects.filter(profile=profile).order_by('-pk')
    user_info_zero = user_info[0]
    

    
    delivery = get_object_or_404(models.delivery_check, pk=pk)
    delivery.mass=mass
   
    delivery.save()
    collection.delivery_check = delivery
    collection.save()
    
    for checkout in  checkouts:
        checkout.delivery_check = delivery
        checkout.status = "joint"
        

        checkout.save()


    
    return redirect("accounts:orders")

def pay_delivery_api(request):

    delyvery_pk = request.POST.get("delyvery_pk")
    contact_pk  = request.POST.get("contact_pk")
    
    delyvery = get_object_or_404(models.delivery_check, pk=delyvery_pk)
    if contact_pk is not None:
        my_contacts_info = get_object_or_404(models.my_contacts_info, pk=contact_pk)
        delyvery.my_contacts_info=my_contacts_info
        money_pk = request.POST.get("money_pk")
        if money_pk is not None:
            Mass_and_money = get_object_or_404(models.Mass_and_money, pk=money_pk)
            delyvery.price=Mass_and_money.money
        

        delyvery.save()

    last_order_id = models.order_id_count.objects.all()
       
    if last_order_id:
        last_order_id = last_order_id.last()
        order_id = int(last_order_id.order_id)+1
        last_order_id.order_id = str(order_id)
        last_order_id.save()

    else:
        models.order_id_count.objects.create(order_id="3141801")
        order_id = 3141801
    current_site = get_current_site(request)
    confirmation_url = f'http://{current_site.domain}/api/check_payment_delyvery'
    url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/InitPayment"

    myobj = {
        "ClientID":"9da0d612-fa83-48a9-96ff-0bf0e61e9e54",
        "Username":"3d19541048",
        "Password":"lazY2k",
        "Description":"aaa",
        "OrderID":order_id,
        "Amount":10,
        "BackURL":confirmation_url
    }
    r = requests.post(url = url, json = myobj)

  

    resp_data = r.json()
    data = {
            "pay":1
    }
    if (int(resp_data["ResponseCode"])==1):
        PaymentID=resp_data["PaymentID"]
        
        data.update({"PaymentID":PaymentID})
        delyvery.order_id=order_id
        delyvery.save()
    

        
        
    
    
    return JsonResponse(data, safe=False)
def error404(request):
    return render(request, "template_rus/error404.html")

def page_not_found(request, exception):
    return render(request, '404_templates/404.html', status=500)
def add_check_api(request):
    indicator = request.POST.get("indicator")
    create = request.POST.get("create")
    price = 0
    mass_add_indicator = request.POST.get("mass_add_indicator")

    
    
    if indicator=="collection":
        mass=0
        checkout_products = models.checkout_products.objects.filter(Q(status="pay") & Q(profile=request.user.profile))
        if create is not None:
            collection = models.collection.objects.create(collection_name="collection", profile=request.user.profile)
        else:
            collection = get_object_or_404(models.collection, profile = request.user.profile)

        
        for i in request.user.profile.checkout_products_list.all():
            if i.indicator=="size":
                if i.product.sale_price_size:
                    price += (i.count_size/i.product.min_size)*i.product.sale_price_size
                else:
                    price += (i.count_size/i.product.min_size)*i.product.price_size
                
                
                
            elif i.indicator=="counter":
                price_counter=None
                
                

                for j in  i.product.counter_props.all().order_by('counter_prop'):
                    if (int(i.count) >= int(j.counter_prop)):
                        price_counter = float(j.counter_price)
                        if(j.counter_price_sale):
                            price_counter= float(j.counter_price_sale)
                        else:
                            price_counter= float(j.counter_price)
                price+=price_counter*i.count


                        
                
                
            elif i.indicator=="count":
                if i.product.sale_price:
                    price += i.count*i.product.sale_price
                else:
                    price += i.count*i.product.price
                
                
            elif i.indicator=="size_pcs":
                if i.product.sale_price_pcs:
                    price += i.count*i.product.sale_price_pcs
                else:
                    price += i.count*i.product.price_pcs
                
                

                #orders = models.products_Order.objects.create(product=product_cart.product, customer=request.user.profile,count_size=count,price=price)
            else:
                pass
            
            if i.product.max_size>0:
                mass+=(int(i.count_size) * float(i.product.mass))/100
            else:
                mass+=int(i.count) * float(i.product.mass)

        
        

        

        
        
        
        last_order_id = models.order_id_count.objects.all()
       
        if last_order_id:
            last_order_id = last_order_id.last()
            order_id = int(last_order_id.order_id)+1
            last_order_id.order_id = str(order_id)
            last_order_id.save()

        else:
            models.order_id_count.objects.create(order_id="3141801")
            order_id = 3141801
            
        


        contact_pk = request.POST.get("contact_pk")
        print(contact_pk, "contact_pk")
        
        my_contacts_info = get_object_or_404(models.my_contacts_info, pk=contact_pk)
        checkout = models.checkout_products.objects.create(profile=request.user.profile,price=price, order_id=order_id, collection=collection, mass=mass,first_name=my_contacts_info.first_name, last_name=my_contacts_info.last_name,email=my_contacts_info.email,phone_number=my_contacts_info.phone_number,country=my_contacts_info.country,state=my_contacts_info.state,city=my_contacts_info.city,address=my_contacts_info.address, index=my_contacts_info.index)
        
        for order in request.user.profile.checkout_products_list.all():

            checkout.products_Order.add(order)
        
        checkout.status="collectionnotpay"
        comment = request.POST.get("comment")
        if comment is not None:
            checkout.comments = comment

        checkout.save()
        
        delivery_check_status = None
        if len(collection.checkout_products.all())==0:
            delivery_check = models.delivery_check.objects.create(pay_status="dontpay")
            collection.delivery_check = delivery_check
            delivery_check_status =delivery_check
        else:
            delivery_check_status =collection.delivery_check

        

        collection.save()
        data = {
            "collection":1
        }
    else:
        #price = sum([i.product.sale_price * i.count if i.product.sale > 0 else i.product.price * i.count for i in request.user.profile.checkout_products_list.all()])
        price = 0
        for i in request.user.profile.checkout_products_list.all():
            if i.indicator=="size":
                if i.product.sale_price_size:
                    price += (i.count_size/i.product.min_size)*i.product.sale_price_size
                else:
                    price += (i.count_size/i.product.min_size)*i.product.price_size
                
                
                
            elif i.indicator=="counter":
                price_counter=None
                
                

                for j in  i.product.counter_props.all().order_by('counter_prop'):
                    if (int(i.count) >= int(j.counter_prop)):
                        price_counter = float(j.counter_price)
                        if(j.counter_price_sale):
                            price_counter= float(j.counter_price_sale)
                        else:
                            price_counter= float(j.counter_price)
                price+=price_counter*i.count


                        
                
                
            elif i.indicator=="count":
                if i.product.sale_price:
                    price += i.count*i.product.sale_price
                else:
                    price += i.count*i.product.price
                
                
            elif i.indicator=="size_pcs":
                if i.product.sale_price_pcs:
                    price += i.count*i.product.sale_price_pcs
                else:
                    price += i.count*i.product.price_pcs
                
                

                #orders = models.products_Order.objects.create(product=product_cart.product, customer=request.user.profile,count_size=count,price=price)
            else:
                pass
        mass = sum([(int(i.count_size) * float(i.product.mass))/100 if i.product.max_size>0 else int(i.count) * float(i.product.mass)  for i in request.user.profile.checkout_products_list.all()])
        order_mass =  mass
        if mass_add_indicator is None:
            delyvery_box_mass = models.price_of_deliverybox.objects.filter(Q(mass_start__lte=mass) & Q(mass_end__gte=mass))[0]
            
            mass+=delyvery_box_mass.total_mass



        last_order_id = models.order_id_count.objects.all()
       
        if last_order_id:
            last_order_id = last_order_id.last()
            order_id = int(last_order_id.order_id)+1
            last_order_id.order_id = str(order_id)
            last_order_id.save()

        else:
            models.order_id_count.objects.create(order_id="3141801")
            order_id = 3141801
            

        
        contact_pk = request.POST.get("contact_pk")
        
        my_contacts_info = get_object_or_404(models.my_contacts_info, pk=contact_pk)
        zone_shipping = models.zone_countries.objects.filter(country=my_contacts_info.country)
        
        
        zone = models.zone.objects.filter(zone_countries__in = zone_shipping)
        Mass_and_money = models.Mass_and_money.objects.filter(Q(zones__in = zone) & Q(mass_start__lte=mass) &  Q(mass_end__gte=mass))
        if len(Mass_and_money)==1:
            shipping_price = Mass_and_money[0].money
            
        else:
            minimum = Mass_and_money[0].money
            if int(minimum)>int(Mass_and_money[1].money):
                minimum = Mass_and_money[1].money
            shipping_price = minimum
        delivery_check = models.delivery_check.objects.create(price=shipping_price,mass=mass, my_contacts_info=my_contacts_info, order_id=order_id)
        
    
        checkout = models.checkout_products.objects.create(profile=request.user.profile,price=price,mass=order_mass, order_id=order_id, delivery_check=delivery_check, first_name=my_contacts_info.first_name, last_name=my_contacts_info.last_name,email=my_contacts_info.email,phone_number=my_contacts_info.phone_number,country=my_contacts_info.country,state=my_contacts_info.state,city=my_contacts_info.city,address=my_contacts_info.address, index=my_contacts_info.index)
        if mass_add_indicator is not None:
            checkout.status="not_payjoint"
        else:
            checkout.status="notpay"
        comment = request.POST.get("comment")
        if comment is not None:
            checkout.comments = comment
        

        for i in request.user.profile.checkout_products_list.all():

            checkout.products_Order.add(i)
        checkout.save()
        

        data = {
            "collection":0
        }
    current_site = get_current_site(request)
    confirmation_url = f'http://{current_site.domain}/api/check_payment'
    url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/InitPayment"
    print("order_id", order_id)
    myobj = {
        "ClientID":"9da0d612-fa83-48a9-96ff-0bf0e61e9e54",
        "Username":"3d19541048",
        "Password":"lazY2k",
        "Description":"aaa",
        "OrderID":order_id,
        "Amount":10,
        "BackURL":confirmation_url
    }
    r = requests.post(url = url, json = myobj)

  

    resp_data = r.json()
    if (int(resp_data["ResponseCode"])==1):
        PaymentID=resp_data["PaymentID"]
        
        data.update({"PaymentID":PaymentID})
    formUrl = None

        
        
    
    print(resp_data, "lmkl", data)
    return JsonResponse(data, safe=False)
def change_delivery_price(request,pk):
    checkout = get_object_or_404(models.checkout_products, pk=pk)
    return render(request, "template_rus/change_delivery_pay.html", {"checkout":checkout})
def apichange_delivery_price(request):
    pk = request.POST.get("pk")
    price = request.POST.get("price")
    delivery = get_object_or_404(models.delivery_check, pk=pk)
    delivery.price = float(price)

    delivery.save()
    checkout = models.checkout_products.objects.filter(delivery_check=delivery)
    checkout.update(status = "joint_green")
    
    return JsonResponse("data" , safe=False)


def check_payment(request):
    
    resposneCode = request.GET.get("resposneCode")
    
    if resposneCode=="00":
        url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/GetPaymentDetails"
        PaymentID = request.GET.get("paymentID")
        myobj = {
        "PaymentID":PaymentID,
        "Username":"3d19541048",
        "Password":"lazY2k"
        }




        r = requests.post(url = url, json = myobj)

      

        resp_data = r.json()
        if (resp_data["ResponseCode"]=='00' and resp_data["OrderStatus"]=='2'):
            
            
            
            checkout_products = get_object_or_404(models.checkout_products, order_id = resp_data["OrderID"])
            #collection add
            for i in checkout_products.products_Order.all():
                if i.count_size:
                    i.product.max_size-=(i.count_size/i.product.min_size)*10
                else:
                    all_pcs = int(i.product.pcs)-i.count
                    i.product.pcs=str(all_pcs)
                if i.product.max_size==0 or i.product.pcs==0:
                    i.available = False
                i.product.save()
            if checkout_products.status=="collectionnotpay":
                collection = get_object_or_404(models.collection, profile = request.user.profile)
                if collection.delivery_check:
                    checkout_products.delivery_check = collection.delivery_check
                collection.checkout_products.add(checkout_products)
                checkout_products.status = "collectionpay"
                collection.save()
            elif checkout_products.status=="not_payjoint":
                checkout_products.status = "joint"

            else:
                checkout_products.status = "pay"
            checkout_products.save()
            request.user.profile.product_cart.clear()
            request.user.profile.save()
            html_message = render_to_string('layouts/email_template.html',{"checkout":checkout_products, "request":request})
            email  = request.user.profile.email
            
            
            
            
            plain_message = strip_tags(html_message)
            send_mail(
                'Checkout',
                plain_message,
                'boutique.broderie.am@gmail.com',
                [email],
                fail_silently=False,
                html_message=html_message,
                

                )
            

        



    return redirect("accounts:orders")
def check_payment_delyvery(request):
    resposneCode = request.GET.get("resposneCode")
    print(resposneCode, "resposneCode")
    if resposneCode:
        url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/GetPaymentDetails"
        PaymentID = request.GET.get("paymentID")
        myobj = {
        "PaymentID":PaymentID,
        "Username":"3d19541048",
        "Password":"lazY2k"
        }


        r = requests.post(url = url, json = myobj)

      

        resp_data = r.json()

        delivery_check = get_object_or_404(models.delivery_check, order_id = resp_data["OrderID"])
        
        
            
        
        

        
        if (resp_data["ResponseCode"]=='00' and resp_data["OrderStatus"]=='2'):
            delivery_check.pay_status = "delyverypay"
            
            delivery_check.save()
            
            try:
                
                
                collection = get_object_or_404(models.collection, delivery_check=delivery_check)
                
                collection.checkout_products.clear()


                collection.save()
                collection.delete()
            except:
                pass
            html_message = render_to_string('layouts/email_template.html',{"delivery_check":delivery_check, "request":request})
            email  = request.user.profile.email
            
            
            
            
            plain_message = strip_tags(html_message)
            send_mail(
                'Checkout',
                plain_message,
                'boutique.broderie.am@gmail.com',
                [email],
                fail_silently=False,
                html_message=html_message,
                

                )
            
            
            
            
        print(resp_data, "resp_data")
        return redirect("accounts:orders") 

def login_page(request):
    return  render(request, "template_rus/login.html")
def sign_up_page(request):
    return  render(request, "template_rus/sign_up.html")
def password_recovery_page(request):
    return  render(request, "template_rus/recovery_password.html")
def new_password_page(request):
    return render(request, "template_rus/reset_password_page.html")
def blog(request):
    blog_articles = models.Blog.objects.all()
    number_of_item = 3
    paginatorr = Paginator(blog_articles, number_of_item)
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)
        results = paginatorr.page(page_n).object_list.filter()
        if (int(page_n)-2>=0):
            page_range = page_range[int(page_n)-2:int(page_n)+2]
        else:
            page_range = page_range[0:int(page_n)+3]
        
        return JsonResponse({"results":serializers.serialize('json', results),"page_range":list(page_range)})

    return  render(request, "template_rus/blog.html", {"blog_articles":first_page, "page_range":page_range})
def blog_article(request, pk):
    Blog = get_object_or_404(models.Blog, pk=pk)


    return  render(request, "template_rus/blog_article.html", {"Blog":Blog})
def my_products(request):
    products = models.products.objects.all().order_by("-created_at")
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, "template_rus/scroll_my_products.html", {"products":products, "products_count":len(products)})
    
def change_profile(request):
    profile = get_object_or_404(models.Profile, user = request.user)
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    password = request.POST.get("password")
    profile_password = profile.user.password
    if profile_password != password:
        user = User.objects.get(username=profile.user.username)
        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
    

        #user = authenticate(username= u.username, password=password)
        
    
        login(request, user)
        profile.password = password
    if profile.email != email:
        profile.email = email
    if profile.first_name != first_name:
        profile.first_name = first_name
    if profile.phone_number != phone_number:
        profile.phone_number = phone_number
    if profile.last_name != last_name:
        profile.last_name = last_name
    profile.save()

    
    print(email, first_name, last_name, phone_number)
    return JsonResponse(1, safe=False)




    
def add_sales(request):
    sales = request.POST.get("sales")
    product_pk = request.POST.get("pk")
    product = get_object_or_404(models.products, pk=int(product_pk))
    product.sale = float(sales)
    
    

    
    if int(sales)==0:
        product.sale_price = 0
        product.sale_price_pcs=0
        product.sale_price_size=0
    else:
        if product.counter_props.all():
            for i in product.counter_props.all():
                if int(sales)==0:
                    i.counter_price_sale = 0
                else:
                    i.counter_price_sale = int(int(i.counter_price)*((100-int(sales))))/100
                i.save()
        
        if product.price_pcs:
            
            product.sale_price_pcs = int(int(product.price_pcs)*(100-int(sales)))/100
        if product.price_size:
            
            product.sale_price_size = int(int(product.price_size)*(100-int(sales)))/100
        if product.price:
            product.sale_price = int(int(product.price)*(100-int(sales)))/100
    
    product.save()
    
    return JsonResponse("data", safe=False)


def assembled(request):
    pk = request.POST.get("pk")
    checkout_products = get_object_or_404(models.checkout_products, pk=pk)
    checkout_products_list = models.checkout_products.objects.filter(delivery_check=checkout_products.delivery_check).exclude(pk=pk)

    checkout_products.assembled = "assembled"
    checkout_products.save()
    checkout_products_list.update(assembled="assembled")
    return JsonResponse("data", safe=False)


def my_checkout_products(request):
    checkouts = models.checkout_products.objects.filter(Q(status="pay") | Q(status="collectionpay") |  Q(status="send") | Q(status="unsend") | Q(status="joint") | Q(status="joint_green")).order_by('-date_ordered')
    zone_countries = models.zone_countries.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(checkouts, 2)
    try:
        checkouts = paginator.page(page)
    except PageNotAnInteger:
        checkouts = paginator.page(1)
    except EmptyPage:
        checkouts = paginator.page(paginator.num_pages)
    
    return  render(request, "template_rus/my_checkout_list_scroll.html", {"checkouts":checkouts, "zone_countries":zone_countries})
def check(request, pk):
    order = get_object_or_404(models.products_Order, pk=pk)

    return render(request, "template_rus/check.html", {"order":order})
def favorite(request):
    favorite_products = models.favorite_products.objects.filter(profile=request.user.profile)
    return  render(request, "template_rus/favorites.html", {"favorite_products":favorite_products})
def add_product_page(request):
    category_choeses = models.category_choeses.objects.filter()
    barnds = models.Brand.objects.all()


    return  render(request, "template_rus/add_product_page.html",{"category_choeses":category_choeses, "barnds":barnds})
def add_product_page_size(request):
    category_choeses = models.category_choeses.objects.filter()
    barnds = models.Brand.objects.all()


    return  render(request, "template_rus/add_product_page_size.html",{"category_choeses":category_choeses, "barnds":barnds})
def add_product_page_size_pcs(request):
    category_choeses = models.category_choeses.objects.filter()
    barnds = models.Brand.objects.all()


    return  render(request, "template_rus/add_product_page_size_pcs.html",{"category_choeses":category_choeses, "barnds":barnds})
def change_product_page(request, pk):
    product = get_object_or_404(models.products, pk=pk)
    images =models.productsimage.objects.filter(post=product)
    barnds = models.Brand.objects.all()

    if product.price_size:
        return  render(request, "template_rus/change_product_page_size.html", {"product":product,"barnds":barnds, "images":images,"images_len":len(images), "sub_categorys":product.sub_categories.all(), "sub_categorys_len":len(product.sub_categories.all())})
    
    else:
        return  render(request, "template_rus/change_product_page.html", {"product":product,"barnds":barnds, "images":images,"images_len":len(images), "sub_categorys":product.sub_categories.all(), "sub_categorys_len":len(product.sub_categories.all())})
    
   

def add_about_us(request):
    return  render(request, "template_rus/add_about_us.html")


def address_book(request):
    my_contacts_info = models.my_contacts_info.objects.filter(profile=request.user.profile)
    return  render(request, "template_rus/address_book.html",{"my_contacts_info":my_contacts_info})
def api_add_categories(request):
    category_name=request.POST.get("category_name")
    sub_categories_switch = request.POST.get("sub_categories_switch")
    category_choeses = models.category_choeses.objects.create(name=category_name)
    if sub_categories_switch:
        sub_categories_length = int(request.POST.get("sub_categories_length"))
        for i in range(0, sub_categories_length):
            sub_category = models.sub_category.objects.create(name=request.POST.get(f'sub_name{i}'))
            category_choeses.sub_category.add(sub_category)
            
        category_choeses.save()
    return JsonResponse("data", safe=False)
    
def add_favorite_products(request):
    pk = request.POST.get("pk")
   
    
    product = get_object_or_404(models.products, pk = pk)
    profile = get_object_or_404(models.Profile, user = request.user)
    
    
    if not models.favorite_products.objects.filter(product=product, profile = profile).exists():
        if product.price_size:
            add_product_cart =models.favorite_products.objects.create(profile = profile, product = product, count_size=product.min_size)
        else:
            add_product_cart =models.favorite_products.objects.create(profile = profile, product = product,count = 1)

        data = {
            "data":1,
            "product_pay":product.price,
            "name":product.name_ru,
            
            "pk":product.pk,
            "image":str(product.avatar_p)
            
           


        }
    else:
        models.favorite_products.objects.filter(product=product, profile = profile).delete()
        data = {
            "data":0,
             "product_pay":product.price,
            "name":product.name_ru,
            
             "pk":product.pk
        }

    
    return JsonResponse(data, safe=False)


def add_cart_product(request):
    pk = request.POST.get("pk")
    count = request.POST.get("count")
    count_size = request.POST.get("count_size")
    indicator = request.POST.get("indicator")
    product_page_request_status = request.POST.get("product_page_request_status")
    
    product = get_object_or_404(models.products, pk = pk)
    profile = get_object_or_404(models.Profile, user = request.user)
    #count = models.products_cart.objects.filter(profile = profile).count()
    
    
    if product_page_request_status is not None:
        count = 1
        count_size = str(product.min_size)+" sm"
    
    min_size = 1

    if not profile.product_cart.filter(product=product).exists():
        if product.counter_props.all():
            indicator = "counter"
            
            price=None

            for i in  product.counter_props.all():
                if (int(count) >= int(i.counter_prop)):
                    price = int(i.counter_price)
                    if i.counter_price_sale:
                        
                        price = int(i.counter_price_sale)


                    
                    
            if price is None:
                add_product_cart =models.products_cart.objects.create(profile = profile, product = product, count=count, indicator=indicator)
                price_total = int(add_product_cart.count)*product.price
            else:
                add_product_cart =models.products_cart.objects.create(profile = profile, product = product, count=count, indicator=indicator)
                price_total = int(add_product_cart.count)*price
            


        elif product.price_size:
            indicator = "size"
            


            add_product_cart =models.products_cart.objects.create(profile = profile, product = product, count_size=count_size[:-3], indicator=indicator)
            this_price = product.price_size
            if product.sale_price_size:
                this_price = product.sale_price_size
            min_size = product.min_size

            price_total = int(count_size[:-3])*product.min_size*this_price/100
        elif product.price_pcs:
            indicator = "size_pcs"
            add_product_cart =models.products_cart.objects.create(profile = profile, product = product, count=count,indicator=indicator)
            this_price = product.price_size
            if product.sale_price_pcs:
                this_price = product.sale_price_pcs

            price_total = int(count)*this_price
        else:
            indicator = "count"
            add_product_cart =models.products_cart.objects.create(profile = profile, product = product, count=count,indicator=indicator)
            this_price = product.price
            if product.sale_price:
                this_price = product.sale_price

            price_total = int(count)*this_price

        

        data = {
            "data":1,
            "product_pay":product.price,
            "name":product.name_ru,
            "price_total":price_total,
            "pk":product.pk,
            "min_size":min_size,
            "image":str(product.avatar_p)
            
           


        }
        profile.product_cart.add(add_product_cart)
        profile.save()
    else:
        data = {
            "data":0,
             "product_pay":product.price,
            "name":product.name_ru,
            "count":count,
             "pk":product.pk
        }
        
    

    
    return JsonResponse(data, safe=False)
def product_isactive(request):
    pk = request.POST.get("pk")
    turn_onoff=  request.POST.get("turn_onoff")
    product = get_object_or_404(models.products, pk = int(pk))

    if int(turn_onoff) == 0:
        product.active = False
    else:
        product.active = True
    product.save()
    
    return JsonResponse("data", safe=False)
def product_is_send(request):
    pk = request.POST.get("pk")
    

    delivery_check = get_object_or_404(models.delivery_check, pk = pk)
    checkouts = models.checkout_products.objects.filter(delivery_check = delivery_check)
    
    
    

    
    
    checkouts.update(status = "send")
    

    
    
    
    return JsonResponse("data", safe=False)

def product_delete(request):
    
    group = request.POST.get("group")
    if group is not None:
        lens = request.POST.get("lens")
        for i in range(0,int(lens)):
            models.products.objects.filter(pk = int(request.POST.get(f'product_pk{i}'))).delete()

    else:
        pk = request.POST.get("pk")
        product = models.products.objects.filter(pk = int(pk)).delete()
    
    data = {"success":1}
    
    return JsonResponse(data, safe=False)
def product_detalis_view(request, pk):
    # add if (product ststus == "True")

    product = get_object_or_404(models.products, pk = pk)

    
    images = models.productsimage.objects.filter(post =product)
   
    product_recommendation = models.products.objects.filter().exclude(pk =pk)[:10]
    
   
    
    

    return render(request, "template_rus/product_page.html", {"product":product, "product_recommendation":product_recommendation, "images":images})
@csrf_protect
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))

def post_detail(request, pk):
    return render(request, "template_rus/blog_article.html")
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            

            post.name_ru = request.POST.get("Name_ru")
            post.name_am = request.POST.get("Name_am")
            post.name_en = request.POST.get("Name_en")
            
            
            
            post.save()
            return redirect('accounts:blog_article', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'template_rus/post_edit.html', {'form': form})
def about_new(request):
    if request.method == "POST":
        form = aboutform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            return redirect('accounts:about_us')
    else:
        form = aboutform()
    return render(request, 'template_rus/edit_about_us.html', {'form': form})
def about_edit(request, pk):
    post = get_object_or_404(models.about_us, pk=pk)
    if request.method == "POST":
        form = aboutform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            return redirect('accounts:about_us')
    else:
        form = aboutform(instance=post)
    
    return render(request, 'template_rus/add_about_us.html', {'form': form, "post":post})
def delivery_info_new(request):
    if request.method == "POST":
        form = delivery_infoform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            return redirect('accounts:delivery_info')
    else:
        form = delivery_infoform()

    return render(request, 'template_rus/add_delivery_us.html', {'form': form})
def delivery_info_edit(request, pk):
    post = get_object_or_404(models.delivery_info, pk=pk)
    if request.method == "POST":
        form = delivery_infoform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            return redirect('accounts:delivery_info')
    else:
        form = delivery_infoform(instance=post)
    
    return render(request, 'template_rus/add_delivery_us.html', {'form': form, "post":post})


def rules_new(request):
    if request.method == "POST":
        form = rulesform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            return redirect('accounts:rules')
    else:
        form = rulesform()

    return render(request, 'template_rus/edit_rules.html', {'form': form})
def rules_edit(request, pk):
    post = get_object_or_404(models.rules, pk=pk)
    if request.method == "POST":
        form = rulesform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            return redirect('accounts:rules')
    else:
        form = rulesform(instance=post)
    
    return render(request, 'template_rus/edit_rules.html', {'form': form, "post":post})

def post_edit(request, pk):
    post = get_object_or_404(models.Blog, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            name_am = request.POST.get("Name_am")
            name_en = request.POST.get("Name_en")

            

            post.name_ru = request.POST.get("Name_ru")
            
            
            
            
            post.save()
            return redirect('accounts:blog_article', pk=post.pk)
    else:
        form = PostForm(instance=post)
    print(post, "post")
    return render(request, 'template_rus/post_edit.html', {'form': form, "post":post})
def delete_comments(request):
    comment = models.products_comment.objects.filter(pk=int(request.POST.get("pk"))).delete()

    return JsonResponse("data", safe=False)
def change_brand(request):
    pk = request.POST.get("pk")
    name = request.POST.get("name")
    image = request.FILES.get("image")

    brand = get_object_or_404(models.Brand, pk=int(pk))
    if image is not None:
        brand.brand_picture = image
    brand.brand = name
    brand.save()
    return JsonResponse("data", safe=False)
def add_user_info(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    address = request.POST.get("address")
    index = request.POST.get("index")
    city = request.POST.get("city")
    country = request.POST.get("country")
    state = request.POST.get("state")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    info = models.my_contacts_info.objects.create(profile = request.user.profile,first_name = first_name,last_name=last_name,email=email,phone_number=phone_number,country=country,state=state,city=city,address=address,index=index)
    data = {"info_pk":info.pk}
    return JsonResponse(data,safe=False)
def change_user_info(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    address = request.POST.get("address")
    index = request.POST.get("index")
    city = request.POST.get("city")
    country = request.POST.get("country")
    state = request.POST.get("state")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    pk = request.POST.get("pk")
    info = get_object_or_404(models.my_contacts_info, pk=int(pk))
    info.first_name = first_name
    info.last_name = last_name
    print(first_name, "first_name")
    if first_name is None or len(first_name)==0:
        info.first_name = request.user.profile.first_name
        info.last_name = request.user.profile.last_name

    info.email = email
    info.address = address
    info.index = index
    info.state = state
    info.country = country
    info.phone_number = phone_number
    info.city = city
    info.save()


    
    
    return JsonResponse("data",safe=False)

def delete_blog(request, pk):
    
    models.Blog.objects.filter(pk=pk).delete()
    return redirect('accounts:blog')


def add_blog_view(request):
    
    name = request.POST.get("name_ru")
    description = request.POST.get("Description_ru")
    img_len = request.POST.get("img_len")
    for i in range(1, int(img_len)):
        
        print(request.FILES.get(f'images{i}'))
    print(request.FILES.get(f'images{0}'))
    blog = models.Blog.objects.create(name_ru=name, description_rus=description, avatar_p=request.FILES.get(f'images{0}'), text=description)
    return JsonResponse(blog.pk, safe=False)

    
def add_product_api(request):

    
    name_ru = request.POST.get("name_ru")
    name_am = request.POST.get("name_am")
    name_en = request.POST.get("name_en")
    description_ru = request.POST.get("Description_ru")
    description_am = request.POST.get("Description_am")
    description_en = request.POST.get("Description_en")
    brand_pk = request.POST.get("Brand")
    category = request.POST.get("catrgory")
    size = request.POST.get("Size")
    pcs = request.POST.get("pcs")
    pcs_type = request.POST.get("pcs_type")
    price = request.POST.get("Price")
    img_len = request.POST.get("img_len")
    color = request.POST.get("color")
    color_id = request.POST.get("color_code")
    table_len_size = request.POST.get("table_len_size")
    table_len_size_pcs = request.POST.get("table_len_size_pcs")
    
    table_len_counter = request.POST.get("table_len_counter")
    table_len_mass = request.POST.get("table_len_mass")
    
    
    SKU_code = request.POST.get("SKU_code")
    
    catrgory_pk = request.POST.get("catrgory_pk")
    video_link = request.POST.get("video_link")
    video_file = request.FILES.get("video_file")
    Sale_product = request.POST.get("Sale_product")
    mass_product = request.POST.get("mass_product")



    


    sub_categories_len = request.POST.get("sub_categories_len")
    if catrgory_pk is  not None:
        category_obj = models.category_choeses.objects.filter(category_id_main=catrgory_pk)
    else:
        category_obj = models.category_choeses.objects.filter(name=category)
    deck = list(range(0, 9))
    

    if not category_obj:
        
        if catrgory_pk is  None:
            
            
            random.shuffle(deck)
            catrgory_pk = ''.join(str(x) for x in deck)



        category_obj = models.category_choeses.objects.create(name=category,category_id_main=catrgory_pk)
        


    else:
        products_count = int(category_obj[0].products_count)+1
        category_obj.update(products_count=products_count)
        category_obj = category_obj[0]

    sub_category_name = ""
    
    


    
   
   
    image_main = request.FILES.get(f'images{0}')
    product = models.products.objects.create(name_ru=name_ru,name_am=name_am,name_en=name_en,SKU_code=SKU_code, pcs=pcs,description_rus=description_ru, description_arm=description_am, description_eng=description_en, pcs_type=pcs_type, avatar_p=image_main,zoom_image=image_main, category_choeses=category_obj)
    if brand_pk is not None:
        brand = get_object_or_404(models.Brand, pk=brand_pk)
        product.Brand = brand
    if video_link is not None:
        product.video_link = video_link
        
    if video_file is not None:
        product.video = video_file
        
    
    if Sale_product is not None:
        product.sale=Sale_product
    if mass_product is not None:
        product.mass=mass_product
    product.save()
    
    if sub_categories_len is not None:
        for i in range(0,int(sub_categories_len)):
            category_name=request.POST.get(f'sub_category_name{i}')
            sub_category_obj = models.category_choeses.objects.filter(name=category_name)
            if not sub_category_obj:
                random.shuffle(deck)
                catrgory_pk = ''.join(str(x) for x in deck)

                sub_category_obj = models.category_choeses.objects.create(name=category_name,name_en =request.POST.get(f'sub_category_name_en{i}') ,name_am =request.POST.get(f'sub_category_name_am{i}'), parent=category_obj, category_id_main = catrgory_pk,category_id=product.category_choeses.pk)
            else:
                products_count = int(sub_category_obj[0].products_count)+1
                sub_category_obj.update(products_count=products_count)
                sub_category_obj = sub_category_obj[0]
            product.sub_categories.add(sub_category_obj)
            

            
                
            #category_obj.subcategory.add(sub_category_obj)
            

            category_obj = sub_category_obj

            
    
    for i in range(1, int(img_len)):
        models.productsimage.objects.create(post=product, avatar_e=request.FILES.get(f'images{i}'))
    
    if price is None:
        
        if table_len_counter is not None:
            product.price = price
        
        else:
            product.price = request.POST.get(f'size_price{0}')
    else:
        if table_len_counter is not None:
            if int(table_len_counter) != 0:
                product.price = price



            
        else:
            product.price = price
        
    if table_len_counter is not None:
        if int(table_len_counter) != 0:
            minimum = int(request.POST.get(f'counter_prop{0}'))
            for i in range(0, int(table_len_counter)):
                if int(request.POST.get(f'counter_prop{i}'))<minimum:
                    minimum = int(request.POST.get(f'counter_prop{i}'))
                
                if int(request.POST.get(f'counter_prop{i}'))==1:
                    product.price  = float(request.POST.get(f'counter_price{i}'))
                counter_props = models.counter_props.objects.create(counter_price=request.POST.get(f'counter_price{i}'), counter_prop = request.POST.get(f'counter_prop{i}'))
                product.counter_props.add(counter_props)
            #counter_props = models.counter_props.objects.create(counter_name="от 1", counter_price=price, counter_prop = 1)
            product.counter_props.add(counter_props)
    
    if table_len_size != 0 and table_len_size is not None:
        product.min_size = int(request.POST.get("min_size"))
       
        product.price_size = (int(request.POST.get("price_size"))*product.min_size)/100
       
        product.max_size = int(request.POST.get("max_size"))
    elif table_len_size_pcs is not None:
        product.price_pcs = int(request.POST.get("price_size_pcs"))
        
        
        #product.price = (product.price*product.min_size)/100
        
        
    
    product.save()
    
    
    
    return JsonResponse(product.pk, safe=False)
def get_category_ids(request):
    pk = request.POST.get("pk")
    deg = request.POST.get("deg")
    if pk != "undefined":
        if int(deg)==1:
            category_choeses=models.category_choeses.objects.filter(category_id_main=pk)
        else:
            category_choeses=models.category_choeses.objects.filter(pk=pk)
       
        sub_categories = models.category_choeses.objects.filter(parent__in=category_choeses)
    else:
        sub_categories=[]

    
    

    return JsonResponse(serializers.serialize('json', sub_categories),safe=False)

def add_product_change_api(request):
    name_ru = request.POST.get("name_ru")
    name_en = request.POST.get("name_en")
    name_am = request.POST.get("name_am")
    description_rus = request.POST.get("Description_ru")
    description_arm = request.POST.get("Description_am")
    description_eng = request.POST.get("Description_en")
    brand = request.POST.get("brand")
    category = request.POST.get("catrgory")
    size = request.POST.get("Size")
    pcs = request.POST.get("pcs")
    pcs_type = request.POST.get("pcs_type")
    price = request.POST.get("Price")
    img_len = request.POST.get("img_len")
    color = request.POST.get("color")
    color_id = request.POST.get("color_code")
    table_len_size = request.POST.get("table_len_size")
    table_len_counter = request.POST.get("table_len_counter")
    table_len_mass = request.POST.get("table_len_mass")
    
    brand_pk = request.POST.get("Brand")
    SKU_code = request.POST.get("SKU_code")
    
    category_new_value = request.POST.get("category_new_value")
    video_link = request.POST.get("video_link")
    video_file = request.FILES.get("video_file")
    pk = request.POST.get("pk")
    video_link = request.POST.get("video_link")
    video_file = request.FILES.get("video_file")
    table_len_size_pcs = request.POST.get("table_len_size_pcs")
    product = get_object_or_404(models.products, pk=int(pk))
    product.name_ru = name_ru
    product.name_en = name_en
    product.name_am = name_am
    product.description_rus = description_rus
    product.description_arm = description_arm
    product.description_eng = description_eng
    if color is not None:
        product.color = color
    if color_id is not None:
        product.color_id = color_id
    
    if price is None:
        
        if table_len_counter is not None:
            product.price = price
        
        else:
            product.price = request.POST.get(f'size_price{0}')
    else:
        if table_len_counter is not None:
            if int(table_len_counter) != 0:
                product.price = price



            
        else:
            if product.sale_price:
                product.sale_price = int(int(price)*(100-int(product.sale)))/100
            product.price = price
    
    
    
    product.SKU_code=SKU_code
    if brand_pk is not None:
        brand = get_object_or_404(models.Brand, pk=brand_pk)
        product.Brand = brand
    product.pcs=pcs
   
    product.pcs_type=pcs_type
    images_len_delete = request.POST.get("images_len_delete")
    main_image_delete = request.POST.get("main_image_delete")
    Sale_product = request.POST.get("Sale_product")
    mass_product = request.POST.get("mass_product")
    if Sale_product is not None:
        product.sale=Sale_product
    if mass_product is not None:
        product.mass=mass_product
    
    
    deck = list(range(0, 9))
    
    sub_categories_len = request.POST.get("sub_categories_len")
    
    


    category_obj_main = models.category_choeses.objects.filter(name=category)
    catrgory_before  = request.POST.get("catrgory_before")
    print(category_new_value, "category_new_value", catrgory_before)
    if category_new_value:
        category_obj_main = models.category_choeses.objects.get(category_id_main=category_new_value)
        product.category_choeses=category_obj_main
    else:
        category_obj_main = category_obj_main[0]
    
    
    
    
    if video_link is not None:
        product.video_link = video_link
        
    if video_file is not None:
        product.video = video_file
        


        
    for i in range(0, int(sub_categories_len)):
        subcategory = product.sub_categories.all()
        
        pk =  request.POST.get(f"pk{i}")
       
        subcategory_ru = subcategory.filter(pk=pk)
        subcategory_ru.update(name=request.POST.get(f"sub_category_name_ru{i}"),name_am=request.POST.get(f"sub_category_name_am{i}"),name_en=request.POST.get(f"sub_category_name_en{i}"))
            
        

    for i in range(0, int(images_len_delete)):
        
        
        models.productsimage.objects.filter(pk=request.POST.get(f'img_num_del{i}')).delete()
    for i in range(0, int(img_len)):

        
        data = request.FILES.get(f'images{i}')
        
        models.productsimage.objects.create(post = product,avatar_e=data)
    if int(main_image_delete) == 1:
        avatar = models.productsimage.objects.filter(post=product)[0]
        product.avatar_p = avatar.avatar_e
        avatar.delete()
       
    
    
    category_obj = category_obj_main
    

    if table_len_counter is not None:
        product.counter_props.clear()
        
        for i in range(0, int(table_len_counter)):
            
            price = request.POST.get(f'counter_price{i}')
            counter_props = models.counter_props.objects.create(counter_price=price, counter_prop = request.POST.get(f'counter_prop{i}'))
            if product.sale:
                counter_props.counter_price_sale = int(int(float(price))*((100-int(product.sale))))/100
            if int(request.POST.get(f'counter_prop{i}'))==1:

                    product.price  = float(price)
                    if product.sale:
                        product.sale_price = int(int(float(price))*((100-int(product.sale))))/100


            
            product.counter_props.add(counter_props)
    
    if table_len_size != 0 and table_len_size is not None:
        product.min_size = int(request.POST.get("min_size"))

        price = int(request.POST.get("price_size"))
        product.price_size = price

        if product.sale_price_size:
            product.sale_price_size = int(int(price)*(100-int(product.sale)))/100
       
        product.max_size = int(request.POST.get("max_size"))
    elif table_len_size_pcs is not None:
        
        price = int(request.POST.get("price_size_pcs"))
        product.price_pcs = price
        if product.sale_price_pcs:
            product.sale_price_pcs = int(int(price)*(100-int(product.sale)))/100
    

    product.save()

    return JsonResponse("data", safe=False)





def checkout_delivery(request, pk):
    
    delyvery = get_object_or_404(models.delivery_check, pk=pk)
    if not delyvery.my_contacts_info:
        my_contacts_info=models.my_contacts_info.objects.filter(profile=request.user.profile).order_by('-pk')
        zone_countries = models.zone_countries.objects.filter()
    else:
        my_contacts_info=None
        zone_countries=None
        

    return render(request, "template_rus/delyvery_check.html", {"delyvery":delyvery, "my_contacts_info":my_contacts_info, "zone_countries":zone_countries})

def add_comment_product(request):
    comment = request.POST.get("comment")
    lens = request.POST.get("lens")
    images_switch = 0
    


    
    stars = request.POST.get("stars")


    
    if stars is None:
        stars=0
    files_len = request.POST.get("files_len")

   
    comment_model = models.products_comment.objects.create(profile = request.user.profile, description = comment, stars=stars)
    if files_len is not None:
        
        
        for i in range(0, int(files_len)):
        
        
            images = models.products_commets_images.objects.create(image=request.FILES.get(f'file{i}'))
            comment_model.products_commets_images.add(images)
        images.save()
    

    data = {
        "comment":comment_model.description,
        "create_date":comment_model.created_at,
        "profile":comment_model.profile.first_name,
        "images_switch":images_switch,
        
        "pk":comment_model.pk
    }
    return JsonResponse(data, safe=False)

def delete_cart_all_product(request):
    profile = get_object_or_404(models.Profile, user = request.user)
    pk = request.POST.get("pk", None)
    if pk is not None:
        product=profile.product_cart.get(pk=pk)
        profile.product_cart.remove(product)
        

        profile.save()
    else:
        products_carts = profile.product_cart.all().delete()
        profile.product_cart.clear()
        profile.save()
    return JsonResponse("data", safe=False)

def remove_cart_product(request):
    pk = request.POST.get("pk")
    
    product = get_object_or_404(models.products, pk = pk)
    profile = get_object_or_404(models.Profile, user = request.user)
    count = models.products_cart.objects.filter().count()

    
    if models.products_cart.objects.filter(product=product).exists():

        add_product_cart = models.products_cart.objects.get(product=product).delete()
        data = {
            "data":1,
            
            "count":int(count)-1, 
             "price":product.price
            
           


        }
    else:
        data = {
            "data":0,
            
            "count":int(count)-1, 
            "price":product.price
        }

    
    return JsonResponse(data, safe=False)


def change_account(request):
    first_name = request.POST.get("first_name")

    profile = get_object_or_404(models.Profile, pk=request.user.profile.pk)
    profile.first_name = first_name
    profile.save()
    data = {
        "success":1
    }

    return JsonResponse(data, safe=False)
def search_my_checkout_with_country(request):
    country = request.POST.get("country")
    my_contacts_info = models.my_contacts_info.objects.filter(country=country)

    products = models.checkout_products.objects.filter(Q(delivery_check__my_contacts_info__in=my_contacts_info) &  (Q(status="pay") | Q(status="collectionpay") |  Q(status="send") | Q(status="unsend") | Q(status="joint") | Q(status="joint_green"))).order_by('-date_ordered')
    products=CheckoutSerializer(products, many=True)
    

    return JsonResponse(products.data,safe=False)
def search_my_checkout(request):
    
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        if search_text is not None and search_text != u"":

            
            text = re.escape(search_text)
            if request.user.is_superuser:
                products = models.checkout_products.objects.filter(Q(order_id__iregex = r"(^|\s)%s" % text) & (Q(status="pay") | Q(status="collectionpay") |  Q(status="send") | Q(status="unsend") | Q(status="joint") | Q(status="joint_green"))).order_by('-date_ordered')
            else:
                products = []
        else:
            products=models.checkout_products.objects.filter(Q(status="pay") | Q(status="collectionpay") |  Q(status="send") | Q(status="unsend") | Q(status="joint") | Q(status="joint_green")).order_by('-date_ordered')
    else:
        products=[]
    


    products=CheckoutSerializer(products, many=True)
    
    
    
    

        
            
            

        


    return JsonResponse(products.data,safe=False)

def search_my_products(request):
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        if search_text is not None and search_text != u"":

            
            text = re.escape(search_text)
            if request.user.is_superuser:
                products = models.products.objects.filter(name_ru__iregex = r"(^|\s)%s" % text).exclude().order_by()
            else:
                products = []
        else:
            products=models.checkout_products.objects.filter(Q(status="pay") | Q(status="collectionpay") |  Q(status="send") | Q(status="unsend") | Q(status="joint") | Q(status="joint_green")).order_by('-date_ordered')
    else:
        products=[]

    products=ArticleSerializer(products, many=True)
    

        
            
            

        

    return JsonResponse(json.dumps(products.data),safe=False)
def search_category_api(request):
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        search_color = request.POST.get('search_color')
        search_size =  request.POST.get('search_size')
        


        if search_text is not None and search_text != u"":

            
            text = re.escape(search_text)
            if search_color is  None:
                search_color = ""
            if search_size is  None:
                search_size = ""
            


            if request.user.is_superuser:
                

                products = models.products.objects.filter(Q(name_ru__iregex = r"(^|\s)%s" % text) | Q(name_am__iregex = r"(^|\s)%s" % text) | Q(name_en__iregex = r"(^|\s)%s" % text)).exclude().order_by()
            else:
                
                products = models.products.objects.filter(Q(name_ru__iregex = r"(^|\s)%s" % text) | Q(name_am__iregex = r"(^|\s)%s" % text) | Q(name_en__iregex = r"(^|\s)%s" % text)).exclude().order_by()

            data = list()
            
            
            products = products.filter(Q(color__iregex=search_color))
        else:
            data = list()
            
            
        products=ArticleSerializer(products, many=True)

        
            
            

        return JsonResponse(json.dumps(products.data),safe=False)
            

        

def get_categories(request):
    pk = request.POST.get("category_pk")
    



    category=get_object_or_404(models.category_choeses, category_id_main=pk)

    categorys = models.category_choeses.objects.filter(parent=category)
    
    return JsonResponse(serializers.serialize('json', categorys),safe=False)
def orders_view(request, pk):
    checkout = get_object_or_404(models.checkout_products, pk=pk)

   
    return render(request, "template_rus/orders_view.html", {"checkout":checkout})
def about_us(request):
    about_us = models.about_us.objects.all().last()
    return render(request, "template_rus/about_us.html",{"about_us":about_us})
def delivery_info(request):
    delivery_info = models.delivery_info.objects.all().last()
    return render(request, "template_rus/delyvery_us.html",{"about_us":delivery_info}) 
    
def reviews(request):
    comments = models.products_comment.objects.all()
    number_of_item = 10
    paginatorr = Paginator(comments, number_of_item)

    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range

    

    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)
        results = paginatorr.page(page_n).object_list.filter()
        statuss_se=CommentsSerializer(results, many=True)


        return JsonResponse({"results":statuss_se.data})
    return render(request, "template_rus/reviews.html", {"comments":first_page}) 

def rules(request):
    about_us = models.rules.objects.all().last()
    return render(request, "template_rus/rules.html", {"about_us":about_us}) 
def apisearch_product(request):

    if request.method == "POST":
        search_text = request.POST.get('search_text')
        categroy_value = request.POST.get("categroy_value")
        if search_text is not None and search_text != u"":
            



            search_text = request.POST.get('search_text')
            text = re.escape(search_text)
            if request.user.is_superuser:
                products = models.products.objects.filter(Q(name_ru__iregex = r"(^|\s)%s" % text) | Q(name_ru__iregex = r"(^|\s)%s" % text) | Q(name_am__iregex = r"(^|\s)%s" % text) | Q(name_en__iregex = r"(^|\s)%s" % text) | Q(description_arm__iregex = r"(^|\s)%s" % text) | Q(description_rus__iregex = r"(^|\s)%s" % text) | Q(description_eng__iregex = r"(^|\s)%s" % text) | Q(color__iregex = r"(^|\s)%s" % text) | Q(color_id__iregex=r"(^|\s)%s" % text)).exclude().order_by()
            else:
                products = models.products.objects.filter(Q(name_ru__iregex = r"(^|\s)%s" % text) | Q(name_ru__iregex = r"(^|\s)%s" % text) | Q(name_am__iregex = r"(^|\s)%s" % text) | Q(name_en__iregex = r"(^|\s)%s" % text) | Q(description_arm__iregex = r"(^|\s)%s" % text) | Q(description_rus__iregex = r"(^|\s)%s" % text) | Q(description_eng__iregex = r"(^|\s)%s" % text) | Q(color__iregex = r"(^|\s)%s" % text) | Q(color_id__iregex=r"(^|\s)%s" % text)).exclude().order_by()
            
            if len(categroy_value)>0:
                category_choeses = models.category_choeses.objects.filter(category_id_main=categroy_value)

                products=products.filter(category_choeses__in=category_choeses)
            
            
        else:
            data = list()
            
            
        
        statuss_se=ArticleSerializer(products, many=True)
        
            
            

        return JsonResponse(json.dumps(statuss_se.data),safe=False)
       


def add_checkout(request):
    step = 0
    data_form =request.POST.getlist('data')
    shipping_address  = request.POST.get("shipping_address")
    
    pk_list_product = data_form[0].split(",")
    count_product_array = request.POST.getlist('count_product_array')
    count_product = count_product_array[0].split(",")
    
    profile = get_object_or_404(models.Profile, pk=request.user.profile.pk)
    profile.checkout_products_list.clear()

    for i in pk_list_product:
        product = get_object_or_404(models.products, pk = int(i))
        orders_pr = models.products_Order.objects.create(customer=request.user.profile, product = product, transaction_id=generate_key_check(10, 12), count=(int(count_product[step])), price=float(product.price)*(int(count_product[step])), shipping_address=shipping_address)
        profile.checkout_products_list.add(orders_pr)
        step+=1
        profile.save()
    

    data = {
    "data":1


    }
    return JsonResponse(data, safe=False)

def change_shipping_address(request):
    
    address_my = request.POST.get("address_my")
    number_phone = request.POST.get("number_phone")
    reciver_name = request.POST.get("reciver_name")
    zip_code = request.POST.get("zip_code")
    Country = address_my.split("/")
    reciver_name = reciver_name.replace("/", " ")
   

    address = models.shipping_address.objects.create(address=address_my,zipcode=zip_code, res_name=reciver_name,profile=request.user.profile, Country=Country[0])

    data = {
    "success":1,
    "address":address.address,
    "Country":Country
    }
    return JsonResponse(data, safe=False)

def search_category(request, category_name):
    if request.user.is_superuser:
    
        obj = models.products.objects.filter(category=category_name)
    else:
        obj = models.products.objects.filter(Q(category=category_name) & Q(approved="True"))

    obj_max_price = obj.order_by('-price')
    
    colors =list(dict.fromkeys([x[0] for x in obj.values_list("color")])) 
    sizes =list(dict.fromkeys([x[0] for x in obj.values_list("size")])) 
    if len(obj_max_price)>0:
        max_price =int(obj_max_price[0].price) 
        min_price = int(obj_max_price[len(obj_max_price)-1].price)
    else:
        max_price =0
        min_price = 0


   


    return render(request, "template_rus/search_result.html", {"products":obj, "max_price":max_price, "min_price":min_price, "colors":colors[:6], "sizes":sizes[:6], "category_name":category_name,"category_status":"true"})
def search_category(request, category_name):
    if request.user.is_superuser:
    
        obj = models.products.objects.filter(category=category_name)
    else:
        obj = models.products.objects.filter(Q(category=category_name) & Q(approved="True"))

    obj_max_price = obj.order_by('-price')
    
    colors =list(dict.fromkeys([x[0] for x in obj.values_list("color")])) 
    sizes =list(dict.fromkeys([x[0] for x in obj.values_list("size")])) 
    if len(obj_max_price)>0:
        max_price =int(obj_max_price[0].price) 
        min_price = int(obj_max_price[len(obj_max_price)-1].price)
    else:
        max_price =0
        min_price = 0


   


    return render(request, "template_rus/search_result.html", {"products":obj, "max_price":max_price, "min_price":min_price, "colors":colors[:6], "sizes":sizes[:6], "category_name":category_name,"category_status":"true"})
def shop(request):
    
    if request.user.is_superuser:
    
        products = models.products.objects.filter()
    else:
        products = models.products.objects.filter(approved="True")

    obj_max_price = products.order_by('-price')
    
    colors =list(dict.fromkeys([x[0] for x in products.values_list("color")])) 
    sizes =list(dict.fromkeys([x[0] for x in products.values_list("size")])) 
    if len(obj_max_price)>0:
        max_price =int(obj_max_price[0].price) 
        min_price = int(obj_max_price[len(obj_max_price)-1].price)
    else:
        max_price =0
        min_price = 0
    return render(request, "template_rus/search_result.html", {"products":products, "max_price":max_price, "min_price":min_price, "colors":colors[:6], "sizes":sizes[:6]})

def filter_products(request):
    price_max = request.POST.get("price_max")
    price_min = request.POST.get("price_min")
    sizes = request.POST.getlist("sizes")
    colors = request.POST.getlist("colors")
    category_name = request.POST.get("category_name")
    category_status = request.POST.get("category_status")
    
    colors = colors[0].split(",")
    sizes = sizes[0].split(",")
    if category_status=="true":
        
        if colors[0]!='' or sizes[0]!='':
            obj = models.products.objects.filter(Q(price__gte=price_min) & Q(price__lte=price_max) & Q(color__in=colors) & Q(size__in=sizes)).filter(category=category_name)
        else:

            

        
        
            obj = models.products.objects.filter(Q(price__gte=price_min) & Q(price__lte=price_max)).filter(category=category_name)
    else:
        
        if colors[0]!='' or sizes[0]!='':
            obj = models.products.objects.filter(Q(price__gte=price_min) & Q(price__lte=price_max) & Q(color__in=colors) & Q(size__in=sizes)).filter(name__icontains=category_name)
        else:

            

        
        
            obj = models.products.objects.filter(Q(price__gte=price_min) & Q(price__lte=price_max)).filter(name__icontains=category_name)
   
    if not request.user.is_superuser:
        
        obj=obj.filter(approved="True")

    return JsonResponse(serializers.serialize('json', obj), safe=False)




def change_approved_status(request):
    pk = request.POST.get("pk")
    status = request.POST.get("status")

    if status=="False":
        description = request.POST.get("description")
        product = get_object_or_404(models.products,pk=pk)
        product.approved = str(status)
        product.approved_description = description
        product.save()
            
    else:

        product = get_object_or_404(models.products,pk=pk)
        product.approved = str(status)
        product.save()
    


    data = {
        "data":1
    }
    return JsonResponse(data,safe=False)
