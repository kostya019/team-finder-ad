from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate

from .models import CustomUser
from .validators import validate_phone_number, validate_github_url


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["name", "surname", "github_url", "phone", "avatar", "about",]
        widgets = {
            'about': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                    'Ваш профиль — как открытый репозиторий. Заполните его, чтобы вас нашли!'
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            validated_phone = validate_phone_number(phone)
            return validated_phone
        return phone

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url:
            validated_url = validate_github_url(github_url)
            return validated_url
        return github_url

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'phone' in self.cleaned_data:
            instance.phone = self.cleaned_data['phone']
        if 'github_url' in self.cleaned_data:
            instance.github_url = self.cleaned_data['github_url']
        if commit:
            instance.save()
        return instance


class CustomRegistrationForm(UserCreationForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'surname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем поле username, если оно есть
        if 'username' in self.fields:
            self.fields.pop('username')
        if 'password1' in self.fields:
            self.fields.pop('password1')
        if 'password2' in self.fields:
            self.fields.pop('password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        """
        Переопределяем метод save, чтобы корректно использовать наш менеджер.
        """
        cleaned_data = self.cleaned_data

        user = CustomUser.objects.create_user(
            email=cleaned_data['email'],
            name=cleaned_data['name'],
            surname=cleaned_data['surname'],
            password=cleaned_data['password'],
        )

        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Сохраняем request
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                username=email,
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Неверные email или пароль.',
                    code='invalid_login'
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    'Аккаунт деактивирован.',
                    code='inactive'
                )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
