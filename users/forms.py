from django import forms
from .models import UserAccount


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Enter your email", max_length=150, help_text="Required")
    username = forms.CharField(label="Enter your username", min_length=4, max_length=50, help_text="Required",
                               error_messages={'required': 'You have to enter your email'})
    first_name = forms.CharField(label="Enter your First Name", help_text="Required")
    last_name = forms.CharField(label="Enter your Last Name", help_text="Required")
    password = forms.CharField(label="Enter your password", widget=forms.PasswordInput)
    re_password = forms.CharField(label="Enter your password again", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'username', 'first_name', 'last_name',)

    def clean_email(self):
        email = self.cleaned_data['email']
        query_res = UserAccount.objects.filter(email=email)
        if query_res.count():
            raise forms.ValidationError("This email is already taken!")
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        query_res = UserAccount.objects.filter(username=username)
        if query_res.count():
            raise forms.ValidationError("Username already exists!")
        return username

    def clean_re_password(self):
        data = self.cleaned_data
        if data['password'] != data['re_password']:
            raise forms.ValidationError("Passwords are not equal!")
        return data['re_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Last Name'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['re_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
