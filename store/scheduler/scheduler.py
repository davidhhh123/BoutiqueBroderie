from zeep import Client
from zeep.transports import Transport
from django.shortcuts import get_object_or_404
from store.models import rates
from django.utils import timezone

def deactivate_expired_accounts():
    wsdl_url = "https://services.ameriabank.am/ExchangeRates/srvExchangeRates.svc?wsdl"
    transport = Transport()
    client = Client(wsdl=wsdl_url, transport=transport)
    partner_key = "9nBUZQ434$CKFe#TVm"
    response = client.service.f_ExchangeRates(partner_key=partner_key)

    rate_mappings = {
        "USD": 0,
        "EUR": 2,
        "RUR": 4,
    }
    

    updated_rates = []

    for rate_name, response_index in rate_mappings.items():
        rate_value = float(response[response_index]['cb_rate'])
        rates_model = get_object_or_404(rates, rate_name=rate_name)
        rates_model.rate = rate_value
        rates_model.date_updates = timezone.now()
        updated_rates.append(rates_model)

    rates.objects.bulk_update(updated_rates, ['rate','date_updates'])
    

    # Process the response if needed
