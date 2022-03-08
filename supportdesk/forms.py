# Django
from django import forms

# App
from .models import Request

class RequestForm(forms.ModelForm):    
    class Meta:
        model = Request
        fields = ['summary', 'description', 'is_high_priority']     
        
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Unable to login to application'}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }   