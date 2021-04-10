from django import forms
from django.contrib.auth.forms import UserCreationForm
from customer.models import Customer, Director, User, Queueoperator, Queue
from django.db import transaction


                                        
class SigninForm(forms.Form):
    username    = forms.CharField(max_length=250,
                                    widget=forms.TextInput(
                                        attrs={
                                            'type'       : 'email',
                                            'class'      : 'form-control h-auto py-7 px-6 rounded-lg border-0',
                                            'placeholder': 'Email Address'
                                        }
                                    ))
    
    password    = forms.CharField(max_length=50,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'type'            : 'password',
                                            'class'           : 'form-control h-auto py-7 px-6 rounded-lg border-0',
                                            'autocomplete'    : 'off'
                                        }
                                    ))


    

# class Test_signin(forms.Form):
#     username = forms.CharField(max_length=50)
#     password = forms.CharField(widget=forms.PasswordInput())

class EditForm(forms.Form):
    queueNameEdited     = forms.CharField(max_length=100,
                            widget=forms.TextInput(
                                attrs={
                                    "type"      :   "text",
                                    "class"     :   "form-control form-control-lg form-control-solid",
                                }
                            )
                        )

    categoriesEdited    = forms.CharField(
                            widget=forms.TextInput(
                                attrs={
                                    "type"      :   "text",
                                    "class"     :   "form-control form-control-lg form-control-solid",
                                }
                            )
                        )

    # This needs to be populated by the queueOperators
    queueOperator_list = forms.MultipleChoiceField(
        widget=forms.Select(
            attrs= {
                'class' : 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
            }
        ),
    )

    def __init__(self, queue, categoriesStr, operators, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.operators = operators
        self.fields["queueNameEdited"].widget.attrs["value"] = queue.Name
        self.fields["categoriesEdited"].widget.attrs["value"] = categoriesStr
        # self.fields["queueOperator_list"].widget.attrs["value"] = operators

    


class SingupForm(UserCreationForm):

    customer_list = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=True,
        widget=forms.Select(
            attrs= {
                'class' : 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1', 'password2')
        

    

    def __init__(self, *args, **kwargs): 
        super(SingupForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['username'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['username'].widget.attrs['placeholder'] = 'Write your username here'


        self.fields['last_name'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['email'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['email'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['password1'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['password1'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['password2'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['password2'].widget.attrs['placeholder'] = 'Write your first name here'

        print("-----------SingupForm-----------")
        for field in self.fields:
            print(field)
        print("------------------------")

    @transaction.atomic
    def save(self):
        print("HERE SingupForm.save")
        user = super().save(commit=False)
        user.is_director = True
        user.save()
        director = Director.objects.create(user=user, Customer = self.cleaned_data.get('customer_list'))
        return user    

class QueueOperatorSignup(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1', 'password2')
        


    def __init__(self, *args, **kwargs): 
        self.director = kwargs.pop('user',None)
        super(QueueOperatorSignup, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['username'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['username'].widget.attrs['placeholder'] = 'Write your username here'


        self.fields['last_name'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['email'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['email'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['password1'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['password1'].widget.attrs['placeholder'] = 'Write your first name here'

        self.fields['password2'].widget.attrs['class'] = 'form-control h-auto py-7 px-6 border-0 rounded-lg font-size-h6'
        self.fields['password2'].widget.attrs['placeholder'] = 'Write your first name here'

        print("-----------SingupForm-----------")
        for field in self.fields:
            print(field)
        print("------------------------")
    
    
    @transaction.atomic
    def save(self):
        print("HERE SingupForm.save")
        user = super().save(commit=False)
        director = Director.objects.get(user= self.director)
        user.is_queueoperator = True
        user.save()
        queueoperator = Queueoperator.objects.create(user=user, Director=director, Customer=director.Customer)
        return user
