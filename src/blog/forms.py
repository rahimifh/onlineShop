from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "user"]

    def clean_user(self):
        user = self.cleaned_data.get("user")
        if len(user) > 200:
            raise forms.ValidationError("طول نام از دویست حرف بیشتر است !")
        return user

    def clean_text(self):
        text = self.cleaned_data.get("text")
        if len(text) > 400:
            raise forms.ValidationError("طول متن نظر از ۴۰۰ حرف بیشتر است")
        return text


class SearchForm(forms.Form):
    pass
