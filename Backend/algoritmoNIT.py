

cadena="2431739K"
CAD=cadena
valor=cadena[-1]
cadena=cadena[:-1]
acum=0
position=2
for c in cadena[::-1]:
    temp=position*int(c)
    position+=1
    acum+=temp
obtainmod=acum%11
result=11-obtainmod
print("EL (RESULTADO): ",result)
print("EL ULTIMO DIGITO: ",valor)
print("EL NIT: ",CAD)
if result==valor or (result==10 and valor=="K"):
    print("resultado CORRECTO") 
else:
    print("resultado incorrecto")