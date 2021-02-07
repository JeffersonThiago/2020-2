import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Pergunta
from django.urls import reverse


def cria_enquete(texto, quant_dias):
    """
    Cria um objeto da classe Pergunta, com um texto e uma data, representada
    por uma quantidade de dias (positiva ou negativa) e salva ela no banco de
    teste
    """
    data_teste = timezone.now() + datetime.timedelta(days=quant_dias)
    return Pergunta.objects.create(texto=texto, data_publicacao = data_teste)

### testes para classe de index view####
##############################################


class IndexViewTest(TestCase):
    def test_indexview_sem_perguntas(self):
        """
        Se não existe enquetes cadastradas é exibida uma mensagem apropiada.
        """
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code,200)
        self.assertContains(resposta,"Nenhuma enquete cadastrda até o momento")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],[])

    def test_indexview_com_enquete_no_passado(self):
        """
        Enquetes com data de publicação no passado são apresentadas.
        """
        cria_enquete(texto="Enquete no passado", quant_dias=-30)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code,200)
        self.assertContains(resposta,"Enquete no passado")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],['<Pergunta: Enquete no passado>'])

    def test_indexview_com_enquete_no_futuro(self):
        """
        Enquetes com data de publicações no futuro NÃO são exibidas.
        """
        cria_enquete(texto="Enquete no futuro", quant_dias=30)

        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code,200)
        self.assertContains(resposta,"Nenhuma enquete cadastrda até o momento")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],[])

    def test_indexview_com_enquete_no_passado_e_outra_no_futuro(self):
        """
        Apenas a enquete com data de publicação no passado devera ser apresentada
        """
        cria_enquete(texto="Enquete no passado", quant_dias=-2)
        cria_enquete(texto="Enquete no futuro", quant_dias=2)
        resposta = self.client.get(reverse('enquetes:index'))

        self.assertEqual(resposta.status_code,200)
        self.assertContains(resposta,"Enquete no passado")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],
            ['<Pergunta: Enquete no passado>'])

    def test_indexview_com_duas_enquetes_no_passado(self):
        """
        ambas as enquetes devem ser apresentadas no resultado
        """
        cria_enquete(texto="Enquete no passado 1", quant_dias=-10)
        cria_enquete(texto="Enquete no passado 2", quant_dias=-5)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code,200)
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],
            ['<Pergunta: Enquete no passado 1>',
            '<Pergunta: Enquete no passado 2>'])

#### testes para classe detailview###
#########################################

class DetailViewTest(TestCase):
    """
    Está view deverá retornar um codigo 404 para enquetes com data no futuro.
    """
    def test_enquete_no_futuro(self):
        enq_futura = cria_enquete(texto="Enquete no futuro", quant_dias=5)
        url = reverse('enquetes:detalhes', args=(enq_futura.id,))
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code,404)

    def test_enquete_no_passado(self):
        """
        Detalhes de enquetes com data no passado são exibidos sem problemas.
        """

        enq_passado = cria_enquete(texto="Enquete no passado", quant_dias=-5)
        url = reverse('enquetes:detalhes', args=(enq_passado.id,))
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code,200)
        self.assertContains(resposta, enq_passado.texto)

