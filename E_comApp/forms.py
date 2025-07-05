from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
		widgets = {
            'username': forms.TextInput(attrs={
                        'placeholder':'Username',
                }),
            'password1': forms.PasswordInput(attrs={
            			'placeholder' : 'Password',
            	}),
            'password2': forms.PasswordInput(attrs={
            			'placeholder' : 'Retype-Password'
            	}),
            }

class storeform(forms.ModelForm):
	class Meta:
		model = store
		fields = ['productimage','productname','price']
		widgets = {
				'productname':forms.TextInput(attrs={
					'class':'form-control names'
					}),
				'price':forms.NumberInput(attrs={
					'class':'form-control names'
					})
		}		
class loginform(forms.Form):
	username = forms.CharField(label = 'Username', max_length=(100),widget= forms.TextInput
                           (attrs={'placeholder':'Enter Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
	number = forms.CharField(label='Phone Number', max_length=10,min_length=10,widget=forms.TextInput(attrs={'placeholder':'Enter Phone Number'}))

## without login and register or Abstract class models ############################
# class CustomUserForm(UserCreationForm):
# 	uname = forms.CharField(label="User Name",max_length=(50))
# 	class Meta:
# 		model = models.CustomUser
# 		fields = UserCreationForm.Meta.fields + ('uname', 'uphonenumber',)

# class registerform(forms.ModelForm):
# 	class Meta:
# 		model = models.registertable
# 		fields = '__all__'
####################################################################################