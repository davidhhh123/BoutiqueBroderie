

$("body").addClass("stop-scrolling")
$(window).on( "load", function() {
        $("#loader_page").remove()
        $("body").removeClass("stop-scrolling")
    });


function microAlert(e,i,t){var o=i||3e3,r=$.extend(!0,{css:{},id:null},t),c=(new Date).getTime();$(".micro-alert").length||$("body").append($("<div>",{class:"micro-alert"})),$container=$(".micro-alert");var a="id-micro-alert"+c,n=$("<div>",{class:"micro-alert-item "+a,css:r.css});"string"==typeof r.modificator&&n.addClass("is-"+r.modificator),n.on("click",function(){$(this).remove()}),n.html(e),$container.append(n),setTimeout(function(){$("."+a).remove()},o)}


var search_item_template = `
<a href="<item_url>" class="search_items_a">
<div class="search_item">


                  <div class="bx_img_element">
                              <img data-lazyload="" class=" lazyloaded" src="<image_url>" data-src="https://greenbird.ru/upload/resize_cache/iblock/8f9/80_80_1/gqfoq8krih9ylp9h4n4ltxrnhzcbfzci.jpg">
                          </div>

                          <div class="bx_item_element">
                          
              <span><search_text></span>
                              <div class="bx_item_element_article">
                                </div>
                  <div class="price cost prices">
                    <div class="title-search-price">
                      <div class="price"><price> `+ pay_icon_search +`</div>
                    </div>
                  </div>
                            
               
            </div>

                  
                </div></a>
                `
           const makeAPICall = (searchValue) => {
       
        if (!searchValue) {
            return;
        }
     
        var data = new FormData()
        var text = searchValue
        $(".header__search-field_main").val(text)
        var value_o = searchValue
        data.append("search_text", text)
        $(".header__search__results").html("")
        $(".header__search__results").css("display", "block")
        
        categroy_value = ""
        if($("#selected-value span").attr("value") != undefined){
          var categroy_value = $("#selected-value span").attr("value")
          }

        //console.log($(".search_input_t").eq(1).val().length)
        
        if (text.length>0){
        $.ajax({
                type: "Post",
                url: "/api/search_product/",
                dataType: 'json',
                data: {
                    'search_text' : text,
                    'categroy_value':categroy_value,
                    'csrfmiddlewaretoken': '{{csrf_token}}'
                },
                success(data){
                     searchSuccess(data, value_o)
                }, 
                error(data){
                    console.log("error")
                    $(".header__search__results").css("display", "none")
                }
                
            });}
        else{
        	$(".header__search__results").css("display", "none")

        }
    
}

      function searchSuccess(statuss, value_o)

{
    //console.log("value_o", value_o)
   
   
      



    l = JSON.parse(statuss)
    

if(l != ''){
  for (var i = 0, len = l.length; i < len; ++i) {

        var result = l[i];
        //console.log(len_for_string)
        var str = result['name_ru']
        var price = result['price']
        var image_url = result['avatar_p']
        var item_url = "/shop/products/"+result['id']
        if (result['sale_price'] != 0){
          price = result['sale_price']

        }

        if (parseInt(result['price_pcs']) != 0){
          price = result['price_pcs']
          if (result['sale_price_pcs']){
            price = result['sale_price_pcs']

          }
          

        }
        else if (parseInt(result['price_size']) != 0){
          price = result['price_size']
          if (result['sale_price_size']){
            price = result['sale_price_size']

          }

        }
        else if (result['counter_props'].length > 0){
          var count_er = parseInt(result['counter_props'][0]['counter_prop'])
          var counter_props = result['counter_props'][0]
          
          for (var i_counter =0;i_counter<result['counter_props'].length;i_counter++){
            if (parseInt(result['counter_props'][i_counter]['counter_prop'])<count_er){
              count_er = parseInt(result['counter_props'][i_counter]['counter_prop'])
              counter_props =  result['counter_props'][i_counter]
            }

          }
          price = counter_props["counter_price"]
          if (counter_props["counter_price_sale"] != 0){
            price = counter_props["counter_price_sale"]

          }
          
         
          
        }
        else{

        }
       
       
        search_item = search_item_template.replace("<search_text>", str)
        search_item = search_item.replace("<price>", (parseFloat(price)/parseFloat(pay_rates_search)).toFixed(2))
        
        search_item = search_item.replace("<item_url>", item_url)
        search_item = search_item.replace("<item_url1>", item_url)
        
        search_item = search_item.replace("<image_url>", image_url)
        

        $(".header__search__results").append(search_item)
        //$(".search_res_container").append(box)
        
        
        
    }
   
     
   



}
else{
	

  
  



}



    
    
}
var sidebar_click = false
var template_for_catalog =`  <li class="header__collections-item is-level-1" data-navigation-item="">
                  
                    

                    
                    

                    <a href="#" class="img-ratio img-fit header__collections-photo">
                      <div class="img-ratio__inner">
                        

                        
                         
                        
                      </div>
                    </a>
                  

                  <div class="header__collections-controls">
                    <a href="<url>" class="header__collections-link" data-navigation-link="/collection/dlya-malchikov">
                      <katalog_name>
                    </a>

                    
                  </div>

                  
                </li>`
const debounce = (fn, delay = 500) => {
        let timerId = null;
        return function (...args) {
            clearTimeout(timerId);
            timerId = setTimeout(function () {
                fn.apply(this, args);
            }, delay);
        };
    };

const onInput = debounce(makeAPICall, 500);

    $(".header__search-field_main").on("input", function (e) {
        onInput(e.target.value);
    });






$(".header_mobile .header__collections-link").on("click", function(){
	var data  = new FormData()
	category_pk = $(this).attr("category_pk")
	data.append("category_pk", category_pk)
	 $.ajax({

           
           url: '/api/get_categories/',
           method: "POST",
           data: data,
           
           success: function(data) {
           l = JSON.parse(data)


if(l != ''){
	 $(".header__collections_mobile.sub_category_mobile .grid-list").html("")
  for (var i = 0, len = l.length; i < len; ++i) {

        var result = l[i];
        //console.log(len_for_string)
        
        if (lang_all_page=="ru"){
          var template_for_catalogs =template_for_catalog.replace("<katalog_name>",result['fields']['name']) 

        }
        else if (lang_all_page=="en"){
          var template_for_catalogs =template_for_catalog.replace("<katalog_name>",result['fields']['name_en']) 

        }
        else if (lang_all_page=="hy"){
          var template_for_catalogs =template_for_catalog.replace("<katalog_name>",result['fields']['name_am']) 
          
        }

         
         template_for_catalogs =template_for_catalogs.replace("<url>","/shop_products/category/"+result['fields']['category_id_main']) 
   
    $(".header__collections_mobile.sub_category_mobile .grid-list").append(template_for_catalogs)
        
    }}else{
    	$(".header__collections_mobile.sub_category_mobile .grid-list").html("")

    }

           },
            error: function(daa){$(".header__collections_mobile.sub_category_mobile .grid-list").html("")},
            processData: false,
            contentType: false,


           })
	 $(".js-show-sub-menu").css("display", "block")
	 $(".js-hide-mobile-menu").css("display", "none")
	 
	 $(".header__collections_mobile.header_mobile").addClass("noneshow_collections")

	  $(".header__collections_mobile.header_mobile").removeClass("show_collections")
$(".header__collections_mobile.sub_category_mobile").removeClass("noneshow_collections")
	  $(".header__collections_mobile.sub_category_mobile").addClass("show_collections")
	 

	
	

})
$(".js-show-sub-menu").on("click", function(){
	 $(".js-show-sub-menu").css("display", "none")
	 $(".js-hide-mobile-menu").css("display", "block")
	 $(".header__collections_mobile.header_mobile").removeClass("noneshow_collections")
	  $(".header__collections_mobile.header_mobile").addClass("show_collections")
	  $(".header__collections_mobile.sub_category_mobile").removeClass("show_collections")
	  $(".header__collections_mobile.sub_category_mobile").addClass("noneshow_collections")
	

})
$(".sidebar-collections__link").on("click",function(){
	var data  = new FormData()
	category_pk = $(this).attr("category_pk")
  var this_name = $(this).text()
  var this_url = $(this).attr("url")
  $(".collections_katalog .grid-list.header__collections-menu").html("")
  //var template_for_catalogs =template_for_catalog.replace("<katalog_name>",this_name) 
  //template_for_catalogs =template_for_catalogs.replace("<url>",this_url) 
  if ($(this).attr("request") != undefined){
    var template_for_catalogs =template_for_catalog.replace("<katalog_name>","товары дня") 
         template_for_catalogs =template_for_catalogs.replace("<url>","/day_of_products")
          $(".collections_katalog .grid-list.header__collections-menu").append(template_for_catalogs) 


  }
  else{
	data.append("category_pk", category_pk)
  //$(".collections_katalog .grid-list.header__collections-menu").append(template_for_catalogs)
	 $.ajax({

           
           url: '/api/get_categories/',
           method: "POST",
           data: data,
           
           success: function(data) {

           l = JSON.parse(data)
    

if(l != ''){
	 
  for (var i = 0, len = l.length; i < len; ++i) {

        var result = l[i];
        //console.log(len_for_string)
        
        if (lang_all_page=="ru"){
          var template_for_catalogs =template_for_catalog.replace("<katalog_name>",result['fields']['name']) 

        }
        else if (lang_all_page=="en"){
          var template_for_catalogs =template_for_catalog.replace("<katalog_name>",result['fields']['name_en']) 

        }
        else if (lang_all_page=="hy"){
          var template_for_catalogs =template_for_catalog.replace("<katalog_name>",result['fields']['name_am']) 
          
        }
         
         template_for_catalogs =template_for_catalogs.replace("<url>","/shop_products/category/"+result['fields']['category_id_main']) 
   
    $(".collections_katalog .grid-list.header__collections-menu").append(template_for_catalogs)
        
    }}else{
    	$(".collections_katalog .grid-list.header__collections-menu").html("")

    }

           },
            error: function(daa){$(".collections_katalog .grid-list.header__collections-menu").html("")},
            processData: false,
            contentType: false,


           })}
	 $(".collections_katalog").addClass("is-show")
	

 
});

$(".js-hide-catalog").on("click", function(){
	$(".collections_katalog").removeClass("is-show")

})

$(".pay").on("click", function(){
  $(".pays_contaner").toggle()
})
$(".lang").on("click", function(){
  $(".langs_contaner").toggle()
})


$(".add_cart_products").on("click", function(){
  var pk = $(this).attr("pk")
  var data = new FormData()
   data.append("pk", pk)
            data.append("count", 1)
           
            

            

            

     $.ajax({


              
            url: '/api/add_cart_product/',
            method: "POST",
            data: data,
            success: function(data){
             if (data.data!=0){
                 $(".icon.icon-cart .header__control-bage").text(parseInt($(".header__control-bage").text())+1)
                  $(".navigation-bar__icon.icon-cart .navigation-bar__bage").text($(".icon.icon-cart .header__control-bage").text())
                 
                 
                }
                open_window('/cart_page/',700,300);
                
                

             
               
                  
                

            },
            error: function(daa){},
            processData: false,
            contentType: false,
        })

})

$(".langs_contaner .lang_sellect").on("click", function(){
  var lang = $(this).attr("id")
  if (lang=="English"){
    url = "/language/activate/en/"

  }
  else if(lang=="Armenian"){
    url = "/language/activate/hy/"

  }
  else{
    url = "/language/activate/ru/"

  }
  var link = document.createElement('a');
  link.href = url;
  document.body.appendChild(link);
  link.click();   



})


var toggle_value = 0

$("span.label_add_search_category").on("click", function(){
  var text = $(this).text()
  var pk = $(this).attr("value")

  
  if ($(this).attr("v") == undefined){
     
  $("#selected-value span").attr("value", pk)

  }
 else{
  $("#selected-value span").attr("value", "")

 }
 $("#selected-value span").text(text)

  $("#options .label").removeClass("display_options")
  $("#options .label").addClass("display_none_options")
  $("#options").removeClass("show_class")
   toggle_value=0
})



$("#options-view-button").on("click", function(){
  
  
 
  if (toggle_value==0){
    toggle_value=1
    $("body").addClass("class_show_div")
 $("#options .label").removeClass("display_none_options")
  $("#options .label").addClass("display_options")
  $("#options").addClass("show_class")
  }
  else{
    toggle_value=0
    $("body").removeClass("class_show_div")
     $("#options .label").removeClass("display_options")
  $("#options .label").addClass("display_none_options")
  $("#options").removeClass("show_class")
  }
  
   
})


$(".pays_contaner .pay_sellect").on("click", function(){
  var pay_code = $(this).attr("id")
  if (pay_code=="ENG"){
    url = "/api/change_currency_symbol/ENG/"

  }
  else if(pay_code=="ARM"){
    url = "/api/change_currency_symbol/ARM/"

  }
   else if(pay_code=="EUR"){
    url = "/api/change_currency_symbol/EUR/"

  }
  else{
    url = "/api/change_currency_symbol/RUR/"

  }
  var link = document.createElement('a');
  link.href = url;
  document.body.appendChild(link);
  link.click();   



})
var $container = $('#options-view-button');

$('body').on('click', function(evt) {
  var $target = $(evt.target);

  if ( $target.closest($container).length  || $target.closest($(".pay")).length || $target.closest($(".lang")).length ) { 
    console.log('❌ click inside');
  }
  else {
    $("#options .label").removeClass("display_options")
  $("#options .label").addClass("display_none_options")
  $("#options").removeClass("show_class")
  $(".pays_contaner").hide()
  $(".langs_contaner").hide()
  //$(".header__search__results").css("display", "none")
  toggle_value=0
  }


});
$(document).on("click", ".button.add-cart-counter__btn.add_cart_btn_counter_ind", function(){
  var product_page_request_status = 1
  var indicator = $(this).attr("ind")
  var pk = $(this).attr("pk")
  var data = new FormData()
  data.append("product_page_request_status", product_page_request_status)
  data.append("indicator", indicator)
  data.append("pk", pk)
  
  $.ajax({


              
            url: '/api/add_cart_product/',
            method: "POST",
            data: data,
            success: function(data){
              if (data.data!=0){

                 $(".icon.icon-cart .header__control-bage").text(parseInt($("span.header__control-bage.cart-empty").text())+1)
                  $(".navigation-bar__icon.icon-cart .navigation-bar__bage").text($(".icon.icon-cart .header__control-bage").text())
                  
                  if (parseInt(data.min_size) !=  1){
                     $(".header__control-btn.header__cart .header__control-text").text(String((parseFloat($(".header__control-btn.header__cart .header__control-text").text())+(parseInt(data.min_size)/100)*parseFloat(data.price_total/parseFloat(pay_rates_search).toFixed(2))).toFixed(2))+" "+pay_icon_search)


                  }
                  else{
                     $(".header__control-btn.header__cart .header__control-text").text(String((parseFloat($(".header__control-btn.header__cart .header__control-text").text())+parseFloat(data.price_total/parseFloat(pay_rates_search).toFixed(2))).toFixed(2))+" "+pay_icon_search)

                  }
                 }
                open_window('/cart_page/',700,300);
                
                

             
               
                  
                

            },
            error: function(daa){},
            processData: false,
            contentType: false,
        })

})



$(`div[data-fixed-panels="bottom"]:not(.bottom_tab_mobile)`).remove()
$( window ).on( "resize", function() {
  if ($(".navigation-bar-panel.navigation-bar-search.is-show").length>0){
    if ($(this).width() > 767){
     $("header").css("display", "block")
     

  }
  else{
     $("header").css("display", "none")
    

  }

  }
  
 
});