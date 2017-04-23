from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from qutip import *

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
  seqTrans = []
  for values in request.POST.iterlists():
    for v in values:
      # pega apenas a lista com valores, pula o index
      if i == 1:
        print("linha %s => %s" % (i,v))
        dado.insert(0,v)
        # itera entre os gates do array
        for gate in v:
          if gate != "line":
            seqTrans.insert(0,gate)
      i = not(i)
  print("______")
  print(dado)
  print("seqTrans %s" % (seqTrans))
  q = Qobj([[0,1],[1,0]])
  print(q)
  t = q*sigmax()
  print(t.data)
  print(t.full())
  '''
  print(dado[0].split(","))
  print(dado[0][:-1].split(",")) # split sem pegar a ultima virgula
  '''

  # criar funcao para aplicar as transfomacoes da lib de quantica dependendo da porta que foi utilizada

  data = {
    'msg' : str(t.data)
  }
  print("**** Fim *****")
  return JsonResponse(data)

  def applyTransf(strGate, qobj):

    if strGate == "x":
      return qobj*sigmax()
    elif strGate == "y":
      return qobj*sigmay()
    elif strGate == "z":
      return qobj*sigmaz()
    elif strGate == "not":
      print("ry")
    elif strGate == "h":
      print("ry")
    elif strGate == "i":
      return qobj*qeye(2)
    elif strGate == "s":
      print("ry")
    elif strGate == "sr":
      print("ry")
    elif strGate == "sw":
      print("ry")