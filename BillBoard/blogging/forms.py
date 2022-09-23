from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'Автор не выбран'
        self.fields['cat'].empty_label = 'Категория не выбрана'
        self.fields['cat'].widget.attrs.update(
            {'class': 'btn btn-secondary dropdown-toggle'}, size='7')
        self.fields['author'].widget.attrs.update(
            {'class': 'btn btn-secondary dropdown-toggle',
             'type': 'button',
             'data-toggle': 'dropdown',
             'aria-haspopup': 'true',
             'aria-expanded': 'false'
             }
        )

    class Meta:
        model = Post
        fields = ['author', 'title', 'slug',
                  'text', 'photo', 'upload', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'size': 58}),
            'slug': forms.URLInput(attrs={'size': 58}),
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 7}),
        }

    def clean(self):
        cleaned_data = super().clean()

        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        description = self.cleaned_data.get("text")
        if description is not None and len(description) < 10:
            raise ValidationError(
                {"text": "Сообщение не может быть менее 10 символов."})

        if title == description:
            raise ValidationError(
                "Заголовок не должен быть идентичен тексту поста.")

        return cleaned_data
