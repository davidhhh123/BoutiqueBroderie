from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def add_order(request):
    profile = get_object_or_404(models.Profile, pk=request.user.profile.pk)
    profile.checkout_products_list.clear()
    data = []
    
    for index, product_cart in enumerate(request.user.profile.product_cart.all()):
        cart_pk = int(request.POST.get(f'cart_pk{index}'))
        
        if int(product_cart.pk) != cart_pk:
            profile.checkout_products_list.clear()
            profile.save()
            break
        
        cart_count = int(re.findall(r'\d+', request.POST.get(f'count{index}'))[0])
        
        if product_cart.indicator == "size":
            count = cart_count or product_cart.count_size
            price = (count / product_cart.product.min_size) * (
                product_cart.product.sale_price_size
                if product_cart.product.sale_price_size
                else product_cart.product.price_size
            )
        elif product_cart.indicator == "counter":
            price = None
            count = cart_count or product_cart.count
            
            for j in product_cart.product.counter_props.all().order_by("counter_prop"):
                if int(count) >= int(j.counter_prop):
                    price = float(j.counter_price_sale or j.counter_price)
                    break
            price = count * price if price is not None else 0
        elif product_cart.indicator == "count":
            count = cart_count or product_cart.count
            price = count * (
                product_cart.product.sale_price
                if product_cart.product.sale_price
                else product_cart.product.price
            )
        elif product_cart.indicator == "size_pcs":
            count = cart_count or product_cart.count
            price = count * (
                product_cart.product.sale_price_pcs
                if product_cart.product.sale_price_pcs
                else product_cart.product.price_pcs
            )
        else:
            continue
        
        orders = models.products_Order.objects.create(
            product=product_cart.product,
            customer=request.user.profile,
            count_size=count if product_cart.indicator == "size" else count,
            price=price,
            indicator=product_cart.indicator,
        )
        profile.checkout_products_list.add(orders)
        data.append({"product_id": product_cart.product.pk, "count": count, "price": price})
    
    profile.save()
    return JsonResponse(data, safe=False)
