from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '이름'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'message': forms.Textarea(attrs={'placeholder': '전달하고 싶은 내용을 남겨주세요.', 'rows': 6}),
        }
