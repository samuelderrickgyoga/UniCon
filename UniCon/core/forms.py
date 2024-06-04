from django.contrib.auth.forms import *
from django import forms
from django.contrib.auth.models import *
from .models import *
#profile
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    university = forms.ChoiceField(choices=[
        ('makerere', 'Makerere'), ('kyambogo', 'Kyambogo'), ('kabaale', 'Kabaale'), ('gulu', 'Gulu'),
        ('muni', 'Muni'), ('soroti', 'Soroti'), ('lira', 'Lira'), ('busitema', 'Busitema'), ('mountains_of_the_moon', 'Mountains of the Moon')
    ], required=True)
    student_id = forms.CharField(max_length=20, required=True)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1980, 2024)), required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)
    phone = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)
    course = forms.CharField(max_length=100, required=True)
    year = forms.ChoiceField(choices=[
        ('freshman', 'Freshman'), ('sophomore', 'Sophomore'), ('junior', 'Junior'), ('senior', 'Senior')
    ], required=True)
    interests = forms.MultipleChoiceField(choices=[
        ('sports', 'Sports'), ('music', 'Music'), ('technology', 'Technology')
    ], widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Profile
        fields = ['dob', 'university', 'interests', 'course', 'year', 'firstname', 'lastname', 'phone', 'profile_picture',]
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'university': forms.Select(attrs={'class': 'form-control'}),
            'interests': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

# first itime signup
class signup(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
 #working with posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']   