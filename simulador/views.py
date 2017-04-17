from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request, numPortas = 0):
  num = int(numPortas)
  if num > 0:
    n = num
  else:
    n = 10
  context = {'arrPortas':['h','x','i','s','y','z','not','sr','sw','point','line'],
    'numMaxPortas': range(n),
    'portaDefault': 'line',
  }
  return render(request, 'simulador/index.html', context)

# funcao de ajax para processar o circuito
@csrf_exempt  # para receber os dados por post
def calcular(request):
  print("***** Inicio *****")
  print(request.POST)
  i = 0
  dado = []
  for values in request.POST.iterlists():
    for v in values:
      if i == 1:
        print("linha %s => %s" % (i,v))
        dado.insert(0,v)
      i = not(i)
  print("______")
  print(dado)
  '''
  print(dado[0].split(","))
  print(dado[0][:-1].split(",")) # split sem pegar a ultima virgula
  '''

  # criar funcao para aplicar as transfomacoes da lib de quantica dependendo da porta que foi utilizada

  data = {
    'msg' : dado
  }
  print("**** Fim *****")
  return JsonResponse(data)