from django import forms
from .models import BusinessEnquiry, Feedback


class BusinessEnquiryForm(forms.ModelForm):
    class Meta:
        model = BusinessEnquiry
        fields = ['name', 'nature_of_business', 'email', 'organisation_company', 'contact_phone', 'queries_partnership_details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'nature_of_business': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nature of Business'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'organisation_company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organisation/Company'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Phone'}),
            'queries_partnership_details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Queries/Partnership Details', 'rows': 5}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'category', 'priority', 'suggestions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name (optional)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com (optional)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share your thoughts...', 'rows': 4}),
        }