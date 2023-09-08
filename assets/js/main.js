function ajax_register(username, password, email, name, lastname, phone){
     $.ajax({

           
           url: '/api/sign_up/',
           type: 'POST',
           dataType: 'json',
           enctype: 'multipart/form-data',
           data: {'username': username,'password': password,
'email': email,'name':name,'lastname':lastname, 'phone': phone,

                      'csrfmiddlewaretoken': '{{ csrf_token }}'},
           
           success: function(data) {
            if (data.data==1){
                console.log("success")
                location.replace("/my_account/")

            }
            else if (data.data=="error"){
                console.log("user")
                $(".login_exists").css("display", "block")
            }
            else if (data.data==2){
                console.log("success")
                location.replace("/"+String(data.pk)+"/")

            }
            

           },
           error: function(data) {
                  alert('Something went wrong.');
           }


           })
}

function validateUsername(username) {
  // Check if the username is not empty
  var nameRegex = /^[a-zA-Z ]+$/;


  // Check if the name matches the regular expression
  
  if (nameRegex.test(username)) {
    return true;
  } else {
    return false;
  }
}

// Output: "Username is valid"


$(document).on("click", ".btn_registration", function(){
    //$(".login_head").css("display", "none")
    
    var username = $("#register-login").val()
    var password = $("#register-password").val()
    var email = $("#register-email").val()
    var name = $("#register-name").val()
    var lastname = $("#register-lastname").val()
    var phone = $("#register-phone").val()
    var agree = $("#register-agree")
    var validation = true
    const errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];
    const phoneInputField = document.querySelector("#register-phone");
   const phoneInput = window.intlTelInput(phoneInputField, {
     utilsScript:
       "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
   });
   if (phoneInput.isValidNumber()) {
      
      validation = true
    } else {
      validation = false
      
      const errorCode = phoneInput.getValidationError();
      error_text = ""
      if (lang_all_page=="ru"){
        if (errorMap[errorCode] == "Invalid number"){
            error_text = "Номер телефона должен быть цифрами"
          }
          else if(errorMap[errorCode] == "Too short"){
            error_text = "Номер телефона короткий"

          }
          else if(errorMap[errorCode] == "Too long"){
            error_text = "Номер телефона длинный"
            
          }
          else if(errorMap[errorCode] == "Invalid number"){
            error_text = "Номер телефона неправильный"
            
          }
          else{
            error_text = "Неверный код страны"

          }
        
          
        }
        else if (lang_all_page=="en"){
          if (errorMap[errorCode] == "Invalid number"){
            error_text = "Phone number must be numbers"
          }
          else if(errorMap[errorCode] == "Too short"){
            error_text = "Phone number is short"

          }
          else if(errorMap[errorCode] == "Too long"){
            error_text = "Phone number is long"
            
          }
          else if(errorMap[errorCode] == "Invalid number"){
            error_text = "Phone number is wrong"
            
          }
          else{
            error_text = "Invalid country code"

          }

          
         

        }
        else if (lang_all_page=="hy"){
         if (errorMap[errorCode] == "Invalid number"){
            error_text = "Հեռախոսահամարը պետք է լինի թվեր"
          }
          else if(errorMap[errorCode] == "Too short"){
            error_text = "Հեռախոսահամարը կարճ է"

          }
          else if(errorMap[errorCode] == "Too long"){
            error_text = "Հեռախոսահամարը երկար  է"
            
          }
          else if(errorMap[errorCode] == "Invalid number"){
            error_text = "Հեռախոսահամարը սխալ է"
            
          }
          else{
            error_text = "Երկրի կոդը սխալ է"

          }
          
        }
       
        $(".error_window").text(error_text)
        $(".error_window").css("display", "block")
        
      
      
     
    }


const validationResult_name = validateUsername(name);
const validationResult_last_name = validateUsername(lastname);

console.log(validationResult_name, validationResult_last_name); 
if (validationResult_name && validationResult_last_name){
  validation = true
  
}
else{
  validation = false
  
   if (lang_all_page=="ru"){
    error_text = "Неверное имя или фамилия."
       
          
        }
        else if (lang_all_page=="en"){
          error_text = "Invalid first name or last name."
         

          
         

        }
        else if (lang_all_page=="hy"){
          error_text = "Սխալ անուն կամ ազգանուն."
         
          
        }
  $(".error_window").text(error_text)
  $(".error_window").css("display", "block")

}

    
    
    
    


    

    if (username.length != 0 && password.length != 0 && email.length != 0 && name.length != 0 && lastname.length != 0 && phone.length != 0 && agree.length>0 && validation){
if (agree.is(':checked')) {ajax_register(username, password, email, name, lastname, phone)}
  else{
    $(".label_policy").css("color", "red")

  }
        
      
       
       

    


}
    



})
$(document).on("click", ".btn_login", function(){
    //$(".login_head").css("display", "none")
    
    var username = $("#singin-email").val()
    var password = $("#singin-password").val()
    
    

    if (username.length != 0 && password.length != 0){
       
        $.ajax({

           
           url: '/api/sign_in/',
           type: 'POST',
           dataType: 'json',
           enctype: 'multipart/form-data',
           data: {'username': username,'password': password,


                      'csrfmiddlewaretoken': '{{ csrf_token }}'},
           
           success: function(data) {
            if (data.data==1){
                console.log("success")
                location.replace("/my_account/")

            }
            else{
                
                $(".login_invalid").css("display", "block")

            }

           },
           error: function(data) {
                  alert('Something went wrong.');
           }


           })

    }
    



})


