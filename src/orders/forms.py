from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone',
            'address',
            'postal_code',
            'city',
        ]
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        # print(type(self.instance))
        # if self.instance:
        #     self.fields["phone"].widget.attrs["value"] = self.instance.username
        # self.fields["last_name"].widget.attrs["value"] = self.instance.lastName

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'