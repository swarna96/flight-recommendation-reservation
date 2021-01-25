from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from flight.models import Flight
from flight.models import Contact,Input_Data
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1','password2')
    def save(self,commit=True):
        user =  super(CustomUserCreationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']

        if commit:
            user.save()
        return user

class FlightForm(ModelForm):
    class Meta:
        model = Flight
        fields='__all__'

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields='__all__'

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password')

class InputDataForm(ModelForm):
    class Meta:
        model = Input_Data
        fields=('user_id','user_name','airline_name','overall_rating')