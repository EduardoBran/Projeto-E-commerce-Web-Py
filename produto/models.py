from categoria.models import Categoria
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from utils import utils


class Produto(models.Model):
    nome = models.CharField(max_length=24)
    categoria_produto = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoria')
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
        default='L',
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

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['id']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(
        max_length=3, verbose_name="Nome (Máx de 3 caracteres)")
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(
        default=0, verbose_name='Preço promocional')
    estoque = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações (obrigatório)'


class BaseFavorito(models.Model):
    criados = models.DateField(verbose_name='Criação', auto_now_add=True)
    modificado = models.DateField(verbose_name='Atualização', auto_now=True)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        abstract = True


class Favorito(BaseFavorito):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')

    def __str__(self):
        return f'{self.usuario}'


class ItemFavorito (BaseFavorito):
    favorito = models.ForeignKey(Favorito, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(
        default=0, verbose_name='Preço Promocional')
    slug = models.CharField(max_length=255)
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.favorito}'

    class Meta:
        verbose_name = 'Item favorito'
        verbose_name_plural = 'Itens favoritados'
