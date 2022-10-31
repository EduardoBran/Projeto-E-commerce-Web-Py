from django.contrib.auth.models import User
from django.db import models


class Pedido(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    criado = models.DateField(verbose_name='Criação', auto_now_add=True)
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )
    modificado = models.DateField(verbose_name='Atualização', auto_now=True)

    def __str__(self):
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255, verbose_name='Variação')
    variacao_id = models.PositiveIntegerField(verbose_name='Variação Id')
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(
        default=0, verbose_name='Preço Promocional')
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
