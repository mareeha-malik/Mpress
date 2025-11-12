from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        pw2 = cleaned.get('password2')
        if pw and pw2 and pw != pw2:
            self.add_error('password2', 'Passwords do not match')
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows':4, 'class':'w-full border rounded p-2'})
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar

        # validate content type
        content_type = getattr(avatar, 'content_type', '')
        if not content_type.startswith('image/'):
            raise forms.ValidationError('Uploaded file is not an image')

        # validate file size (2.5 MB limit)
        limit_mb = 2.5
        if avatar.size > limit_mb * 1024 * 1024:
            raise forms.ValidationError(f'Image file too large (>{limit_mb} MB)')

        return avatar
