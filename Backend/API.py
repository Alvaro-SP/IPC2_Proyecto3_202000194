import re
from xml.etree import ElementTree as ET
from xml.dom import minidom
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from dateutil.parser import parse
import xmltodict
from Peticiones import peticiones
from Errores import errores
from Datos import datos
from Dias import dias
import json
app = Flask(__name__)
cors = CORS(app, resourses={r"/*": {"origin": "*"}})

peticion = peticiones()
entradaglobal = ""
fecha_resumen = ""
cont_EntradaXML=1 #*CONTADOR DE TIPO ENTERO
cont_SalidaXML=1 #*CONTADOR DE TIPO ENTERO
mensaje_errores=""

#!██████████████████    RESETEAR TODO     █████████████████████

@app.route('/reset', methods=['PATCH'])
def reset_state():
    global entradaglobal
    peticion.reiniciar_todo()
    entradaglobal = ""
    return Response(status=204)


#!██████████████████    LECTURA DE XML     █████████████████████
# ?LEER EL XML DE ENTRADA
# TODO██████████████████   PROCESO    █████████████████████
# ?POSTEAR EL PROCESO
@app.route('/Procesar', methods=['POST'])
def post_events():
    # parse_request = request.data.decode('utf-8')
    global entradaglobal
    global cont_EntradaXML
    global mensaje_errores
    parse_request = request.json['XMLdatos']
    #  '+str(cont_EntradaXML)+' -->
    archivo = open('XML_generados/archivo_Entrada_.xml', 'w')
    cont_EntradaXML+=1
    archivo.write(parse_request)
    archivo.close()

    entradaglobal = parse_request
    parse_request = parse_request.lower()

    root_machine = ET.fromstring(parse_request)
    
    list_referencia = []
    nit_emisor_invalid = 0
    nit_receptor_invalid = 0
    iva_error = 0
    total_error = 0
    referencia_duplicada = 0
    codigo_Ceros = "1"
    dicc_dias = {}
    cantidad_Facturas_Buenas = 0
    cantidad_Facturas_Malas = 0
    contadorDTE=0
    DTEerror=""

    for dtes in root_machine.findall('dte'):
        contadorDTE+=1
        try:
            print("-----------------------------------")
            tiempo = (dtes.find('tiempo'))  # .strip()
            fecha = re.search(r'\d{2,2}\/\d{2,2}\/\d{4,4}',
                            tiempo.text).group().strip()
            fechaoriginal = fecha
            referencia = dtes.find('referencia').text
            nit_emisor1 = dtes.find('nit_emisor').text
            nit_emisor = re.search(r'\d{1,20}(k|\d)', nit_emisor1).group().strip()
            nit_receptor1 = dtes.find('nit_receptor').text
            nit_receptor = re.search(r'\d{1,20}(k|\d)', nit_receptor1).group().strip()
            valor11 = (dtes.find('valor').text)
            iva1 = (dtes.find('iva').text)
            total1 = (dtes.find('total').text)
            valor = re.search(r'\d+\.\d{2}', valor11).group().strip()
            iva = re.search(r'\d+\.\d{2}', iva1).group().strip()
            total = re.search(r'\d+\.\d{2}', total1).group().strip()
            valor = float(valor)
            iva = float(iva)
            total = float(total)
            ivacalc = round((valor)*0.12, 2)
            totalcalc = (valor)+(ivacalc)
            print("IVA CALCULADO: ", ivacalc)
            print("IVA LEÍDO: ", iva)
            print("TOTAL CALCULADO: ", totalcalc)
            print("TOTAL LEÍDO: ", total)
            # print("NIT EMISOR CALCULADO: ", ivacalc)
            print("NIT EMISOR LEÍDO: ", nit_emisor)
            # print("NIT RECEPTOR CALCULADO: ", ivacalc)
            print("NIT RECEPTOR LEIDO: ", nit_receptor)

            #!validando los datos
            
            #! NIT
            valor1 = nit_emisor[-1]
            nit_emisor = nit_emisor[:-1]
            acum = 0
            position = 2
            for c in nit_emisor[::-1]:
                temp = position*int(c)
                position += 1
                acum += temp
            obtainmod = acum % 11
            result = 11-obtainmod
            print("EL RESULTADO nit RECEPTOR CALCULADO: ", result)
            print("EL ULTIMO DIGITO ES: ", valor1)
            #!NIT 2
            valor2 = nit_receptor[-1]
            nit_receptor = nit_receptor[:-1]
            acum2 = 0
            position2 = 2
            for c in nit_receptor[::-1]:
                temp2 = position2*int(c)
                position2 += 1
                acum2 += temp2
            obtainmod2 = acum2 % 11
            result2 = 11-obtainmod2
            print("EL RESULTADO nit RECEPTOR CALCULADO: ", result2)
            print("EL ULTIMO DIGITO ES: ", valor2)
            nitcorrect1 = False
            nitcorrect2 = False

            if str(result) == str(valor1) or ((str(result) == "10") and (str(valor1) == "k")):
                nitcorrect1 = True
            else:
                nitcorrect1 = False

            if str(result2) == str(valor2) or ((str(result2) == "10") and (str(valor2) == "k")):
                nitcorrect2 = True
            else:
                nitcorrect2 = False

            if iva == ivacalc and total == totalcalc and nitcorrect1 == True and nitcorrect2 == True and referencia not in list_referencia:
                cantidad_Facturas_Buenas += 1
                fecha = fecha.split("/")
                dia = int(fecha[0])
                diatext = fecha[0]
                mes = fecha[1]
                anio = fecha[2]
                print("Dia: ", dia, "Mes: ", mes, "Año: ", anio)
                #! CREACION DEL CODIGO DE REFERENCIA
                if dia not in dicc_dias:  # sino esta en los dias se agrega y se añade un codigo
                    codigoCeros_obtain = codigo_Ceros.zfill(8)
                    dicc_dias[dia] = codigoCeros_obtain
                    # print("EL CODIGO CONTADOR ES:", codigoCeros_obtain)

                elif dia in dicc_dias:
                    codigoCeros_obtain = int(dicc_dias.get(dia))
                    codigoCeros_obtain = str(codigoCeros_obtain+1)
                    codigoCeros_obtain = codigoCeros_obtain.zfill(8)
                    dicc_dias[dia] = codigoCeros_obtain

                Codigo_completo = str(anio)+str(mes) + \
                    str(diatext)+str(codigoCeros_obtain)
                print("EL CODIGO CONTADOR ES:", Codigo_completo)
                # parse(fechaoriginal, dayfirst=True)
                datosobj = datos(True, Codigo_completo, fechaoriginal,
                                referencia, nit_emisor, nit_receptor, valor, iva, total, 0, 0, 0, 0, 0)
                # TODO: se agrega el objeto
                peticion.agregar_peticion(datosobj)
                print(datosobj.date, " -->", datosobj.valido)
            else:
                cantidad_Facturas_Malas += 1
                refcont_temp = 0
                nit_emisor_temp = 0
                nit_receptor_temp = 0
                iva_error_temp = 0
                total_error_temp = 0
                if referencia in list_referencia:
                    print("REFERENCIA DUPLICADA")
                    referencia_duplicada += 1
                    refcont_temp += 1
                    # datosobj = datos(False, None, parse(fechaoriginal, dayfirst=True), referencia,nit_emisor, nit_receptor, valor, iva, total, 1,0,0,0,0)
                    # # TODO: se agrega el objeto
                    # peticion.agregar_peticion(datosobj)

                if nitcorrect1 != True:
                    print("NIT EMISOR MAL CALCULADO")
                    nit_emisor_invalid += 1
                    nit_emisor_temp += 1
                    # datosobj = datos(False, None, parse(fechaoriginal, dayfirst=True), referencia,nit_emisor, nit_receptor, valor, iva, total, 0,1,0,0,0)
                    # # TODO: se agrega el objeto
                    # peticion.agregar_peticion(datosobj)
                if nitcorrect2 != True:
                    print("NIT RECEPTOR MAL CALCULADO")
                    nit_receptor_invalid += 1
                    nit_receptor_temp += 1
                    # datosobj = datos(False, None, parse(fechaoriginal, dayfirst=True), referencia,nit_emisor, nit_receptor, valor, iva, total, 0,0,1,0,0)
                    # # TODO: se agrega el objeto
                    # peticion.agregar_peticion(datosobj)
                if iva != ivacalc:
                    print("IVA MAL CALCULADO")
                    iva_error += 1
                    iva_error_temp += 1
                    # datosobj = datos(False, None, parse(fechaoriginal, dayfirst=True), referencia,nit_emisor, nit_receptor, valor, iva, total, 0,0,0,1,0)
                    # # TODO: se agrega el objeto
                    # peticion.agregar_peticion(datosobj)
                if total != totalcalc:
                    print("TOTAL MAL CALCULADO")
                    total_error += 1
                    total_error_temp += 1
                    # datosobj = datos(False, None, parse(fechaoriginal, dayfirst=True), referencia,nit_emisor, nit_receptor, valor, iva, total, 0,0,0,0,1)
                    # # TODO: se agrega el objeto
                    # peticion.agregar_peticion(datosobj)
                datosobj = datos(False, None, fechaoriginal, referencia, nit_emisor, nit_receptor,
                                valor, iva, total, refcont_temp, nit_emisor_temp, nit_receptor_temp, iva_error_temp, total_error_temp)
                # TODO: se agrega el objeto
                peticion.agregar_peticion(datosobj)
                print(datosobj.date, " -->", datosobj.valido)
        except:
            DTEerror+="     "+str(contadorDTE)+" -> "+str(fechaoriginal)+" ,  \n"
            print(DTEerror)
            continue

    peticion.total_fac_buenasymalas(cantidad_Facturas_Buenas, cantidad_Facturas_Malas)
    
    # fin de la lectura ahora se guardan los datos
    if DTEerror!=[]:
        t="Por favor Revise los DTE: \n "+ DTEerror+"\n"
        mensaje_errores=t
        return jsonify(t)
    else:
        return jsonify("Archivo Correcto!")


@app.route('/ConsultaXMLentrada', methods=['GET'])
def getXMLentrada():
    global entradaglobal
    return Response(response=entradaglobal)
@app.route('/ConsultamensajeError', methods=['GET'])
def geterrormessage():
    global mensaje_errores
    return Response(response=mensaje_errores)


#!██████████████████   CONSULTAR DATOS    █████████████████████
# ?OBTENER LOS DATOS
@app.route('/ConsultaDatos', methods=['GET'])
def getDatos():
    global entradaglobal
    global cont_SalidaXML
    stats = peticion.proceso_datos_salida()
    document = minidom.Document()
    print(stats)

    if stats != []:
        root = document.createElement('SOLICITUD_AUTORIZACION')
        document.appendChild(root)

        for stat in stats:
            stat_element = document.createElement('AUTORIZACION')
            root.appendChild(stat_element)

            date_element = document.createElement('FECHA')
            date_element.appendChild(document.createTextNode(stat['date']))
            stat_element.appendChild(date_element)

            cant_fac_received = document.createElement('FACTURAS_RECIBIDAS')
            cant_fac_received.appendChild(
                document.createTextNode(str(stat['cant_facturas'])))
            stat_element.appendChild(cant_fac_received)

            errors_element = document.createElement('ERRORES')
            stat_element.appendChild(errors_element)

            nit_emisor = document.createElement('NIT_EMISOR')
            nit_emisor.appendChild(
                document.createTextNode(str(stat['nitcorrect1'])))
            errors_element.appendChild(nit_emisor)

            nit_receptor = document.createElement('NIT_RECEPTOR')
            nit_receptor.appendChild(
                document.createTextNode(str(stat['nitcorrect2'])))
            errors_element.appendChild(nit_receptor)

            iva = document.createElement('IVA')
            iva.appendChild(document.createTextNode(str(stat['iva'])))
            errors_element.appendChild(iva)

            total = document.createElement('TOTAL')
            total.appendChild(document.createTextNode(str(stat['total'])))
            errors_element.appendChild(total)

            referencia_duplicada = document.createElement(
                'REFERENCIA_DUPLICADA')
            referencia_duplicada.appendChild(
                document.createTextNode(str(stat['referencia'])))
            errors_element.appendChild(referencia_duplicada)

            cant_fac_corrects = document.createElement('FACTURAS_CORRECTAS')
            cant_fac_corrects.appendChild(
                document.createTextNode(str(stat['cant_corrects_fac'])))
            stat_element.appendChild(cant_fac_corrects)

            cant_emisor = document.createElement('CANTIDAD_EMISORES')
            cant_emisor.appendChild(
                document.createTextNode(str(stat['cant_emisors'])))
            stat_element.appendChild(cant_emisor)

            cant_receptor = document.createElement('CANTIDAD_RECEPTORES')
            cant_receptor.appendChild(
                document.createTextNode(str(stat['cant_receptors'])))
            stat_element.appendChild(cant_receptor)

            list_autorizations = document.createElement(
                'LISTADO_AUTORIZACIONES')
            stat_element.appendChild(list_autorizations)

            for user in stat['autorizaciones']:
                aprobacion = document.createElement('APROBACION')
                list_autorizations.appendChild(aprobacion)

                nit_del_emisor = document.createElement('NIT_EMISOR')
                nit_del_emisor.appendChild(
                    document.createTextNode(user['nit_emisor']))
                nit_del_emisor.setAttribute("ref", user['referencia'])
                aprobacion.appendChild(nit_del_emisor)

                codigo_de_aprobacion = document.createElement(
                    'CODIGO_APROBACION')
                codigo_de_aprobacion.appendChild(
                    document.createTextNode(str(user['codigo_aprobacion'])))
                aprobacion.appendChild(codigo_de_aprobacion)

            total_aprobaciones = document.createElement('TOTAL_APROBACIONES')
            total_aprobaciones.appendChild(
                document.createTextNode(str(stat['total_aprobacion'])))
            list_autorizations.appendChild(total_aprobaciones)

        XML_Salida = document.toprettyxml(indent='\t', newl='\n')
        #!ESCRITURA DEL ARCHIVO DE SALIDA
        #'+str(cont_SalidaXML)+'-->
        archivo = open('XML_generados/archivo_Salida_.xml', 'w', encoding="utf8")
        cont_SalidaXML+=1
        archivo.write(XML_Salida)
        archivo.close()
        return Response(response=XML_Salida, status=200, mimetype='application/xml', content_type='application/xml')
    else:
        return Response(response="")


#!██████████████████   RESUMEN IVA   █████████████████████
# ?OBTENER LOS IVA
@app.route('/ResumenIva', methods=['POST'])
def postfecha():
    global fecha_resumen
    date = request.json['date']
    fecha_resumen = date
    print("Fecha enviada: ", date)
    return Response(status=204)


@app.route('/ResumenIva_emitido', methods=['GET'])
def getIvas():
    global fecha_resumen
    date = fecha_resumen
    if date != "":
        iva_emitido = peticion.get_Resumen_Iva_Emitido(date)
        print(iva_emitido)
        return jsonify(iva_emitido)
    else:
        return jsonify("")


@app.route('/ResumenIva_recibido', methods=['GET'])
def getIvasReceived():
    global fecha_resumen
    date = fecha_resumen
    if date != "":
        iva_recibido = peticion.get_Resumen_Iva_Recibido(date)
        return jsonify(iva_recibido)
    else:
        return jsonify("")


@app.route('/ResumenIva_Fechas', methods=['GET'])
def getIvasfechas():
    fechaslist = peticion.get_Resumen_Iva_Fechas()
    if fechaslist != []:
        return jsonify(fechaslist)
    else:
        return jsonify("")


#!██████████████████   RESUMEN RANGO    █████████████████████
# ?OBTENER LOS PACIENTES
@app.route('/ResumenRango', methods=['GET'])
def getResumenes():

    pass
# OBTENER UN DATO

#!██████████████████   GRAFICA    █████████████████████
# ?OBTENER LOS PACIENTES


@app.route('/Grafica', methods=['GET'])
def getGraficas():

    pass
# OBTENER UN DATO


if __name__ == '__main__':
    app.run(debug=True, port=5000)
