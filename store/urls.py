from django.urls import path, include

from . import views
from django.conf.urls import url

app_name = 'accounts'



urlpatterns = [
   
    path('', views.home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('orders/', views.orders, name="orders"),
    
    path('blog/', views.blog, name="blog"),
    path('about_us/', views.about_us, name="about_us"),
    path('delivery_info/', views.delivery_info, name="delivery_info"),
    path('add_about_us/', views.about_new, name="about_new"),
    path('edit_about_us/<pk>', views.about_edit, name="about_edit"),
    path('add_delivery_info/', views.delivery_info_new, name="delivery_info_new"),
    path('add_price_of_deliverybox/', views.price_of_deliverybox, name="delivery_box_money"),
    path('order_detalis/<pk>', views.order_detalis, name="order_detalis"),
    path('change_delivery_price/<pk>', views.change_delivery_price, name="change_delivery_price"),
    
    
    path('edit_delivery_info/<pk>', views.delivery_info_edit, name="delivery_info_edit"),
    path('add_rules/', views.rules_new, name="rules_new"),
    path('edit_rules/<pk>', views.rules_edit, name="rules_edit"),
    path('rules/', views.rules, name="rules"),
    path('reviews/', views.reviews, name="reviews"),
    path('blog_article/<pk>/', views.blog_article, name="blog_article"),
    path('language/activate/<language_code>/', views.ActivateLanguageView.as_view(), name='activate_language'),
    
    path('my_account/', views.my_account, name="my_account"),
    
    
    path('shop/products/<pk>/', views.product_detalis_view, name="product_detalis_view"),
    
    
    path('shop_products/', views.shop_products, name="shop_products"),
    path('my_products/', views.my_products, name="my_products"),
    path('my_checkout_products/', views.my_checkout_products, name="my_checkout_products"),
    path('check/<pk>', views.check, name="check"),
    
    
    path('shop_products/category/<categoryid>', views.shop_products_category, name="shop_products_category"),
    
    #path('shop_products/subcategory/<categoryid>', views.shop_products_subcategory, name="shop_products_subcategory"),
    path('products_of_day/', views.products_of_day, name="day_of_products"),
    path('new/', views.new_products, name="new_products"),
    path('brand_products/<Brand_id>', views.brand_products, name="brand_products"),
    path('add_day_of_products/', views.add_day_of_products, name="add_day_of_products"),
    path('add_brand/', views.add_brand, name="add_brand"),
    path('products_of_brands/', views.all_brands_product, name="all_brands_product"),
    

    
    
    path('add_product_page/', views.add_product_page, name="add_product_page"),
    path('add_product_page_size/', views.add_product_page_size, name="add_product_page_size"),
    path('add_product_page_size_pcs/', views.add_product_page_size_pcs, name="add_product_page_size_pcs"),
    path('add_blog/', views.post_new, name="add_blog"),
    path('blog_edit/<pk>/', views.post_edit, name="blog_edit"),

    
    
    
    path('add_zones/', views.add_zones, name="add_zones"),
    
    
    path('address_book/', views.address_book, name="address_book"),
    path('favorite/', views.favorite, name="favorite"),
    path('add_slides/', views.add_slides, name="add_slides"),
    path('add_price_for_shipping/', views.add_price_for_shipping, name="add_price_for_shipping"),
    

    
    path('cart_page/', views.cart_page, name="cart_page"),
    path('checkout/', views.checkout_page, name="checkout_page"),
    path('max_per_order/', views.max_per_order, name="max_per_order"),
    
    path('change_product/<pk>/', views.change_product_page, name="change_product_page"),

    path('collection_view/', views.collection_view, name="collection_view"),
    path('orders_view/<pk>', views.orders_view, name="orders_view"),
    path('checkout_delivery/<pk>', views.checkout_delivery, name="checkout_delivery"),
    path('confirm/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('confirm_reset/<uidb64>/<token>/', views.confirm_reset_password, name='confirm_reset_password'),
    
    
    
    
    

    path('sign_in/', views.login_page, name="login_page"),
    path('sign_up/', views.sign_up_page, name="sign_up_page"),
    path('recovery_password/', views.password_recovery_page, name="password_recovery_page"),
    path('new_password_page/', views.new_password_page, name="new_password_page"),
    

    
   
    path('categories/<category_name>/', views.search_category, name="search_category"),

    
    path('error404', views.error404, name="error404"),
    path('checkout_shipping_collection/<pk>', views.checkout_collection_page, name="checkout_collection_page"),

    path('api/sign_up/', views.registration, name="registration"),
    path('api/sign_in/', views.sign_in, name="sign_in"),
    path('api/sign_out/', views.sign_out, name="sign_out"),
    path('api/send_recovery_via_email/', views.send_recovery_via_email, name="send_recovery_via_email"),
    

    
    path('api/check_max_count_product/', views.check_max_count_product, name="check_max_count_product"),
    path('api/add_images_for_categories/', views.add_images_for_categories, name="add_images_for_categories"),
    path('api/add_categories/', views.api_add_categories, name="add_categories"),
    
    
    path('api/get_categories/', views.get_categories, name="get_categories"),
    path('api/add_images_for_home_page_slide/', views.add_images_for_home_page_slide, name="add_images_for_home_page_slide"),
    
    
    path('api/delete_cart_all_product/', views.delete_cart_all_product, name="delete_cart_all_product"),
    path('note/<int:pk>/', views.post_detail, name='post_detail'),
    path('note/new/', views.post_new, name='post_new'),
    path('api/product_isactive/', views.product_isactive, name="product_isactive"),
    path('api/add_order/', views.add_order, name="add_order"),
    path('api/add_product_view/', views.add_product_api, name="add_product_view"),
    path('api/add_product_view_change/', views.add_product_change_api, name="add_product_view_change"),
    path('api/product_delete/', views.product_delete, name="product_delete"),
    path('api/search_my_products/', views.search_my_products, name="search_my_products"),
    
    path('api/add_blog_view/', views.add_blog_view, name="add_blog_view"),
    path('api/add_comment_product/', views.add_comment_product, name="add_comment_product"),
    path('api/add_cart_product/', views.add_cart_product, name="add_cart_product"),
    path('api/remove_cart_product/', views.remove_cart_product, name="remove_cart_product"),
    
    path('api/add_favorite_products/', views.add_favorite_products, name="add_favorite_products"),
    path('api/new_register_password/', views.new_register_password, name="new_register_password"),
    
    
    
    path('api/change_account/', views.change_account, name="change_account"),
    path('api/search_product/', views.apisearch_product, name="apisearch_product"),
    path('api/search_category_api/', views.search_category_api, name="search_category_api"),
    
    
    path('api/add_checkout/', views.add_checkout, name="add_checkout"),
    path('api/change_shipping_address/', views.change_shipping_address, name="change_shipping_address"),
    
    path('api/change_approved_status/', views.change_approved_status, name="change_approved_status"),
    
    path('api/delete_product/', views.delete_product, name="delete_product"),
    path('api/filter_products/', views.filter_products, name="filter_products"),
    path('api/search_my_checkout/', views.search_my_checkout, name="search_my_checkout"),
    
    path('api/remove_zones/', views.remove_zones, name="remove_zones"),
    
    path('api/delete_blog/<pk>/', views.delete_blog, name="delete_blog"),
    path('api/add_user_info/', views.add_user_info, name="add_user_info"),
    path('api/change_user_info/', views.change_user_info, name="change_user_info"),
    path('api/add_check_api/', views.add_check_api, name="add_check_api"),
    path('api/remove_collection/', views.remove_collection, name="remove_collection"),
    path('api/add_shipping_price/', views.api_add_shipping_price, name="api_add_shipping_price"),
    path('api/change_shipping_price/', views.change_shipping_price, name="change_shipping_price"),
    
    path('api/remove_shipping_price/', views.remove_shipping_price, name="remove_shipping_price"),
    
    
    path("api/check_payment", views.check_payment, name="check_payment"),
    path("api/pay_delivery_api/", views.pay_delivery_api, name="pay_delivery_api"),
    path("api/check_payment_delyvery/", views.check_payment_delyvery, name="check_payment_delyvery"),
    
    
    path("api/product_is_send/", views.product_is_send, name="product_is_send"),
    path("api/add_zones/", views.api_add_zones, name="api_add_zones"),
    path("api/get_ship_price/", views.get_ship_price, name="get_ship_price"),
    path("api/add_max_per/", views.add_max_per, name="add_max_per"),
    path("api/add_sales/", views.add_sales, name="add_sales"),
    path("api/add_brand/", views.add_brand, name="add_brand_api"),
    path("api/delete_brand/", views.delete_brand, name="delete_brand"),
    path("api/send_email/", views.send_email, name="send_email"),
    path("api/delete_comments/", views.delete_comments, name="delete_comments"),
    path("api/change_brand/", views.change_brand, name="change_brand"),
    
    
    
    path("api/create_delivery/<pk>/", views.create_delivery, name="create_delivery"),
    path("api/create_joint_delivery/<pk>/", views.create_joint_delivery, name="create_joint_delivery"),
    
    path("api/get_category_ids/", views.get_category_ids, name="get_category_ids"),
    path("api/delete_address_book/", views.delete_address_book, name="delete_address_book"),
    path("api/add_day_of_products_api/", views.add_day_of_products_api, name="add_day_of_products_api"),
    path("api/change_currency_symbol/<new_currency_symbol>/", views.change_currency_symbol, name="change_currency_symbol"),
    path("api/add_delivery_box_money/", views.add_delivery_box_price, name="add_delivery_box_money"),
    path("api/change_delivery_box_mass/", views.change_delivery_box_mass, name="change_delivery_box_mass"),
    path("api/remove_delivery_box_mass/", views.remove_delivery_box_mass, name="remove_delivery_box_mass"),
    path("api/change_delivery_price/", views.apichange_delivery_price, name="apichange_delivery_price"),
    path("api/search_my_checkout_with_country/", views.search_my_checkout_with_country, name="search_my_checkout_with_country"),
    
    path("api/assembled/", views.assembled, name="assembled"),
    path("api/change_profile/", views.change_profile, name="change_profile"),

    
    
    
    #path('api/search_category/', views.search_category, name="search_category"),


    
    
    
    
    

    
    
    


    


    
    

    











    
   


    #url(r'^edit_favorites/', views.edit_favorites , name='aa'),
]

