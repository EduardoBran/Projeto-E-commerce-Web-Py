from django import forms
from django.contrib.auth.models import User

from . import models


class PerfilForm(forms.ModelForm):
    cpf = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput',
                   'maxlength': 14
                   }
        ),
        help_text='Informar somente números.'
    )
    data_nascimento = forms.DateField(
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'date',
                   'class': 'input1 form-control textinput textInput'}
        ),
        label='Data de nascimento*'
    )
    cep = forms.CharField(
        required=True,
        widget=forms.TextInput(  # oninput necessário para o maxlength funcionar
            attrs={  # 'type': 'number',
                'class': 'input1 form-control textinput textInput',
                # 'oninput': 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
                'onblur': 'pesquisacep(this.value);',
                'maxlength': 9}
        ),
        help_text='Informar somente números.'
    )
    endereco = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput'}
        ),
        label='Logradouro'
    )
    numero = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput',
                   'maxlength': 4}
        ),
        label='Número'
    )
    complemento = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput',
                   'maxlength': 25}
        ),
    )
    bairro = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput',
                   'maxlength': 30}
        ),
    )
    cidade = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput',
                   'maxlength': 30}
        ),
    )
    choices = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    estado = forms.CharField(
        required=True,
        widget=forms.Select(
            attrs={'class': 'input1 form-control textinput textInput'},
            choices=choices,
        )
    )

    class Meta:
        model = models.Perfil
        fields = ('cpf', 'data_nascimento', 'cep',
                  'endereco', 'numero', 'complemento',
                  'bairro', 'cidade', 'estado'
                  )
        exclude = ('usuario',)


class UserForm(forms.ModelForm):

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput', }
        ),
        label='Usuário',
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'input1 form-control textinput textInput', }
        ),
        label='Senha',
        help_text='Ex: mínimo de 6 caracteres com letras e números.'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'input1 form-control textinput textInput'}
        ),
        label='Confirmação senha',
        help_text='Informe a mesma senha informada anteriormente, para verificação.'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'input1 form-control textinput textInput'}
        ),
        label='E-mail',
        help_text='Ex: seuemail@dominio.com.br'
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput'}
        ),
        label='Nome'
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'input1 form-control textinput textInput'}
        ),
        label='Sobrenome'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe.'
        error_msg_email_exists = 'E-mail já existe.'
        error_msg_password_match = 'As duas senhas não conferem.'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres.'
        error_msg_require_field = 'Este campo é obrigatório.'

        # Usuários logados: atualização
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        # Usuários não logados: cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_require_field

            if not password2_data:
                validation_error_msgs['password2'] = error_msg_require_field

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
