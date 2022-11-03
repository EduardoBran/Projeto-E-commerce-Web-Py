from django.test import TestCase
from model_mommy import mommy


class CategoriaTestCase(TestCase):
    def setUp(self):
        self.categoria = mommy.make('Categoria')

    def test_str(self):
        self.assertEquals(str(self.categoria), self.categoria.nome_cat)
