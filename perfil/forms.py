from cProfile import label

from django import forms
from django.contrib.auth.models import User

from . import models


class PerfilForm(forms.ModelForm):
    # endereco = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(),
    #     label='ENDEREÇO!!!',
    #     help_text='tag small lá do form'
    # )
    data_nascimento = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = models.Perfil
        fields = ('idade', 'data_nascimento', 'cpf',
                  'endereco', 'numero', 'complemento',
                  'bairro', 'cep', 'cidade', 'estado'
                  )
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
        # help_text=''
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'first_name', 'last_name', 'email')

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
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracters.'
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
