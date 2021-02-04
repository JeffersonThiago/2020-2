from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Pergunta, Opcao
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'ultimas_enquetes'
    def get_queryset(self):
        return Pergunta.objects.order_by('data_publicacao')[:5]

class DetalhesView(generic.DetailView):
    model = Pergunta
    context_object_name = 'enquete'
    template_name = 'enquetes/detalhes.html'

class ResultadoView(generic.DetailView):
    model = Pergunta
    context_object_name = 'enquete'
    template_name = 'enquetes/resultados.html'

def votacao(request, enquete_id):
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