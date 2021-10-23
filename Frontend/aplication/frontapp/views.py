from django.shortcuts import render, redirect
from xml.dom import minidom
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import requests
import json
# Create your views here.
endpoint = 'http://localhost:5000{}'


def index(request):
    if request.method == 'GET':        
        peticionDatos= requests.get('http://localhost:5000/ConsultaDatos')
        peticionEntrada =requests.get('http://localhost:5000/ConsultaXMLentrada')
        # mensajeerror =requests.get('http://localhost:5000/ConsultamensajeError')
        
        context = {
            'Salida': peticionDatos.text,
            'Entrada': peticionEntrada.text,
            # 'mensaje': mensajeerror.text,
        }
        # print(peticionDatos.text)
        print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬BIENVENIDO GET▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
        return render(request, 'inicio.html', context)

    elif request.method == 'POST':
        document = request.FILES['document']
        data = document.read()
        peticionDatos=requests.post('http://localhost:5000/Procesar', data)
        print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬BIENVENIDO POST▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
        # print(peticionDatos.text)
        context = {
            'mensaje': json.loads(peticionDatos.text),
        }
        return render(request, 'inicio.html', context)
        # return redirect('inicio')



def resumeniva(request):
    if request.method == 'GET':
        payload = {"fechaslist":"usernae","password":"password"}
        peticionDatos= requests.get('http://localhost:5000/ResumenIva_emitido')
        peticionDatos2= requests.get('http://localhost:5000/ResumenIva_recibido', json=payload)
        fechas=requests.get('http://localhost:5000/ResumenIva_Fechas')
        print("████████████")         
        
        context = {
            'fechaslist': json.loads(fechas.text),
            'iva_emitido': json.loads(peticionDatos.text),
            'iva_recibido': json.loads(peticionDatos2.text),
        }
        return render(request, 'resumeniva.html', context)

def resumenrango(request):
    return render(request, 'resumenrango.html')



def reset(request):
    if request.method == 'PATCH':
        peticionDatos = requests.patch('http://localhost:5000/reset')
        context = {
            'Salida': peticionDatos.text,
            'Entrada': peticionDatos.text,
        }        
        return render(request, 'inicio.html', context)

def Reportes(request):
    return render(request, 'reportes.html')

def Graficas(request):
    return render(request, 'Graficas.html')

def misdatos(request):
    return render(request, 'misdatos.html')
def reports(request):
    if request.method == 'GET':
        date = request.GET.get('date', None)
        code = request.GET.get('code', None)

        context = {
            'date': None,
            'code': None,
        }
        if date is not None:
            context['date'] = date

        if code is not None:
            context['code'] = code
        return render(request, 'reports.html', context)


def calc(request):
    if request.method == 'GET':
        num_1 = request.GET.get('num_1', 0)
        num_2 = request.GET.get('num_2', 0)

        url = endpoint.format('/potencia')

        potencia = requests.get(url, {
            'num_1': num_1,
            'num_2': num_2,
        })

        context = {
            'potencia': potencia.text,
        }

        return render(request, 'calc.html', context)
