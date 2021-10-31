# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import json
print("Hello world")
lista=[] #"1","2","3","4","5","6","7","8","9"
cadena_lista=json.dumps(lista)#!convierte a string
print("cadena: ", cadena_lista, type(cadena_lista))


archivo1 = open('Serializacion/testfile.txt', 'w', encoding="utf8")        
archivo1.write(cadena_lista)
archivo1.close()


file = open('Serializacion/testfile.txt', 'r', encoding="utf8")        
cadena_leida=file.read()
lista_convertida=json.loads(cadena_leida)#!convierte a lista
print("lista: ", lista_convertida, type(lista_convertida))
file.close()


filetest = open('Serializacion/list_dtesXML.txt', 'r', encoding="utf8")        
cadena_leida=filetest.read()
lista_convertida=json.loads(cadena_leida)#!convierte a lista
print("lista: ", lista_convertida, type(lista_convertida))
filetest.close()