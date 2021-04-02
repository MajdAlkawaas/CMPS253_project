from django import forms
from customer.models import Category, Director, Queue
from itertools import chain
class GuestForm(forms.Form):
    name        = forms.CharField(max_length=250,
                            widget=forms.TextInput(
                                attrs={
                                    'type'       : 'text',
                                    'class'      : 'form-control',
                                    'placeholder': 'Enter name'
                                }
                            ))

    phoneNumber = forms.CharField(max_length=250,
                                widget=forms.TextInput(
                                    attrs={
                                        'type'       : 'text',
                                        'class'      : 'form-control',
                                        'placeholder': 'Enter phonenumber'
                                    }
                                ))

    categories_list = forms.ModelChoiceField(
        queryset= Category.objects.none(),
        widget=forms.Select(
            attrs = { 
                'class' : 'form-control',
                'id'    : 'exampleSelect2'
            }
    ))

    def __init__(self, categories, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        print("------------------------")
        print("guest.forms\n HERE Categories type: \n", type(categories))
        print("------------------------")
        print("HERE guest.froms\n", categories)
        self.fields['categories_list'].queryset = categories
        
                                