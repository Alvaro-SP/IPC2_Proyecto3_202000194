from Datos import datos
from datetime import date as Date
from Errores import errores

class peticiones:
    def __init__(self):
        self.list_dtes= []
        self.error_obj=""
        self.total_fac_bue=0
        self.total_fac_mal=0

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

    def agregar_peticion(self, Datos):
        self.list_dtes.append(Datos)

    def total_fac_buenasymalas(self, buenas,malas):
        self.total_fac_bue=buenas
        self.total_fac_mal=malas
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
            
    def get_Resumen_Iva_Emitido(self, date):
        if date!=None:
            fechas_list=self.get_fact_by_fechaVALID(date)
            list_emisors=[]
            # list_receptors=[]
            iva_emitido={}       
            # iva_recibido={}       

            for w in fechas_list:
                if w.nit_emisor not in list_emisors:
                    list_emisors.append(w)
                    iva_emitido[w.nit_emisor]=float(w.iva)
                else:
                    for x in list_emisors:
                        if w.nit_emisor==x.nit_emisor:
                            temp=iva_emitido[w.nit_emisor]
                            iva_emitido[w.nit_emisor]=round(float(w.iva)+temp,2)
                
                # if w.nit_receptor not in list_receptors:
                #     list_receptors.append(w)
                #     iva_recibido[w.nit_receptor]=float(w.iva)
                # else:
                #     for x in list_receptors:
                #         if w.nit_receptor==x.nit_receptor:
                #             temp=iva_recibido[w.nit_receptor]
                #             iva_recibido[w.nit_receptor]=round(float(w.iva)+temp,2)
            
            return iva_emitido#, iva_recibido

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
        fechas_list=[]
        for i in self.list_dtes:
            if i.date not in fechas_list and i.valido==True:
                fechas_list.append(i.date)
        print(fechas_list)
        return fechas_list
