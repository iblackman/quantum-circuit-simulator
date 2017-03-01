from django.shortcuts import render

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
