from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from store.models import category_choeses, products, checkout_products,collection
from django.conf import settings

register = template.Library()




@register.filter(name='checkcollection')
def checkcollection(profile):
    checkout_last = get_object_or_404(collection, profile=profile)
    collections_indikator = None
    
    if checkout_last.checkout_products.all():
    	collections_indikator = True

    return collections_indikator



@register.filter(name='checkcounters')
def checkcounters(count, pk):
    product = get_object_or_404(products, pk=pk)
    price = None
    for counter_prop in product.counter_props.filter(counter_prop__lte=count).order_by('-counter_prop'):
        if counter_prop.counter_price_sale:
            price = counter_prop.counter_price_sale
        else:
            price = counter_prop.counter_price
        break
    return price
