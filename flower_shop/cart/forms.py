# cart/forms.py
from django import forms
from .models import Review

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, label='Full Name')
    address = forms.CharField(max_length=255, label='Address')
    phone = forms.CharField(max_length=15, label='Phone Number')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }