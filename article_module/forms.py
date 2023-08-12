from django import forms

class ArticleCommentForm(forms.Form):
    comment = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'نظر خود را وارد کنید ...'
        })
    )
    replay = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'id': 'comment-replay',
        })
    )