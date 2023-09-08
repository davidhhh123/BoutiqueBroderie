from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.db.models import Sum
from froala_editor.fields import FroalaField
from django_resized import ResizedImageField
register = template.Library()



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    
    email = models.EmailField(default='none@email.com')
    birth_date = models.DateField(default='1999-12-31')
    
    city = models.CharField(max_length=40, default='')
    state = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    product_cart = models.ManyToManyField('products_cart', related_name="product_cart_c")
    shipping_address = models.ManyToManyField('shipping_address', related_name = 'shipping_address')
    receiver = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=20, default="")
    zipcode = models.CharField(max_length=10, default="")
    
    
    

    checkout_products_list = models.ManyToManyField('products_Order', related_name='products_Orders')
    

    

    
    

    def __str__(self):
        return self.user.username

    def get_sum_price(self):
        sums = 0
        product =  self.product_cart.filter(profile__user = self.user)

        
        for i in product:
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
                print(i.count*price, "i.count*price", i.count, price)
            elif i.indicator=="size_pcs":
                if i.product.sale_price_pcs:
                    sums+=i.count*i.product.sale_price_pcs
                else:

                    sums+=i.count*i.product.price_pcs
                print(i.product.price_pcs, "i.product.price_pcs")
            elif i.indicator=="count":
                if i.product.sale_price:
                    sums+=i.count*i.product.sale_price
                else:

                    sums+=i.count*i.product.price
                
            else:
                pass



          
           
            
        print(sums)
        return sums
    def get_cart_product_count(self):

        product_count =  self.product_cart.filter(profile__user = self.user).count()
        
        
        
        return product_count

    def get_favorite_products_count(self):
        count = 0
        product_count =  favorite_products.objects.filter(profile__user = self.user).count()
        
        
        
        
        
        
        return product_count

    


   





   



      




def create_profile(sender, **kwargs):
    
    
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])

       
       



       



        


       


post_save.connect(create_profile, sender=User)
class categories(models.Model):
    name =  models.CharField(max_length=15)
    
    def __str__(self):
        return self.name


class shipping_address(models.Model):
    profile = models.ForeignKey(Profile , on_delete = models.CASCADE , null=True, related_name="Store_shipping_address")
    address =  models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10, default="")
    res_name = models.CharField(max_length=80, default="")
    Country=models.CharField(max_length=20, default="")
    def __str__(self):
        return self.address

class sub_category(models.Model):

    descendant = models.CharField(max_length=50)

    name = models.CharField(max_length=50)
    category_deg = models.PositiveIntegerField(default = '0')
    products_count = models.PositiveIntegerField(default = '0')

class Visit(models.Model):
    visits = models.PositiveIntegerField(default = 0)
    
    visits_one_day = models.PositiveIntegerField(default = 0)
    visits_last = models.PositiveIntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)
    


class category_choeses(models.Model):
    
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50,default="")
    name_am = models.CharField(max_length=50,default="")
    category_id =  models.CharField(max_length=7, default="")
    category_id_main =  models.CharField(max_length=14, default="")


    
    products_count = models.PositiveIntegerField(default = 0)
    image = models.FileField(
        
        default = '',
        
    )
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
class about_us(models.Model):
    description = FroalaField(theme='dark', default="")
    description_am = FroalaField(theme='dark', default="")
    description_en = FroalaField(theme='dark', default="")
class delivery_info(models.Model):
    description = FroalaField(theme='dark', default="")
    description_am = FroalaField(theme='dark', default="")
    description_en = FroalaField(theme='dark', default="")
class rules(models.Model):
    description = FroalaField(theme='dark', default="")
    description_am = FroalaField(theme='dark', default="")
    description_en = FroalaField(theme='dark', default="")

class Blog(models.Model):
    name_ru = models.CharField(max_length=70, default='')
    name_am = models.CharField(max_length=70, default='')
    name_en = models.CharField(max_length=70, default='')
    #text = FroalaField(theme='dark', default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    
    blog_id = models.TextField(default='')
    description_arm = FroalaField(theme='dark', default="")
    description_rus = FroalaField(theme='dark', default="")
    description_eng = FroalaField(theme='dark', default="")
    avatar_p = models.FileField(
        
        default = '',
        
    )
    video = models.FileField(
        
        default = '',
        
    )
    def __str__(self):
        return self.name_ru

class sizes_props(models.Model):
    size_name = models.CharField(max_length=50, default='')
    size_prop = models.CharField(max_length=50, default='')
    size_price = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.size_name
class counter_props(models.Model):
    counter_name = models.CharField(max_length=50, default='')
    counter_prop = models.CharField(max_length=50, default='')
    counter_price = models.CharField(max_length=50, default='')
    counter_price_sale = models.FloatField(default=0)

    

    

class mass_props(models.Model):
    mass_name = models.CharField(max_length=50, default='')
    mass_prop = models.CharField(max_length=50, default='')
    mass_price = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.mass_name
class Brand(models.Model):
    brand = models.CharField(max_length=20, default='')
    brand_picture = ResizedImageField(force_format="WEBP", quality=70, default='', keep_meta=False)
    def __str__(self):
        return self.brand
    

class products(models.Model):
    #profile =  models.ForeignKey(Profile , on_delete = models.CASCADE, related_name = 'profile_product')
    name_ru = models.CharField(max_length=50, default='')
    name_am = models.CharField(max_length=50, default='')
    name_en = models.CharField(max_length=50, default='')
    category_choeses =  models.ForeignKey('category_choeses' , on_delete = models.CASCADE , null=True, related_name="category_choeses_product")
    sub_categories = models.ManyToManyField("category_choeses")
    product_id = models.TextField(default='')
    description_arm = models.CharField(max_length=400, default='')
    description_rus = models.CharField(max_length=400, default='')
    description_eng = models.CharField(max_length=400, default='')
    sale = models.FloatField(default=0, null=True, blank=True)
    sale_price = models.FloatField(default=0, null=True, blank=True)
    mass = models.CharField(max_length=6, default='')
    category =models.CharField(max_length=40, default='')
    size = models.CharField(max_length=30, default='')
    pcs_type = models.CharField(max_length=5, default='')
    
    price = models.FloatField(default="0", null=True, blank=True)
    pcs = models.CharField(max_length=10, default='')
    color = models.CharField(max_length=50, default='')
    Brand = models.ForeignKey('Brand' , on_delete = models.CASCADE , null=True,blank=True, default=None, related_name="Brand_rel")
    active = models.BooleanField(default=False)
    color_id = models.CharField(max_length=50, default='')
    SKU_code = models.CharField(max_length=20, default='')
    sizes_props = models.ManyToManyField("sizes_props")
    min_size = models.PositiveIntegerField(default = 0)
    max_size = models.PositiveIntegerField(default = 0)
    size_pcs = models.PositiveIntegerField(default = 0)
    price_pcs = models.PositiveIntegerField(default = 0)
    price_size = models.PositiveIntegerField(default = 0)
    sale_price_size = models.PositiveIntegerField(default = 0)
    sale_price_pcs=models.PositiveIntegerField(default = 0)
    
    #counter_props = models.ManyToManyField("counter_props")
    #mass_props = models.ManyToManyField("mass_props")
    counter_props = models.ManyToManyField("counter_props")
    
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    view_s = models.PositiveIntegerField(default = '0')
    avatar_p = ResizedImageField(force_format="WEBP", quality=75, default='',size=[400, 400], keep_meta=False)
    video = models.FileField(
        
        default = '',
        
    )
    video_link = models.CharField(max_length=100, default='')
    zoom_image = ResizedImageField(force_format="WEBP", quality=70, default='')

    product_status = models.CharField(max_length=150, default='')
    prop = models.PositiveIntegerField(default = '0')
    prop_type = models.CharField(max_length=5, default='')
    available = models.BooleanField(default=True)



    def __str__(self):
        return self.name_ru
class home_slide(models.Model):
    slide_id = models.CharField(max_length=1, default='')
    image = ResizedImageField(force_format="WEBP", quality=80, default='')
class products_comment(models.Model):
    profile =  models.ForeignKey(Profile , on_delete = models.CASCADE, related_name = 'profile_pro')
    product = models.ForeignKey(products , on_delete = models.CASCADE , null=True, related_name="products_comment")
    description = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    stars = models.PositiveIntegerField(default = '0')
    products_commets_images = models.ManyToManyField('products_commets_images', related_name = 'products_commets_images')
    def __str__(self):
        return self.product.name
class favorite_products(models.Model):
    profile = models.ForeignKey(Profile , on_delete = models.CASCADE, related_name = 'profile_features')
    product = models.ForeignKey(products , on_delete = models.CASCADE, related_name = 'products_features')
    count = models.PositiveIntegerField(default = '0')
    count_size = models.PositiveIntegerField(default = '0')

    
    def __str__(self):
        return self.product.name

class collection(models.Model):
    collection_name = models.CharField(max_length=25, default='')
    profile =  models.ForeignKey(Profile , on_delete = models.CASCADE, related_name = 'profile_collection')
    orders = models.ManyToManyField('products_Order', related_name = 'products_Order_many')
    mass = models.FloatField(default=0)
    checkout_products = models.ManyToManyField('checkout_products', related_name = 'checkout_products_many', blank=True, null=True)
    delivery_check = models.ForeignKey('delivery_check' , on_delete = models.SET_NULL , null=True,blank=True, related_name="delivery_check_collection")
    def __str__(self):
        return self.collection_name
class price_of_deliverybox(models.Model):
    mass_start =  models.PositiveIntegerField(default = '0')
    mass_end =  models.PositiveIntegerField(default = '0')
    total_mass = models.PositiveIntegerField(default = '0')
    
class Mass_and_money(models.Model):
    mass_start =  models.PositiveIntegerField(default = '0')
    mass_end =  models.PositiveIntegerField(default = '0')
    money = models.FloatField(default = '0')
    type= models.CharField(max_length=15, default='')
    zones =  models.ForeignKey('zone' , on_delete = models.CASCADE,null=True,blank=True, related_name = 'zone_class')
class max_cart_price(models.Model):
    price = models.FloatField(default='0')
class zone(models.Model):
    zone_countries = models.ManyToManyField('zone_countries', related_name = 'zone_countries_many')
    zone_number = models.PositiveIntegerField(default = '0')
    def __str__(self):
        return str(self.zone_number)
class zone_countries(models.Model):
    country = models.CharField(max_length=25, default='')



class productsimage(models.Model):
     post = models.ForeignKey(products , on_delete = models.CASCADE , null=True, related_name="productsimages")
     avatar_e = ResizedImageField(force_format="WEBP", quality=70, default='')
     
     def __str__(self):
        return self.post.description

class products_commets_images(models.Model):
    image = models.FileField(
        
        default = '',
        
    )

    def __str__(self):
        return self.products_comments.profile.user.username
class rates(models.Model):
    rate_name = models.CharField(max_length=3)
    rate = models.FloatField(default=1)
    date_updates = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.rate:
            self.date_updates = datetime.now()
        super().save(*args, **kwargs)
class products_Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="Products_orders")
    product = models.ForeignKey(products , on_delete = models.SET_NULL , null=True,blank=True, related_name="order_product")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=10, null=True)
    count  = models.PositiveIntegerField(default = 0)
    count_size = models.PositiveIntegerField(default = 0)
    price = models.FloatField(default="0")
    shipping_address = models.ForeignKey('my_contacts_info' , on_delete = models.SET_NULL , null=True,blank=True, related_name="my_contacts_info_order")
    indicator = models.CharField(max_length=10, null=True)
    avatar_p = ResizedImageField(force_format="WEBP", quality=75, default='',size=[400, 400], keep_meta=False)
    name_ru = models.CharField(max_length=50, default='')
    name_am = models.CharField(max_length=50, default='')
    name_en = models.CharField(max_length=50, default='')


    def __str__(self):
        return str(self.id)

class my_contacts_info(models.Model):
    profile = models.ForeignKey(Profile , on_delete = models.CASCADE , null=True, related_name="contact_info_profile")
    username = models.CharField(max_length=30, default='')
    email=models.CharField(max_length=30, default='')
    phone_number = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=12, default='')
    state = models.CharField(max_length=12, default='')
    city = models.CharField(max_length=12, default='')
    address = models.CharField(max_length=35, default='')
    index = models.CharField(max_length=6, default='')
    def __str__(self):
        return str(self.username)


#prodcuts day and sales

class day_of_product(models.Model):
    product = models.ForeignKey(products , on_delete = models.CASCADE , null=True, related_name="products_day")
class delivery_check(models.Model):
    price = models.FloatField(default=0)
    mass = models.FloatField(default=0)
    pay_status  = models.CharField(default="dontpay", max_length=15)
    order_id = models.CharField(max_length=7, default='')
    my_contacts_info = models.ForeignKey(my_contacts_info, on_delete = models.SET_NULL , null=True,blank=True, related_name="my_contacts_info")
class order_id_count(models.Model):
    order_id = models.CharField(max_length=7, default='')
class checkout_products(models.Model):


    profile = models.ForeignKey(Profile , on_delete = models.CASCADE , null=True, related_name="profile_Order")
    products_Order = models.ManyToManyField(products_Order,related_name="products_Order")
    collection = models.ForeignKey(collection , on_delete = models.SET_NULL , null=True,blank=True, related_name="profile_Order")
    mass = models.PositiveIntegerField(default = '0')
    price = models.CharField(max_length=6, default='')
    transaction_id = models.CharField(max_length=12, default='')
    status = models.CharField(max_length=10, default='')
    assembled=models.CharField(max_length=20, default='notassembled')
    order_id = models.CharField(max_length=7, default='')
    date_ordered = models.DateTimeField(auto_now_add=True)
    delivery_check = models.ForeignKey(delivery_check , on_delete = models.CASCADE , null=True,blank=True, related_name="delivery_check")
    comments = models.CharField(max_length=250, default="")
    my_contacts_info = models.ForeignKey(my_contacts_info, on_delete = models.SET_NULL , null=True,blank=True, related_name="my_contacts_info_check")


    def __str__(self):
        return str(self.id)

class products_cart(models.Model):
    profile =  models.ForeignKey(Profile , on_delete = models.CASCADE, related_name = 'profile_product_cart')

    product = models.ForeignKey(products , on_delete = models.CASCADE, related_name = 'profile_productss', null=True, blank=True)
    count = models.PositiveIntegerField(default = '0')
    count_size = models.PositiveIntegerField(default = '0')
    price = models.FloatField(default = '0')
    indicator = models.CharField(max_length=10, null=True)

    
    
    def __str__(self):
        return self.profile.user.username





