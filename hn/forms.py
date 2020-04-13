from django import forms

from .models import Submit, Comment, Usuari

class HomeForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ['title', 'url','text']
        widget = {'author' : forms.HiddenInput()}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widget = {'author' : forms.HiddenInput()}

class AboutForm(forms.ModelForm):
    class Meta:
        model = Usuari
        fields = ['about']
