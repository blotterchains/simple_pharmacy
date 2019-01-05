    
    function change_header(a){
        if (a=='ورود'){
        document.getElementById("bld_texts").innerHTML=a;
        document.getElementById("home").innerHTML="<center><form method='POST' action='/login'> <input id='header_button' type='text' placeholder='username' name='username'><br><input id='header_button' type='text' name='password' placeholder='password'><br><br><input id='header_button' class='submit' type='submit' value='ورود'></form></center>";
        var contentToRemove = document.querySelectorAll("#drug_show");
        $(contentToRemove).remove(); 
    }
    if (a=='خروج'){

        window.location="/in"
    }
        if(a=="پرداخت"){
        document.getElementById("bld_texts").innerHTML=a;
        //{%if flag=='login'%}
        document.getElementById("home").innerHTML="<center><form method='POST' action='/pardakht'><input id='header_button' type='text' name='user_id' value='{{id[3]}}'><br><input id='header_button' type='text' placeholder='نشانی' name='username'><br><input id='header_button' type='text' name='password' placeholder='نام گیرنده'><br><input id='header_button' type='submit' value='اتصال به صفحه پرداخت'></form></center>";
        //{%endif%}
    }
        if (a=='جستوجو دارو'){
        document.getElementById("bld_texts").innerHTML=a;
        
        document.getElementById("home").innerHTML="<center><form method='POST' action='/signup'><input id='header_button' class='submit' type='submit' value='جستوجو'> <br><input id='header_button' class='submit' type='submit' value='جستوجو'></form></center>";
        var contentToRemove = document.querySelectorAll("#drug_show");
        $(contentToRemove).remove();
        }
        if (a=='سبد خرید'){
        document.getElementById("bld_texts").innerHTML=a;
        
        $(document).ready(function(){
        $.post("/kharid",
        {
        //{%if flag=="login"%}
          id: "{{id[3]}}"
          //{%endif%}
        },
        function(data,status){
            data=data.replace("\\");
            data=data.replace(/de'>/g,"de'> کد محصول<br>");
            data=data.replace(/me'>/g,"me'> نام محصول<br>");
            data=data.replace(/ih'>/g,"ih'>  :توضیحات<br>");
            document.getElementById("home").innerHTML= data+'<input id="header_button" class="pardakht" type="button" value="پرداخت" onclick="change_header(value)"><br><br><br><br><br><br><br><br>';
        });
});
        var contentToRemove = document.querySelectorAll("#drug_show");
        $(contentToRemove).remove();
        }
        if (a=='ثبت نام'){
        document.getElementById("bld_texts").innerHTML=a;
        document.getElementById("home").innerHTML="<center><form id='form_request' method='POST' action='/signup'> <input name='username' id='header_button' type='text' placeholder='username'><br><input id='header_button' name='password' type='text' placeholder='password'><br><input id='header_button' type='text' placeholder='email' name='email'><br><br><input id='header_button' class='submit' type='submit' value='ثبت نام'></form></center>";
        var contentToRemove = document.querySelectorAll("#drug_show");
        $(contentToRemove).remove();
    }
        if (a=='خانه'){
        document.getElementById("bld_texts").innerHTML=a;
        
        $(document).ready(function(){
        $.post("/valid_drugs",
        {
            post:"home"
        },
        function(data,status){
            document.getElementById("home").innerHTML= data;
        });
});        
    }
    if (a=='مشاهده محصولات'){
        document.getElementById("bld_texts").innerHTML=a;
        
        $(document).ready(function(){
        $.post("/valid_drugs",
        {
            post:"login"
        },
        function(data,status){
            document.getElementById("home").innerHTML= data;
        });
});        
    }
    }
function add_kharid(id){
    $(document).ready(function(){
        $.post("/add_kharid",
        {
        //{%if flag=="login"%}

            user_id:"{{id[3]}}",
        //{%endif%}

            drug_id:id
        },
        function(data,status){
            alert(data)
            change_header("سبد خرید")
        });
});
}
function delete_kharid(id){
    $(document).ready(function(){
        $.post("/delete_kharid",
        {
        //{%if flag=="login"%}
            user_id:"{{id[3]}}",
            id:id
            //{%endif%}
        },
        function(data,status){
            alert(data)
            change_header("سبد خرید")
        });
});
} 
