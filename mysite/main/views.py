from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    l1 = "<a href=\"/enquetes\">Aplicação de Enquetes</a><br/>"
    l2 = "<a href=\"/projeto\">Projeto da Disciplina</a><br/>"
    return HttpResponse(l1+l2)