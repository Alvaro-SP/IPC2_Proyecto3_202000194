# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from datetime import *

print("Hello world")

inicio = '01/10/2017'
fin = '06/10/2017'
inicio = datetime.strptime(inicio, '%d/%m/%Y')
fin = datetime.strptime(fin, '%d/%m/%Y')

print(" -----> ",inicio, " -----> ", fin)

lista_fechas = [(inicio + timedelta(days=d)).strftime('%d/%m/%Y')for d in range((fin - inicio).days + 1)] 

print(lista_fechas)