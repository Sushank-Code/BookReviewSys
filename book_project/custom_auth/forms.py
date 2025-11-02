from django import forms
from custom_auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm

   
class RegistrationForm(UserCreationForm):
 
    class Meta:
        model = User
        fields = ["name","email","password1","password2"]

    def clean_email(self):   # clean_'fieldname' is used for single validation
        email = self.cleaned_data.get("email")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists")
        return email

# Password Reset Form
 
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "name@example.com",
            "autocomplete" : "off",
        })
    )
    # In built-in Pw reset view or form , it doesnot show error in case email doesnot exit, so we have to do it on our own
    def clean_email(self):   
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError("Invalid Email Address")
        return email
    