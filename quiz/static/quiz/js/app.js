function submitForm()
{
     if(document.pressed == 'signIn')
     {
        document.getElementById('sign-form').action='/login/';
     } 
     else if(document.pressed == 'signUp')
     {
        document.getElementById('sign-form').action='/signup/';
     }
     return true;
 }