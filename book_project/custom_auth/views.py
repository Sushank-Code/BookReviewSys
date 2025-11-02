from django.shortcuts import render,redirect
from custom_auth.forms import RegistrationForm,CustomPasswordResetForm
from django.contrib import messages  
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

# Reset Password
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

# Email sending
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse_lazy

# Create your views here.
 
def register_view(request): 

    if request.user.is_authenticated:
        return redirect('Dashboard')
    
    if request.method == "POST":
        rf = RegistrationForm(request.POST)
        if rf.is_valid():
            rf.save()
            messages.success(request,"Registration Successful! You can Login Now")
            return redirect('Login')
    else:
        rf = RegistrationForm()
    return render(request,'custom_auth/registration.html',{'rform':rf})

def login_view(request):

    if request.user.is_authenticated:
        return redirect('Dashboard')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')

        if not email or not password:
            messages.error(request,"Both fields are required")

        else:
            user = authenticate(request,email= email,password= password)
            
            if user is not None: # Login done
                login(request,user)

                # print("Session data:", request.session.items())
                if remember_me:
                    request.session.set_expiry(60*60*24)  # 1 day
                else:
                    request.session.set_expiry(0)  

                messages.success(request,"Login Successful")
                return redirect('Dashboard')
            else:
                messages.error(request,"Invalid Email and Password")

    return render(request,'custom_auth/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('Login') 

@login_required
def dash_view(request):
    return render(request,'custom_auth/dashboard.html')

# Change Password after Logging
@login_required
def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request,"Password change sucessfully! Login again with new password")
            return redirect("Login")
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request,'custom_auth/password_change.html',{'form':form})


# Forget Password/Reset password  ( Class Based View )
 
class CustomPasswordResetView(SuccessMessageMixin,PasswordResetView): 
    form_class = CustomPasswordResetForm
    template_name = "custom_auth/password_reset_form.html"
    subject_template_name = 'custom_auth/password_reset_subject.txt'
    html_email_template_name = 'custom_auth/password_reset_email.html'
    success_message = "A password reset link has been sent to your email. Please check your inbox."
    success_url = reverse_lazy('Login')

    def send_mail(self, context, from_email, to_email,html_email_template_name):
        
        # Render the body from the template (with the reset link)
        body = render_to_string(html_email_template_name, context)
        email = EmailMessage(
            # subject=subject,
            body=body,
            from_email=from_email,
            to=[to_email]  
        )
        email.content_subtype = 'html'
        email.send()
        