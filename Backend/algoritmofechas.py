# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Hello world")
import re
cad="364165 gfdsfg 10-12-2021 pjspiof"
cad2=re.search(r'(?:3[01]|[12][0-9]|0?[1-9])([\-\/\.])(0?[1-9]|1[0-2])\1\d{4}', cad).group().strip()
print(cad2)

print("Hello world")

cad="364165 gfdsfg 10/12/2021 pjspiof"
cad2=re.search(r'(?:3[01]|[12][0-9]|0?[1-9])([\/])(0?[1-9]|1[0-2])\1\d{4}', cad).group().strip()
print(cad2)