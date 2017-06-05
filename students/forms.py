from django import forms
from django.forms import ModelForm
from .models import *  
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentsForm(forms.ModelForm):
    # first_name = forms.CharField(max_length = 100)
    # last_name = forms.CharField(max_length = 100)
    # username = forms.CharField(max_length = 100, required=True)
    # email = forms.EmailField(required = True, validators=[validate_email])
    # date_of_birth = forms.DateField(required=True)
    # # gender = forms.Charfield
    # password = forms.CharField(widget = forms.PasswordInput())
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        
        model = Students
        fields = "__all__"
        widget = {
            'password': forms.PasswordInput()
        }

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length = 100)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields =["username", "email", "password"]
        
class StudentsLoginForm(forms.Form):
    email = forms.EmailField(required = True)
    password = forms.CharField(widget = forms.PasswordInput())
    
    # def cleaned_data(self):
    
        
class ContactForm(forms.Form):
    subject = forms.CharField(max_length = 100, required = True)
    message = forms.CharField(required = True, widget = forms.Textarea())
    contact_email = forms.EmailField(required = True)
    
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "Your subject:"
        self.fields['message'].label = "What do you want to say?"
        self.fields['contact_email'].label = "Your email:"
        
    