from django import forms

from .models import Join


class JoinForm(forms.ModelForm):
    email = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'size': 30,
            'placeholder': "Your email ...",
        }))

    class Meta:
        model = Join
        fields = ('email', )

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        queryset = Join.objects.filter(email__iexact=email)
        if queryset.exists():
            raise forms.ValidationError(
                'Этот email уже существует в списке рассылки')
        return email
