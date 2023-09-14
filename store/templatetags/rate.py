from django import template
from django.conf import settings
from django.utils import timezone
from store.models import rates, favorite_products,products
from django.db.models import Q
from django.shortcuts import get_object_or_404


register = template.Library()

@register.filter(name='SET_DEFAULT_CURRENCY_CODE')
def SET_DEFAULT_CURRENCY_CODE(request):
    return request.COOKIES.get(settings.DEFAULT_CURRENCY_CODE, settings.DEFAULT_CURRENCY_CODE)

@register.filter(name='Get_pay_rate')
def Get_pay_rate(request):
    # Use timezone.now() - timezone.timedelta(days=1) directly in filter
    get_rates = rates.objects.filter(date_updates__lte=timezone.now() - timezone.timedelta(days=1), rate_name__in=["USD", "RUR", "EUR"])
    if len(get_rates) > 0:
    	from store.scheduler.scheduler import deactivate_expired_accounts
    	deactivate_expired_accounts()

        

    currency_code = SET_DEFAULT_CURRENCY_CODE(request)
    rate = 1
    
    # Create a dictionary to map currency codes to rate names
    currency_to_rate = {
        "ENG": "USD",
        "ARM": "AMD",
        "RUR": "RUR",
        "EUR": "EUR",
    }
    
    rate_name = currency_to_rate.get(currency_code, "USD")  # Default to USD if currency not found
    rate_obj = rates.objects.filter(rate_name=rate_name).first()

    if rate_obj:
        rate = rate_obj.rate
    
    return rate, currency_code

@register.filter(name='check_favorite')
def check_favorite(profile, pk):
    product = get_object_or_404(products, pk=pk)
    if favorite_products.objects.filter(Q(profile = profile) & Q(product=product)).exists():

        return True
    else:
        return False

