from Datos import datos
from datetime import *
from Errores import errores
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
class peticiones:
    def __init__(self):
        try:
            file = open('Serializacion/list_dtesXML.txt', 'r', encoding="utf8")        
            cadena_leida=file.read()
            file.close()
            newlist_temporal = json.loads(cadena_leida)#!convierte a lista
            list_dtes_news = []  # LISTA QUE SE DESERIALIZA
            for i in newlist_temporal:
                print(datos(**json.loads(json.dumps(i))))
                list_dtes_news.append(datos(**json.loads(json.dumps(i))))
            if list_dtes_news!=[]:
                self.list_dtes= list_dtes_news
            else :
                self.list_dtes= []
        except:
            self.list_dtes= []
        self.error_obj=""
        # self.total_fac_bue=0
        # self.total_fac_mal=0
        self.fechas_list=[]
        self.cont_dtes=1

    def reiniciar_todo(self):
        self.list_dtes=[]
        self.error_obj=""
        #!reset el XML de ENTRADA/SALIDA
        archivo1 = open('XML_generados/archivo_Salida_.xml', 'w', encoding="utf8")        
        archivo1.write("")
        archivo1.close()
        archivo2 = open('XML_generados/archivo_Entrada_.xml', 'w', encoding="utf8")        
        archivo2.write("")
        archivo2.close()
        serial_list=open('Serializacion/list_dtesXML.txt', 'w', encoding="utf8")
        # cadena_lista=json.dumps(self.list_dtes)#!convierte a string
        # print("cadena: ", cadena_lista, type(cadena_lista))
        # print("lista: ", lista_convertida, type(lista_convertida))
        serial_list.write(self.list_dtes)
        serial_list.close()

    def agregar_peticion(self, Datos):
        self.list_dtes.append(Datos)
        serial_list=open('Serializacion/list_dtesXML.txt', 'w', encoding="utf8")

        # json_string = json.dumps([ob.__dict__ for ob in self.list_dtes])
        json_data = json.dumps([us.__dict__ for us in self.list_dtes])
        # print(json_data)
        # print(type(json_data))

        # print(json_data)
        # cadena_lista=json.dumps(self.list_dtes)#!convierte a string
        # print("cadena: ", cadena_lista, type(cadena_lista))
        # print("lista: ", lista_convertida, type(lista_convertida))
        serial_list.write(json_data)
        serial_list.close()
        # lista_convertida=json.loads(cadena_lista)#!convierte a lista



        cant_dtes=open('Serializacion/cant_dtes.txt', 'w', encoding="utf8")
        cant_dtes.write(str(self.cont_dtes))
        cant_dtes.close()
        self.cont_dtes+=1

    def verificar_peticion_referencia(self, referencia):
        for i in self.list_dtes:
            if referencia == i.referencia and i.valido==True:
                return False
        return True
            
    # def total_fac_buenasymalas(self, buenas,malas):
    #     self.total_fac_bue=buenas
    #     self.total_fac_mal=malas
    #!CASI TODO EL PROCESO PARA LA SALIDA DEL XML GENERADO QUE SE ACTUALIZA
    def proceso_datos_salida(self):
        lista_datos = []

        for dte in self.list_dtes:
            if not dte.date in lista_datos :
                lista_datos.append(dte.date)

        list_return = []

        for date in lista_datos:

            element = {}
            
            list_return.append(element)
            # .strftime('%d/%m/%Y')
            element['date'] = date
            
            events_by_date = self.get_fact_by_fecha(date)
            element['cant_facturas'] = len(events_by_date)
            facturas_NoValid = self.get_fact_by_fechaNOVALID(date)
            
            referencia_duplicada, nit_emisor_invalid, nit_receptor_invalid, iva_error, total_error=self.get_errors_facturas(date)
            element['nitcorrect1'] = nit_emisor_invalid
            element['nitcorrect2'] = nit_receptor_invalid
            element['iva'] = iva_error
            element['total'] = total_error
            element['referencia'] = referencia_duplicada

            facturas_Valid = self.get_fact_by_fechaVALID(date)
            element['cant_corrects_fac'] = len(facturas_Valid)
            list_emisors=[]
            for dte in self.list_dtes:
                if dte.nit_emisor not in list_emisors and dte.valido==True:
                        list_emisors.append(dte)
            element['cant_emisors'] = len(list_emisors)

            list_receptors=[]
            for dte in self.list_dtes:
                if not dte.nit_receptor in list_receptors:
                    if dte.valido==True:
                        list_receptors.append(dte)
            element['cant_receptors'] = len(list_receptors)

            
            element['autorizaciones'] = []
            for user in facturas_Valid:
                if user.valido==True:
                    print(user.valido)
                    print(user.date)
                    element['autorizaciones'].append({
                        'nit_emisor': user.nit_emisor,
                        'codigo_aprobacion': user.Codigo_completo,
                        'referencia': user.referencia
                    })

            element['total_aprobacion']=len(element['autorizaciones'])

        return list_return

    def get_fact_by_fecha(self, date):
        events = []
        for event in self.list_dtes:
            if event.date == date:
                events.append(event)
        return events

    def get_fact_by_fechaVALID(self, date):
        events = []
        for event in self.list_dtes:
            if event.date == date and event.valido==True:
                events.append(event)
        return events
    
    def get_fact_by_fechaNOVALID(self, date):
        events = []
        for event in self.list_dtes:
            if event.date == date and event.valido==False:
                events.append(event)
        return events
    
    def get_errors_facturas(self, date):        
        referencia_duplicada=0
        nit_emisor_invalid =0
        nit_receptor_invalid=0
        iva_error =0
        total_error=0
        for event in self.list_dtes:
            if event.date == date and event.valido==False:
                if event.referencia_duplicada==1:
                    referencia_duplicada+=1
                if event.nit_emisor_invalid==1:
                    nit_emisor_invalid+=1
                if event.nit_receptor_invalid==1:
                    nit_receptor_invalid+=1
                if event.iva_error==1:
                    iva_error+=1
                if event.total_error==1:
                    total_error+=1                
        return referencia_duplicada, nit_emisor_invalid, nit_receptor_invalid, iva_error, total_error
            
    #! PROCESO DEL RESUMEN DE IVA CON UNA FECHA
    def get_Resumen_Iva(self, date):
        if date!=None:
            fechas_list=self.get_fact_by_fechaVALID(date)
            list_nits=[]
            list_iva_emitido=[]
            list_iva_recibido=[]
            ruta_graph=""
            iva_emitido={}
            iva_recibido={}
            #! PRIMERO SE LLENA UN LISTA CON TODOS LOS NITS EN UNITARIO
            for w in fechas_list:
                nit_emite=w.nit_emisor  
                nit_recibe=w.nit_receptor              
                if nit_emite not in list_nits :
                    list_nits.append(nit_emite)
                    iva_emitido[nit_emite]=0
                    iva_recibido[nit_emite]=0
                if nit_recibe not in list_nits :
                    list_nits.append(nit_recibe)
                    iva_recibido[nit_recibe]=0
                    iva_emitido[nit_recibe]=0
            print(iva_emitido.keys())
            print(iva_emitido.values())
            print(iva_recibido.keys())
            print(iva_recibido.values())
            print("Lista: ", list_nits)
            #! luego se recorren todos los nits
            for cnit in list_nits:
                print("Recorriendo Nit: ", cnit)
                #! por cada nit 
                for nemi in fechas_list:
                    #!si el nit emisor == al nit se guarda un dic con iva
                    print(" ", nemi.nit_emisor,"==", cnit)
                    if nemi.nit_emisor == cnit:
                        temp=iva_emitido[cnit]
                        iva_emitido[cnit]=round(float(nemi.iva)+temp,2)
                    #!si el nit receptor == al nit se guarda un dic con iva
                    print(" ", nemi.nit_receptor,"==", cnit)
                    if nemi.nit_receptor == cnit:
                        temp2=iva_recibido[cnit]
                        iva_recibido[cnit]=round(float(nemi.iva)+temp2,2)
                        

                # nit_emite=w.nit_emisor  
                # nit_recibe=w.nit_receptor              
                # if nit_emite not in list_nits :
                #     list_nits.append(nit_emite)
                #     # iva_emitido[nit_emite]=float(w.iva)
                #     iva_emitido[nit_emite]=0
                # else:
                #     for x in fechas_list:
                #         if nit_emite==x.nit_emisor:
                #             temp=iva_emitido[nit_emite]
                #             iva_emitido[nit_emite]=round(float(x.iva)+temp,2)
                        


                # if nit_recibe not in list_nits:
                #     list_nits.append(nit_recibe)
                #     # iva_recibido[nit_recibe]=float(w.iva)
                #     iva_recibido[nit_recibe]=0
                # else:
                #     for x in fechas_list:
                #         if nit_recibe == x.nit_receptor:
                #             temp=iva_recibido[nit_recibe]
                #             iva_recibido[nit_recibe]=round(float(x.iva)+temp,2)

                #         if nit_recibe == x.nit_emisor:
                #             temp=iva_emitido[nit_recibe]
                #             iva_emitido[nit_recibe]=round(float(x.iva)+temp,2)

            for ivasriciv in iva_emitido.values():
                list_iva_emitido.append(ivasriciv)


            # for z in fechas_list:    
            #     if z.nit_receptor not in list_nits2:
            #         list_nits2.append(z.nit_receptor)
            #         iva_recibido[z.nit_receptor]=float(z.iva)
            #     else:
            #         for x in list_nits2:
            #             if z.nit_receptor==x.nit_receptor:
            #                 temp=iva_recibido[z.nit_receptor]
            #                 iva_recibido[z.nit_receptor]=round(float(z.iva)+float(temp),2)

            for ivasemitid in iva_recibido.values():
                list_iva_recibido.append(ivasemitid)

            print(list_nits," Longitud: ", len(list_nits))
            print(list_iva_emitido," Longitud: ",len(list_iva_emitido))
            print(list_iva_recibido," Longitud: ",len(list_iva_recibido))
            if len(list_nits)==len(list_iva_emitido)==len(list_iva_recibido):
                ruta_graph=self.get_Graphic_nit_Ivas(list_nits,list_iva_emitido,list_iva_recibido,str(date))
            print("RUTA DE LA GRÁFICA: ",ruta_graph)
            return ruta_graph

    def get_Graphic_nit_Ivas(self, list_nits,list_iva_emitido,list_iva_recibido,date):
        
        # Nits = ['NIT 1', 'NIT 2', 'NINT 3', 'NIT 4', 'NIT 5']
        # iva_emitido = [20, 34, 30, 35, 27]
        # iva_recibido = [25, 32, 34, 20, 25]
        #Obtenemos la posicion de cada etiqueta en el eje de X
        x = np.arange(len(list_nits))
        #tamaño de cada barra
        width = 0.35
        fig, ax = plt.subplots()
        #Generamos las barras para el conjunto de hombres
        rects1 = ax.bar(x - width/2, list_iva_emitido, width, label='Iva Emitido')
        #Generamos las barras para el conjunto de mujeres
        rects2 = ax.bar(x + width/2, list_iva_recibido, width, label='Iva Recibido')
        #Añadimos las etiquetas de identificacion de valores en el grafico
        date=date.replace("/", "_")
        ax.set_ylabel('Nits')
        ax.set_title(f'Resumen de IVA por fecha y NIT del {date}:')
        ax.set_xticks(x)
        ax.set_xticklabels(list_nits)
        #Añadimos un legen() esto permite mmostrar con colores a que pertence cada valor.
        ax.legend()
        def autolabel(rects):
            """Funcion para agregar una etiqueta con el valor en cada barra"""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        #Añadimos las etiquetas para cada barra
        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        rutagraph=f'Frontend/static/images/grafico_Resumen_Iva_Nit{date}.jpg'
        ruth=f'grafico_Resumen_Iva_Nit{date}.jpg'
        plt.savefig(rutagraph)
        return ruth

    def get_Resumen_Iva_Recibido(self, date):
        if date!=None:
            fechas_list=self.get_fact_by_fechaVALID(date)
            # list_emisors=[]
            list_receptors=[]
            # iva_emitido={}       
            iva_recibido={}       

            for w in fechas_list:
                # if w.nit_emisor not in list_emisors:
                #     list_emisors.append(w)
                #     iva_emitido[w.nit_emisor]=float(w.iva)
                # else:
                #     for x in list_emisors:
                #         if w.nit_emisor==x.nit_emisor:
                #             temp=iva_emitido[w.nit_emisor]
                #             iva_emitido[w.nit_emisor]=round(float(w.iva)+temp,2)
                
                if w.nit_receptor not in list_receptors:
                    list_receptors.append(w)
                    iva_recibido[w.nit_receptor]=float(w.iva)
                else:
                    for x in list_receptors:
                        if w.nit_receptor==x.nit_receptor:
                            temp=iva_recibido[w.nit_receptor]
                            iva_recibido[w.nit_receptor]=round(float(w.iva)+temp,2)
            
            return iva_recibido#, iva_recibido

    def get_Resumen_Iva_Fechas(self):
        if self.fechas_list==[]:
            for i in self.list_dtes:
                if i.date not in self.fechas_list and i.valido==True:
                    self.fechas_list.append(i.date)
            print(self.fechas_list)
            serial_list=open('Serializacion/list_fechas.txt', 'w', encoding="utf8")
            cadena_lista=json.dumps(self.fechas_list)#!convierte a string
            serial_list.write(cadena_lista)
            serial_list.close()
            return self.fechas_list
        else:
            return self.fechas_list

    #! PROCESO DEL RESUMEN DE IVA CON UN RANGO DE FECHAS
    def get_valor_total(self,date):
        total=0
        for w in self.list_dtes:
            if w.date == date and w.valido==True:
                total+=float(w.total)
        return total
    def get_valor_sinIva(self,date):
        total=0
        for w in self.list_dtes:
            if w.date == date and w.valido==True:
                total+=float(w.valor)
        return total
    
    def get_list_dates(self, dateini, datefin):
        # inicio = '01/10/2017'
        # fin = '06/10/2017'
        inicio = datetime.strptime(str(dateini), '%d/%m/%Y')
        fin = datetime.strptime(str(datefin), '%d/%m/%Y')
        print(" -----> ",inicio, " -----> ", fin)
        lista_fechas = [(inicio + timedelta(days=d)).strftime('%d/%m/%Y')for d in range((fin - inicio).days + 1)] 
        # print(lista_fechas)
        return lista_fechas

    
    def gen_graph_range(self, lista_fechas, list_values, dateini, datefin, param):
        date=dateini+"_to_"+datefin
        # Nits = ['NIT 1', 'NIT 2', 'NINT 3', 'NIT 4', 'NIT 5']
        # iva_emitido = [20, 34, 30, 35, 27]
        # iva_recibido = [25, 32, 34, 20, 25]
        #Obtenemos la posicion de cada etiqueta en el eje de X
        x = np.arange(len(lista_fechas))
        #tamaño de cada barra
        width = 0.35
        fig, ax = plt.subplots()
        #Generamos las barras para el conjunto de hombres
        rects1 = ax.bar(x - width/2, list_values, width, label='Iva Emitido')
        #Generamos las barras para el conjunto de mujeres
        # rects2 = ax.bar(x + width/2, list_iva_recibido, width, label='Iva Recibido')
        #Añadimos las etiquetas de identificacion de valores en el grafico
        date=date.replace("/", "")
        ax.set_ylabel('Nits')
        ax.set_title(f'Resumen por Rango de fechas de VALORES {param} {dateini}-{datefin}:')
        ax.set_xticks(x)
        ax.set_xticklabels(lista_fechas)
        #Añadimos un legen() esto permite mmostrar con colores a que pertence cada valor.
        ax.legend()
        def autolabel(rects):
            """Funcion para agregar una etiqueta con el valor en cada barra"""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        #Añadimos las etiquetas para cada barra
        autolabel(rects1)
        # autolabel(rects2)
        fig.tight_layout()
        param=param.strip()
        rutagraph=f'Frontend/static/images/graph_ResumenRango{param}_{date}.jpg'
        ruth=f'graph_ResumenRango{param}_{date}.jpg'
        plt.savefig(rutagraph)
        return ruth


    def get_Resumen_Rango(self, dateini, datefin, param):
        if dateini!= None and datefin!= None and param != None:
            # .strftime('%d/%m/%Y')
            listdates=self.get_list_dates(dateini, datefin)
            #* Hasta el momento tengo todas las fechas que se encuentran en el intervalo
            #* dado, ahora procedo a validar que esas fechas se encuentren en la lista
            #* de DTES que son válidos
            lista_fechas = []
            list_total=[]
            list_sinIva=[]
            list_fechas_enviar=[]
            path=""

            for dte in self.list_dtes:
                if  dte.date not in lista_fechas and dte.valido==True :
                    lista_fechas.append(dte.date)
            #?---------------------------------------------------------------
            if param == "total": 
                print("VALORES TOTALES")
                for x in listdates:
                    if  x in lista_fechas:
                        print("*****************************")
                        print("Fecha: ", x)
                        list_fechas_enviar.append(x)
                        list_total.append(self.get_valor_total(x))
                print(list_fechas_enviar," Longitud: ", len(list_fechas_enviar))
                print(list_total," Longitud: ",len(list_total))
                # print(list_iva_recibido," Longitud: ",len(list_iva_recibido))
                if len(list_fechas_enviar)==len(list_total):
                    path=self.gen_graph_range(list_fechas_enviar, list_total, dateini, datefin, "TOTALES")                         
                return path       
            #?---------------------------------------------------------------
            elif param == "siniva":
                print("VALORES SIN IVA")
                for x in listdates:
                    if  x in lista_fechas:
                        print("*****************************")
                        print("Fecha: ", x)
                        list_fechas_enviar.append(x)
                        list_sinIva.append(self.get_valor_sinIva(x))
                print(list_fechas_enviar," Longitud: ", len(list_fechas_enviar))
                print(list_sinIva," Longitud: ",len(list_sinIva))
                # print(list_iva_recibido," Longitud: ",len(list_iva_recibido))
                if len(list_fechas_enviar)==len(list_sinIva):
                    path=self.gen_graph_range(list_fechas_enviar, list_sinIva, dateini, datefin, "SIN IVA")   
                return path         
            #?---------------------------------------------------------------
            else:
                return ""
        else:
            return 

    
    

