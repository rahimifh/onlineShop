from django import forms

from shop.models import SpecialOrder




class addOrderForm(forms.ModelForm):
    class Meta:
        model = SpecialOrder
        fields = (
            "name",
            "phone",
            "description",
            "image"
        )

    def save(self, commit=True, *args, **kwargs):
        order = super().save(commit=False)
        if commit:
            order.save()

        return order




