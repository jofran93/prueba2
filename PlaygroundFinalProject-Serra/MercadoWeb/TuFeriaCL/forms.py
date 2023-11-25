from django import forms
from .models import Post, UserProfile, Item
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password  # Importa la función de validación de contraseña
from django.contrib.auth.forms import AuthenticationForm # Esta incluye la lógica necesaria para validar el nombre de usuario y la contraseña y permitir el inicio de sesión.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit




class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'email', 'phone_number', 'profile_picture', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('user').username
        
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        
        return email
    
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        
        # Reglas de validación para la contraseña
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError('\n'.join(e.messages))
        
        return password
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user', 'full_name', 'email', 'phone_number', 'profile_picture', 'password',
            Submit('submit', 'Registrarse')
        )
    
    
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        
        self.fields.pop('username')
        self.fields.pop('password')
        
        self.fields['user'] = forms.CharField(
            label="Nombre de usuario",
            widget=forms.TextInput(attrs={'autofocus': True}),
        )
        self.fields['password'] = forms.CharField(
            label="Contraseña",
            strip=False,
            widget=forms.PasswordInput,
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')

        # Verificar la autenticación utilizando UserProfile
        try:
            user_profile = UserProfile.objects.get(user__username=username)
            if not user_profile.check_password(password):
                raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user', 'password',
            Submit('submit', 'Iniciar sesión')
        )
        
        
        

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['user', 'name', 'price', 'description', 'photo', 'quantity_available']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'item', 'status']
        
