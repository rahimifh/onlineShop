from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from account.models import Account




class PersonDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonDetailForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop("user", None)  # getting kwargs
        self.fields["first_name"].widget.attrs.update(
            {"class": "px-4 my-4 w-full h-12 rounded-xl border-gray-100 bg-slate-100"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "px-4 my-4 w-full h-12 rounded-xl border-gray-100 bg-slate-100"}
        )     
        self.fields["password"].widget.attrs.update(
            {"class": "px-4 my-4 w-full h-12 rounded-xl border-gray-100 bg-slate-100"}
        )

    class Meta:
        model = Account
        fields = ("first_name","last_name", "password")
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "username": "شماره همراه",
            "password": "رمز عبور",
        }

        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"cols": 10, "rows": 3}),
        }

    def save(self, commit=True):
        user = super(PersonDetailForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "password")

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login!")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "phone",
            "country",
            "city",
            "email",
            "birthday",
            "gender",
            "address",
            "profile_image",
        )
