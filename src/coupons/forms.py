from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(label="کد", widget=forms.TextInput(attrs={'class': 'codeinput'}))
