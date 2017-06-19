from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np

from numpy import pi
from qutip import *
#so para testes
from IPython.display import Image

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
  json_data = json_loads_byteified(request.body)
  print(json_data['data'])
  numBit = json_data['len']
  print("length: "+str(numBit))
  qcircuit = QubitCircuit(json_data['len'])
  #foi o jeito que achei para inicializar o circuito
  qcircuit.add_gate("SNOT", 0)
  qcircuit.add_gate("SNOT", 0)

  #iterar entre os dados passados
  for key, gates in json_data['data'].iteritems():
    print("testando: "+key+"  -  "+str(gates))
    for gate in gates:
      print("Gate: "+key+" => "+gate)
      if gate != "line":
        #qcircuit.add_1q_gate("SNOT", int(key))
        qcircuit.add_gate("SNOT", int(key))
        #qcircuit.add_gate("RY", int(key), None, 1, "")


  U_list0 = qcircuit.propagators()
  U0 = gate_sequence_product(U_list0)
  print("-----U0--------")
  print(U0)
  print("----data---------")
  print(U0.data)
  print("----eigenenergies---------")
  print(U0.eigenenergies())
  print("----eigenstates---------")
  print(U0.eigenstates())
  print("----htmlify_matrix_str---------")
  print(htmlify_matrix_str(U0))
  print("----htmlify_matrix---------")
  print(htmlify_matrix(U0))
  print("----unit---------")
  print(U0.unit())
  print("------New Qobj-------")
  Qmin = Qobj([[0],[1],[0],[0]])
  print(Qmin)
  print("------New Qobj Data-------")
  print(Qmin.data)
  print("------max Qobj-------")
  Qmax = Qobj([[1],[0],[1],[0]])
  print(Qmax)
  print("------max Qobj Data-------")
  print(Qmax.data)
  print("-----Matrix elemet-----")
  #print(U0.matrix_element(Qmin,Qmax))

  #qcircuit.png

  print("----###########---------")
  print("----###########---------")
  isUtil = 0
  result = resultInitTransp(numBit)
  seqTrans = []

  for key, gates in json_data['data'].iteritems():
    print("testando: "+key+"  -  "+str(gates))
    for gate in gates:
      print("Gate: "+key+" => "+gate)
      if gate != "line":
        seqTrans.insert(0,gate)
        result[int(key)] = applyTransf(gate,result[int(key)])

  print("-----Result------")
  print(result)
  print("-----to JSON------")
  prepareResultJSON(result)
  print("-----Fim Result----")
  print("seqTrans %s" % (seqTrans))
  q = Qobj([[1,0],[1,0]])
  print(q)
  print(q.data)
  print(q.full())
  print(q.norm())
  # for i in range(0,2):
  #   for j in range(0,2):
  #     for k in range(0,2):
  #       for l in range(0,2):
  #         q = Qobj([[i,j],[k,l]])
  #         print(q)
  #         print(q.data)
  #         print(q.full())
  #         print(q.norm())
  print("----Sigmay()---")
  print(sigmay())
  print("----Sigmaz()---")
  print(sigmaz())
  print("q * Sigmax")
  t = q*sigmax()
  print(t)
  print(t.data)
  print(t.full())
  print(t.norm())

  #test
  print("-----init*U0--------")
  arrayTest=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
  arrayTest=[[0.707,0,0.707,0],[0,0.707,0,0.707],[0.707,0,-0.707,0],[0,0.707,0,-0.707]]
  arrayTest=[[0.5,0.5,0.5,0.5],[0.5,-0.5,0.5,-0.5],[0.5,0.5,-0.5,-0.5],[0.5,-0.5,-0.5,0.5]]

  '''
  print(dado[0].split(","))
  print(dado[0][:-1].split(",")) # split sem pegar a ultima virgula
  '''

  # criar funcao para aplicar as transfomacoes da lib de quantica dependendo da porta que foi utilizada

  prepareResultJSON(result)
  data = {
    'msg' : str(htmlify_matrix(U0)),
    'result' : prepareResultJSON(result) #ajusta tipo de dados do result
  }
  print("**** Fim *****")
  #return json.dumps(data)
  return JsonResponse(data)

def applyTransf(strGate, qubit):
  if strGate == "x":
    return np.dot([[0.0,1.0],[1.0,0.0]],qubit)
  elif strGate == "y":
    return np.dot([[0.0,1.0],[1.0,0.0]],qubit)
  elif strGate == "z":
    return np.dot([[0.0,1.0],[1.0,0.0]],qubit)
  elif strGate == "not":
    return qubit
  elif strGate == "h":
    return np.dot([[1.0,1.0],[1.0,-1.0]],qubit)*(1/np.sqrt(2))
  elif strGate == "i":
    return np.dot([[1.0,0.0],[0.0,1.0]],qubit)
  elif strGate == "s":
    return qubit
  elif strGate == "sr":
    return qubit
  elif strGate == "sw":
    return qubit


###
# Funcoes para format de um ndarray
###
def htmlify_matrix_str(ndarray):
  output = ""
  for row in ndarray:
      #output += "<tr>"
      for col in row:
          output += "" + str(col) + "\n"
          for lv in col:
            print(lv)
      #output += "</tr>"
  #output += "</table>"
  return output
def htmlify_matrix(ndarray):
  output = "<table>"
  for ele in ndarray:
    for row in ele:
        output += "<tr>"
        for col in row:
            output += "<td>" + stringify_num(col) + "</td>"
        output += "</tr>"
  output += "</table>"
  return output
def stringify_num(num):
  if num.imag != 0:
      output = '{0.real:.3f} + {0.imag:.3f}j'.format(num)
  else:
      output = '{0.real:.3f}'.format(num)
  output = output.replace("0.000", "0")
  output = output.replace(" + 0j", "")
  output = output.replace("0 + ", "")
  output = output.replace(".000", "")
  output = output.replace("00 ", " ") ## trailing zeros...
  output = output.replace("00j", "j") 
  output = output.replace("0 ", " ") 
  output = output.replace("0j", "j") ## also only for trailing zeros
  output = output.replace("1j", "j")
  output = output.replace("j", "<i>i</i>")
  output = output.replace("+ -", "- ")
  output = output.replace("-", "&ndash;")
  assert type(output) is str
  return output

#initialize array
def resultInit(n):
  result=[]
  for i in range(0,n):
    result.append([1,0])
  return result

def resultInitTransp(n):
  result=[]
  for i in range(0,n):
    result.append([[1.0],[0.0]])
  return result

def resultInitCol(n):
  result=[]
  for i in range(0,n):
    result.append([1])
    result.append([0])
  return result
#faz tratamnto caso exista algum np.array (nao eh serializavel)
def prepareResultJSON(result):
  resp = []
  for pair in result:
    if type(pair) is np.ndarray:
      pair = pair.tolist()
    resp.append(pair)
  return resp

###
#funcao para decodificar o JSON de UTF-8 para string
###
def json_loads_byteified(json_text):
  return _byteify(
    json.loads(json_text, object_hook=_byteify),
    ignore_dicts=True
  )
def _byteify(data, ignore_dicts = False):
  # if this is a unicode string, return its string representation
  if isinstance(data, unicode):
    return data.encode('utf-8')
  # if this is a list of values, return list of byteified values
  if isinstance(data, list):
    return [ _byteify(item, ignore_dicts=True) for item in data ]
  # if this is a dictionary, return dictionary of byteified keys and values
  # but only if we haven't already byteified it
  if isinstance(data, dict) and not ignore_dicts:
    return {
      _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
      for key, value in data.iteritems()
    }
  # if it's anything else, return it in its original form
  return data

