
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

Nits = ['NIT 1', 'NIT 2', 'NINT 3', 'NIT 4', 'NIT 5']
iva_emitido = [20, 34, 30, 35, 27]
iva_recibido = [25, 32, 34, 20, 25]
#Obtenemos la posicion de cada etiqueta en el eje de X
x = np.arange(len(Nits))
#tamaño de cada barra
width = 0.35
fig, ax = plt.subplots()
#Generamos las barras para el conjunto de hombres
rects1 = ax.bar(x - width/2, iva_emitido, width, label='Iva Emitido')
#Generamos las barras para el conjunto de mujeres
rects2 = ax.bar(x + width/2, iva_recibido, width, label='Iva Recibido')
#Añadimos las etiquetas de identificacion de valores en el grafico
ax.set_ylabel('Nits')
ax.set_title('Resumen de IVA por fecha y NIT:')
ax.set_xticks(x)
ax.set_xticklabels(Nits)
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
plt.savefig('doble_barra.png')


# plt.bar(["40351017","35814691","12345","897541","894984"],[10,20,80,1,50],label="Iva Emitido",color='r',width=.5)
# plt.bar(["40351017","35814691","12345","897541","894984"],[80,90,1,20,50],label="Iva Recibido", color='g',width=.2)
# plt.legend()
# plt.xlabel('Nits')
# plt.ylabel('Monto (Q)')
# plt.title('Resumen de IVA por fecha y NIT: ')
# plt.savefig('grafico_Resumen_Iva_Nit.png')


# #Definimos una lista con paises como string
# diccionario={"24/12/2001":15,"25/12/2001":16,"26/12/2001":17,"27/12/2001":18,"28/12/2001":19}
# print(diccionario)
# a=diccionario.keys()

# paises = ['Estados Unidos', 'España', 'Mexico', 'Rusia', 'Japon']
# #Definimos una lista con ventas como entero
# ventas = [25, 32, 34, 20, 25]

# fig, ax = plt.subplots()
# #Colocamos una etiqueta en el eje Y
# ax.set_ylabel('Ventas')
# #Colocamos una etiqueta en el eje X
# ax.set_title('Cantidad de Ventas por Pais')
# #Creamos la grafica de barras utilizando 'paises' como eje X y 'ventas' como eje y.
# plt.bar(paises, ventas)
# plt.savefig('barras_simple.png')

# # Image.open('testplot.png').save('testplot.jpg','JPEG')
