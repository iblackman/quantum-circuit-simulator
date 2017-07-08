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
  context = {'arrPortas':['h','x','y','z','not','sr','sw','point','line'],
    'numMaxPortas': range(n),
    'portaDefault': 'line',
  }
  return render(request, 'simulador/index.html', context)

# funcao de ajax para processar o circuito
@csrf_exempt  # para receber os dados por post
def calcular(request):
  print("***** Inicio *****")
  json_data = json_loads_byteified(request.body)
  
  numBit = json_data['len']

  connections = prepareConnections(json_data['connections'].iteritems())
  ###
  #  execution using qubitcircuit
  ###
  qcircuit = QubitCircuit(numBit)

  #arrumando ordem dos dados para inserir os gates corretamente
  #os circuitos estavam vindo em ordem estranha
  circuitList = []
  for key, gates in json_data['data'].iteritems():
    circuitList.insert(int(key),gates)


  for i in range(0,len(circuitList[0])):
    for j in range(0,numBit):
      gate = circuitList[j][i]
      if gate != "line":
        if(connections.has_key(str(i))):
          connDict = connections.get(str(i))
          auxKey = j + 1
          targetAux = connDict.get(str(auxKey))
          if targetAux != None:
            target = j
            control = int(targetAux)-1
            if gate == "not":
              qcircuit.add_gate("CNOT", targets=[target], controls=[control])
            elif gate == "sw":
              qcircuit.add_gate("SWAP", targets=[target,control])
            elif gate == "sr":
              qcircuit.add_gate("SQRTNOT", targets=[target], controls=[control])
        else:
          if gate == "x":
            qcircuit.add_gate("RX", j, arg_value=-pi)
          elif gate == "y":
            qcircuit.add_gate("RY", j, arg_value=pi)
          elif gate == "z":
            qcircuit.add_gate("RZ", j, arg_value=pi)
          elif gate == "h":
            qcircuit.add_gate("SNOT", j)


  result = resultInitTransp(numBit)
  
  qInput = initializeInput(numBit)


  U0 = gate_sequence_product(qcircuit.propagators())

  qFinal = U0*qInput

  msg = resultToText(numBit, qFinal.full())
  msg += "<br/>"
  #coloquei isso prq nao quero trazer o resultado com o numero complexo, entao o result ja e suficiente
  msg =  ""
  if(U0 == 1):
    msg += htmlify_matrix(qeye(2**numBit))
  else:
    msg += htmlify_matrix(U0)
  ###Fim teste

  prepareResultJSON(result)
  data = {
    'msg' : msg,#str(htmlify_matrix(U0)),
    'result' : resultToTextSimple(numBit, qFinal.full()) 
  }
  print("**** Fim *****")
  #return json.dumps(data)
  return JsonResponse(data)

###
# initialize the column vector of inputs depending on how many bits has the circuit
###
def initializeInput(n):
  ket = basis(2,0)
  result = []
  for i in range(0,n):
    result.append(ket)
  return tensor(result)

###
# receive number of bits in the circuit and Qobj after gate sequence product
##
def resultToText(n, arr):
  arrSum = sum(np.absolute(arr))
  #format int to binary with leading 0 nth times
  strFormat = "0"+str(n)+"b"
  result = ""
  for i in range(0,arr.size):
    #get value
    aux = arr[i][0]
    if(aux != 0j):
      #calculate porcentage
      porcent = abs(aux/arrSum).real[0] *100
      #format index to binary
      strBit = format(i, strFormat)
      #concatenate result
      result += str(aux) + " |" + strBit + "> " + str(porcent) + "%<br/>"
  return result

###
# Similar to function resultToText, but doesnt bring the value
###
def resultToTextSimple(n, arr):
  arrSum = sum(arr)
  #format int to binary with leading 0 nth times
  strFormat = "0"+str(n)+"b"
  result = ""
  for i in range(0,arr.size):
    #get value
    aux = arr[i][0]
    if(aux != 0j):
      #calculate porcentage
      porcent = (aux/arrSum).real[0] *100
      #format index to binary
      strBit = format(i, strFormat)
      #concatenate result
      result += " |" + strBit + "> &nbsp;&nbsp;&nbsp;&nbsp;" + str(porcent) + "%<br/>"
  return result

###
# returns a array with connections 
###
def prepareConnections(arr):
  result = {}
  for key, value in arr:
    aux = value.split("-")
    result[aux[2]] = {aux[0]:aux[1]}
    #result.append()
  return result


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

