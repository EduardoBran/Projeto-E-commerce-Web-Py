import re
from datetime import date
from unittest.mock import NonCallableMagicMock

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from utils.validacpf import valida_cpf


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    idade = models.PositiveIntegerField(default=0)
    data_nascimento = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50, verbose_name='Endereço')
    numero = models.CharField(max_length=5, verbose_name='Número')
    complemento = models.CharField(max_length=30, blank=True, null=True)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='AC',
        choices=(
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
        )
    )

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):
        error_messages = {}

        idade = date.today().year - self.data_nascimento.year - \
            ((date.today().month, date.today().day) <
             (self.data_nascimento.month, self.data_nascimento.day))

        if idade < 18:
            error_messages['data_nascimento'] = 'O cadastro só é possível para maiores de 18 anos.'

        if self.data_nascimento.year < (date.today().year - 100) or self.data_nascimento.year > date.today().year:
            error_messages['data_nascimento'] = 'Data inválida.'

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já existe.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 dígitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        ano_user = self.data_nascimento.year
        mes_user = self.data_nascimento.month
        dia_user = self.data_nascimento.day
        ano_atual = date.today().year
        mes_atual = date.today().month
        dia_atual = date.today().day
        # print(f'Ano - {ano_atual} ||| Mês - {mes_atual} ||| Dia - {dia_atual}')

        idade = ano_atual - ano_user - \
            ((mes_atual, dia_atual) < (mes_user, dia_user))

        self.idade = idade

        super(Perfil, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
