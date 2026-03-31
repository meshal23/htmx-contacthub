from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
 
class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                'class':'input input-bordered w-full',
                'placeholder':'Contact Name'
            }
        )
    )

    email = forms.EmailField(
        widget= forms.EmailInput(
            attrs= {
                'class':'input input-bordered w-full',
                'placeholder':'Email Address'
            }
        )
    )

    document = forms.FileField(
        widget= forms.FileInput(
            attrs= {
                'class':'file-input file-input-bordered w-full',    
            }
        ),
        required=False
    )

    def clean_email(self): #naming convention for validations starts with clean_
        email = self.cleaned_data['email']

        #check if the email already exist for this user
        if Contact.objects.filter(user=self.initial.get('user'), email=email).exists(): #user=self.initial.get('user') this is for we're searching any email that has an authenticated user see in views.py create_contact method we're sending the authenticated user as initial user value
            raise ValidationError("You already have a contact with this email address")
        return email
    class Meta:
        model = Contact
        fields = (
            'name','email','document'
        )
    
    