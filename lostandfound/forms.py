from django import forms
from django.contrib.auth.models import User
import re

from .models import LostItem


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = [
            'item_name',
            'description',
            'category',
            'location_lost',
            'date_lost',
            'image',
            'contact_name',
            'contact_email',
            'contact_phone',
            'security_question',
            'security_answer',
        ]
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make security fields required in the form
        self.fields['security_question'].required = True
        self.fields['security_answer'].required = True


class ClaimForm(forms.Form):
    claimer_name = forms.CharField(max_length=100, label="Your name")
    claimer_email = forms.EmailField(label="Your email")
    answer = forms.CharField(
        max_length=200,
        label="Your answer to the security question",
        widget=forms.TextInput()
    )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        pattern = r'^[A-Za-z0-9._%+-]+@iau\.edu\.sa$'

        if not re.match(pattern, email):
            raise forms.ValidationError("Email must be an IAU address ending with @iau.edu.sa")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        """
        Create the User and set the password properly (hashed).
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
