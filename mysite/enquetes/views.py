from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Pergunta, Opcao
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        ultimas_enquetes = Pergunta.objects.filter(
            data_publicacao__lte=timezone.now()
            ).order_by('data_publicacao')[:5]
        contexto = {'ultimas_enquetes': ultimas_enquetes}
        return render(request, 'enquetes/index.html', contexto)

class DetalhesView(generic.View):
    def get(self, request, *args, **kwargs):
        enquete_id = self.kwargs['pk']
        enquete = get_object_or_404(Pergunta, pk=enquete_id)
        agora = timezone.now()
        if enquete.data_publicacao>agora:
            raise Http404('Não existe nenhuma enquete com essa identificação')
        return render(request, 'enquetes/pergunta_detail.html', {'pergunta':enquete})


class ResultadoView(generic.View):
    def get(self, request, *args, **kwargs):
        enquete_id = self.kwargs['pk']
        enquete = get_object_or_404(Pergunta, pk=enquete_id)
        return render(request, 'enquetes/resultados.html', {'enquete':enquete})

class VotacaoView(generic.View):
    def post(self, request, *args, **kwargs):
        enquete_id = self.kwargs['enquete_id']
        enquete = get_object_or_404(Pergunta, pk=enquete_id)
        try:
            op_desejada = enquete.opcao_set.get(pk = request.POST['opcao'])
        except (KeyError, Opcao.DoesNotExist):
            contexto = {
                'enquete': enquete,
                'error_message': "Deve ser selecionada uma opção valida"
            }
            return render(request, 'enquetes:detalhes', contexto)

        else:
            op_desejada.votos += 1
            op_desejada.save()
            return HttpResponseRedirect(reverse('enquetes:resultado',
                args=(enquete.id,)))
