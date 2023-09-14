from django import template
from django.db.models import Q
from store.models import checkout_products


register = template.Library()

@register.filter(name='checkcollection')
def checkcollection(profile):
    checkout_last = checkout_products.objects.filter(Q(profile=profile) & (Q(status="pay") | Q(status="collectionpay")) & ~Q(delivery_check__pay_status="delyverypay")).order_by("-date_ordered").last()
    collections_indikator = None
    if checkout_last:
    	collections_indikator = True

    return collections_indikator

