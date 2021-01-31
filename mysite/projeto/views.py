from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    resposta = "Projeto da disciplina"
    return HttpResponse(resposta)