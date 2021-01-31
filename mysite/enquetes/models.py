from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Pergunta(models.Model):
    texto = models.CharField(max_length = 200)
    data_publicacao = models.DateTimeField('Data de Publicação')

    def __str__(self):
        return self.texto

    def publicada_recentemente(self):
        return self.data_publicacao >= timezone.now() - datetime.timedelta(days=1)


class Opcao(models.Model):
    texto = models.CharField(max_length = 100)
    votos = models.IntegerField(default = 0)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)

    def __str__(self):
        return self.texto
