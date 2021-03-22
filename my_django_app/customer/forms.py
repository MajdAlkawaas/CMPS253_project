from django import forms
from .models import Customer


class SingupForm(forms.Form):
    FirstName    = forms.CharField(max_length=50,
                                widget=forms.TextInput(
                                    attrs={
                                        'type'       : "text",
                                        'class'      : "form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6",
                                        'placeholder': 'Write your first name here'
                                    }))

    LastName     = forms.CharField(max_length=50,
                                widget=forms.TextInput(
                                    attrs={
                                        'type'       : "text",
                                        'class'      : "form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6",
                                        'placeholder': 'Write your last name here'
                                    }))

    username     = forms.CharField(max_length=50,
                                widget=forms.TextInput(
                                    attrs={
                                        'type'       : "text",
                                        'class'      : "form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6",
                                        'placeholder': 'Write your username name here'
                                    }))    

    EmailAddress = forms.EmailField(max_length=250,
                                    widget=forms.EmailInput(
                                        attrs={
                                            'type'       : "email",
                                            'class'      : "form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6",
                                            'placeholder': 'Write your email name here'
                                        }))
    
    password     = forms.CharField(max_length=50, 
                                   widget=forms.PasswordInput(
                                       attrs={
                                            'type'        : "password",
                                            'class'       : "form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6",
                                            "autocomplete": "off"
                                        }))

    Customer = forms.ModelChoiceField(queryset=Customer.objects.all(),empty_label="Select Customer", widget=forms.Select(
        attrs={
                'class' : 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
            }))
                                        



class signinForm(forms.Form):
    EmailAddress    = forms.EmailField(max_length=250,
                                    widget=forms.EmailInput(
                                        attrs={
                                            'type'       : 'email',
                                            'class'      : 'form-control h-auto py-7 px-6 rounded-lg border-0',
                                            'placeholder': 'Email Address'
                                        }
                                    ))
    
    password        = forms.CharField(max_length=50,
                                      widget=forms.PasswordInput(
                                          attrs={
                                              'type'            : 'password',
                                              'class'           : 'form-control h-auto py-7 px-6 rounded-lg border-0',
                                              'autocomplete'    : 'off'
                                          }
                                      ))
