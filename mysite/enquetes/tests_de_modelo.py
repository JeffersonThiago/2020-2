import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Pergunta



###### TESTE PARA CLASSE PERGUNTA###
#####################################

class PerguntaTeste(TestCase):
    def test_publicada_recentemente_com_data_no_futuro(self):
        """
        O metodo publicada_recentemente() deve retornar False
        para Perguntas com data de publicação no futuro.
        """
        data_teste = timezone.now() + datetime.timedelta(days=30)
        pergunta = Pergunta(data_publicacao = data_teste)
        self.assertIs(pergunta.publicada_recentemente(),False)

    def test_publicada_recentemente_com_data_no_passado(self):
        """
        O metodo pulicada_recentemente deve retornar False
        para Perguntas com data de publicação anterior as ultimas 24hs.
        """
        data_teste = timezone.now() - datetime.timedelta(days=1,seconds=1)
        pergunta = Pergunta(data_publicacao = data_teste)
        self.assertIs(pergunta.publicada_recentemente(),False)


    def test_publicada_recentemente_com_data_dentro_das_24hs(self):

        """
        O metodo pulicada_recentemente deve retornar True
        para Perguntas com data de publicação dentro das ultimas 24hs.
        """
        data_teste = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        pergunta = Pergunta(data_publicacao = data_teste)
        self.assertIs(pergunta.publicada_recentemente(),True)

