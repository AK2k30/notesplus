from django import forms
from .models import ass
from . models import *
from django.contrib.auth.forms import UserCreationForm

        
class DateInput(forms.DateInput):
    input_type = 'date'
    
    
    
class AssignForm(forms.ModelForm):
    class Meta:
        model = ass
        fields = ('title','owner','pdf', 'cover','url')
        exclude = ('url',)
    
    
class ExpForm(forms.ModelForm):
    class Meta:
        model = exx
        fields = ('title','owner','pdf', 'cover')
    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    Semester = forms.CharField(max_length=100)
    Branch = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','email','Semester','Branch']
        labels = {'email':'Email'}
        
    
class UploadFileForm(forms.Form):
    file = forms.FileField()


