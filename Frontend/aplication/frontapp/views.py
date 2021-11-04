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
        peticionDatos2 =requests.get('http://localhost:5000/ConsultaSalida')
        facbue =requests.get('http://localhost:5000/Consulta_fac_bue')
        facmal =requests.get('http://localhost:5000/Consulta_fac_mal')
        mensajeerror =requests.get('http://localhost:5000/ConsultamensajeError')
        factot =requests.get('http://localhost:5000/Consulta_fac_tot')
        facini =requests.get('http://localhost:5000/Consulta_fac_ini')
        
        context = {
            'Salida': peticionDatos.text,
            'Entrada': peticionEntrada.text,
            'Salida2': peticionDatos2.text,
            'facbue': json.loads(facbue.text),
            'facmal': json.loads(facmal.text),
            'mensaje': json.loads(mensajeerror.text),
            'factot': json.loads(factot.text),
            'facini': json.loads(facini.text),
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
        # payload = {"fechaslist":"usernae","password":"password"}
        peticionDatos= requests.get('http://localhost:5000/ResumenIva')
        # peticionDatos2= requests.get('http://localhost:5000/ResumenIva_recibido', json=payload)
        fechas=requests.get('http://localhost:5000/ResumenIva_Fechas')
        print("████████████")         
        print(peticionDatos.text)
        context = {
            'fechaslist': json.loads(fechas.text),
            'iva_ruta': json.loads(peticionDatos.text),
            # 'iva_recibido': json.loads(peticionDatos2.text),
        }
        return render(request, 'resumeniva.html', context)

def resumenrango(request):
    if request.method == 'GET':
        # payload = {"fechaslist":"usernae","password":"password"}
        peticionDatos= requests.get('http://localhost:5000/ResumenRango')
        # peticionDatos2= requests.get('http://localhost:5000/ResumenIva_recibido', json=payload)
        fechas1=requests.get('http://localhost:5000/Fechas_Range')
        # fechas2=requests.get('http://localhost:5000/ResumenIva_Fechas')
        print("████████████")         
        print(peticionDatos.text)
        context = {
            'fechaslist1': json.loads(fechas1.text),
            'fechaslist2': json.loads(fechas1.text),
            'iva_ruta': json.loads(peticionDatos.text),
            # 'iva_recibido': json.loads(peticionDatos2.text),
        }
        return render(request, 'resumenrango.html', context)



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
    
def docu(request):
    return render(request, 'Docu.html')

