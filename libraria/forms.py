from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, ReviewWeb, listbook, category, review_book, review_user

class ReviewWebForm(forms.ModelForm):
    class Meta:
        model = ReviewWeb
        fields = ['review_field']

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another one.")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'style': 'width: 100%;' 'padding-top: 5px;' 'padding-bottom: 5px;' 'border-radius: 5px;',
            'placeholder': 'Enter Username',
        })
        self.fields['email'].widget.attrs.update({
            'style': 'width: 100%;' 'padding-top: 5px;' 'padding-bottom: 5px;' 'border-radius: 5px;',
            'placeholder': 'Enter Email',
        })
        self.fields['password1'].widget.attrs.update({
            'id': 'password-field',
            'style': 'width: 100%; padding-top: 5px; padding-bottom: 5px; border-radius: 5px;',
            'placeholder': 'Enter password',
            'pattern': '(?=.*\d).{8,}',
            'title': 'Must contain at least one number and at least 8 or more characters',
        })
        self.fields['password2'].widget.attrs.update({
            'id': 'confirm-password-signup',
            'style': 'width: 100%;' 'padding-top: 5px;' 'padding-bottom: 5px;' 'border-radius: 5px;',
            'placeholder': 'Confirm password',
        })

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'file', 'address', 'phone', 'account']

class addbookForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=category.objects.all(),
        empty_label="Select a category", 
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    years = forms.ChoiceField(
        choices=[('', 'Select a publication year')] + [(year, year) for year in range(1990, 2025)],
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


    class Meta:
        model = listbook
        fields = [
            'title', 'author', 'publisher', 'number_of_pages',
            'years', 'category', 'synopsis', 'price', 'cover_image', 'stok'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Enter the book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Enter the author name'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Enter the publisher name'
            }),
            'number_of_pages': forms.NumberInput(attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Enter the number of pages'
            }),
            'synopsis': forms.Textarea(attrs={
                'class': 'form-control synopsis',
                'placeholder': 'Write a short synopsis',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Enter the price'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'stok': forms.NumberInput(attrs={
                'class': 'form-control input-detail',
                'placeholder': 'Enter stock'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ['category_name', 'desc']
        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control'}),
            'desc': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2}),
        }

class ReviewBookForm(forms.ModelForm):
    class Meta:
        model = review_book
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': 'Rate the book (1-5)',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here',
                'rows': 4,
            }),
        }

class ReviewAccountForm(forms.ModelForm):
    class Meta:
        model = review_user
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': 'Rate the librender (1-5)',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here',
                'rows': 4,
            }),
        }

