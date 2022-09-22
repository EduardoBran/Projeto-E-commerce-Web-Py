import os

from categoria.models import Categoria
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image
from utils import utils


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    categoria_produto = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING,  blank=True, null=True, verbose_name='Categoria')
    descricao_curta = models.TextField(
        max_length=255, verbose_name='Descrição curta')
    descricao_longa = models.TextField(verbose_name='Descrição longa')
    imagem = models.URLField(blank=True, null=True, verbose_name='Imagem 1')
    imagem2 = models.URLField(blank=True, null=True, verbose_name='Imagem 2')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(
        default=0, verbose_name='Preço Promo. ')
    tipo = models.CharField(
        default='N',
        max_length=1,
        choices=(
            ('N', 'Nenhum'),
            ('D', 'Destaque'),
            ('L', 'Lançamento'),
            ('V', 'Mais Vendido'),
        )
    )

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['id']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(
        default=0, verbose_name='Preço promocional')
    estoque = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
