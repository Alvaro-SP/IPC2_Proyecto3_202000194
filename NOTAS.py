"""Se recibe mensaje para autorizar un DTE
Se emite un numero unico de autorización (inicia en 1) cada dia no repetido
NUMERO DE AUTORIZACIÓN:  yyyymmdd########, 
año  mes  dia  correlativo <-- en que se solicita la autorización

MENSAJE DEL PROVEEDOR
LUGAR Y FECHA: Guatemala, dd/mm/yyyy hh24:mi
REFERENCIA: A3038
NIT EMISOR: XXXXXXV
NIT RECEPTOR: YYYYYYYV 
VALOR: ########.##
IVA: #######.##
TOTAL: #######.## 

FECHA: Fecha en formato dd/mm/yyyy hh24:mi (horas en formato 24 horas – 0 a 23 
horas)
● REFERENCIA: Código interno enviado por el emisor. Es un texto único de máximo 
40 posiciones.
● NIT EMISOR: XXXXXXV cada X corresponde a un valor entre 0 ... 9. V debe ser la 
validación del NIT ingresado. La cantidad de valores X podrá ser desde 1 hasta 20.
● NIT RECEPTOR: YYYYYYV cada Y corresponde a un valor entre 0 ... 9. V debe ser 
la validación del NIT ingresado. La cantidad de valores Y podrá ser desde 1 hasta 
20.
● VALOR: Valor real positivo de 2 posiciones decimales.
● IVA: Es el resultado de la operación REDONDEAR(VALOR * 0.12, 2).
● TOTAL: Es el resultado de la operación VALOR + IVA

VALIDACIÓN DEL NIT 
1. Multiplique cada carácter por su posición respectiva (siendo la posición 1 el carácter más 
a la derecha), excepto el primero. 
2. Sume todos los resultados. 
3. Obtenga el módulo 11 de la sumatoria. 
4. A 11 réstale el resultado obtenido en el punto 3. 
5. Calcule el módulo 11 del resultado obtenido en el punto No. 4, si este resultado es 10, 
entonces el dígito verificador del NIT deberá ser K.

ARCHIVO DE SALIDA
FECHA: dd/mm/yyyy 
Cantidad total de facturas recibidas: Cantidad total de facturas enviadas al servicio 
Listado de errores en facturas recibidas 
 NIT emisor inválido: cantidad errores 
 NIT receptor inválido: cantidad errores 
 IVA mal calculado: cantidad de errores
 TOTAL mal calculado: cantidad de errores
 REFERENCIA duplicada: cantidad de errores
Cantidad de facturas sin errores: Cantidad total de facturas enviadas sin errores al 
servicio.
Cantidad de emisores de facturas: Cantidad de distintos NIT’s emisores de facturas
Cantidad de receptores de facturas: Cantidad de distintos NIT’s receptores de facturas
… 
FECHA: dd/mm/yyyy 
… 


ARCHIVO DE ENTRADA
<SOLICITUD_AUTORIZACION> 
 <DTE> 
 <TIEMPO> Guatemala, 15/01/2021 15:25 hrs. </TIEMPO>
<REFERENCIA> A1990 </REFERENCIA> 
 <NIT_EMISOR> 7378106 </NIT_EMISOR>
 <NIT_RECEPTOR> 8338817 <NIT_RECEPTOR>
 <VALOR> 100.00 </VALOR>
 <IVA> 12.00 </IVA>
 <TOTAL> 112.00 </TOTAL>
 </DTE> 
 … 
</SOLICITUD_AUTORIZACION >

ARCHIVO DE SALIDA ( autorizaciones.xml )
<LISTAAUTORIZACIONES> 
 <AUTORIZACION>
 <FECHA> 01/09/2021 </FECHA>
 <FACTURAS_RECIBIDAS> 100 </FACTURAS_RECIBIDAS>
 <ERRORES>
 <NIT_EMISOR> 1 </NIT_EMISOR>
 <NIT_RECEPTOR> 2 </NIT_RECEPTOR>
 <IVA> 3 </IVA>
 <TOTAL> 2 </TOTAL>
 <REFERENCIA_DUPLICADA> 3 </REFERENCIA_DUPLICADA>
 </ERRORES>
 <FACTURAS_CORRECTAS> 89 </FACTURAS_CORRECTAS>
 <CANTIDAD_EMISORES> 10 </CANTIDAD_EMISORES> 
 <CANTIDAD_RECEPTORES> 881 </CANTIDAD_RECEPTORES> 
 <LISTADO_AUTORIZACIONES>
 <APROBACION>2
 <NIT_EMISOR ref=”A1990”> 7378106 </NIT_EMISOR>
 <CODIGO_APROBACION> 2021090100000001 </CODIGO_APROBACION>
 </APROBACION>
 …
 <TOTAL_APROBACIONES> 89 </TOTAL_APROBACIONES>3
 </LISTADO_AUTORIZACIONES>
 </AUTORIZACION>
 … 
</LISTAAUTORIZACIONES>
"""