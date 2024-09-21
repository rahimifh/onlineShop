from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from account.models import Account, ver_code


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Account
        fields = (
            "password",
            "firstName",
            "last_Name",
            "username",
            "phone",
            "country",
            "city",
            "email",
            "birthday",
            "gender",
            "education",
            "social_media",
            "address",
            "is_Business",
            "is_active",
            "is_staff",
            "is_superuser",
            "profile_image",
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ("username", "password", "is_active", "is_admin")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "username", "date_joined", "is_active", "is_admin", "firstName")
    list_filter = ("is_admin",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "password",
                    "firstName",
                    "last_Name",
                    "username",
                    "phone",
                    "country",
                    "city",
                    "email",
                    "birthday",
                    "gender",
                    "education",
                    "social_media",
                    "address",
                    "profile_image",
                  
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_EmailVerified",
                    "is_admin",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("username", "password1", "password2")},
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()


@admin.register(ver_code)
class ver_codeAdmin(admin.ModelAdmin):
    list_display = ["phone", "code", "id"]




admin.site.register(Account, UserAdmin)
admin.site.unregister(Group)



