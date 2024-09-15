from .models import  consulting
from django import forms

class RLgiftForm(forms.ModelForm):
    class Meta:
        model = consulting
        fields = (    
            "name",
            "lastName",
            "category",
            "phone",
            "company",
            "description",
              )
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields["name"].widget.attrs.update({'class': 'form-control simple_text_dark_input'})
           self.fields["lastName" ].widget.attrs.update({'class':'form-control simple_text_dark_input'})
           self.fields["category" ].widget.attrs.update({'class':'form-control simple_text_dark_input'})
           self.fields["phone" ].widget.attrs.update({'class':'form-control simple_text_dark_input'})
           self.fields["company" ].widget.attrs.update({'class':'form-control simple_text_dark_input'})
           self.fields["description" ].widget.attrs.update({'class':'form-control simple_text_dark_input'})
