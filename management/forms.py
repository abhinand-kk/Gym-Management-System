from django import forms
from django.contrib.auth.models import User
from .models import ClientProfile, Membership

class ClientProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = ClientProfile
        fields = ['age', 'gender', 'phone_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['user', 'membership_type', 'registration_fee', 'start_date', 'end_date', 'payment_status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django.contrib.auth.forms import UserCreationForm

class SimpleUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        help_text="Required. 150 characters or fewer.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
