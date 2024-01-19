from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, Profile, Comments


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form_inputs'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form_inputs'}))
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput(attrs={'class': 'form_inputs'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_inputs'}),
            'password1': forms.PasswordInput(attrs={'class': 'form_inputs'}),
            'password2': forms.PasswordInput(attrs={'class': 'form_inputs'})
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form_inputs'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form_inputs'}))

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_inputs'}),
            'password': forms.PasswordInput(attrs={'class': 'form_inputs'}),
        }


class AddPostForm(forms.ModelForm):
    title = forms.CharField(label='Title:',
                            widget=forms.TextInput(attrs={'class': 'add_form_input', 'placeholder': 'Add a title'}))
    description = forms.CharField(label='Description:', widget=forms.Textarea(
        attrs={'class': 'add_form_text', 'placeholder': 'Add a description'}))

    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'category')
        labels = {
            'image': '',
            'category': '',
        }


class EditProfileForm(forms.ModelForm):
    name = forms.CharField(label='Change name:',
                           widget=forms.TextInput(attrs={'class': 'add_form_input'}))
    image = forms.ImageField(label="Change image:", required=False, )

    class Meta:
        model = Profile
        fields = ('image', 'name')
        labels = {
            'image': '',
        }


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Add a comment'}))

    class Meta:
        model = Comments
        fields = ('text',)
