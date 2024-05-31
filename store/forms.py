# store/forms.py
from django import forms
from store.models.comment import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
