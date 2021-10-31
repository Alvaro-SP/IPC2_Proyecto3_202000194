# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.

# Esto es GENIAL GRACIAS PYTHON XDXD
import json
print("Hello world")

mylista = []


class datos(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


user = datos(first_name="Jake", last_name="Doyle")
user2 = datos(first_name="alvaro", last_name="socop")
user3 = datos(first_name="sergio", last_name="lemus")
mylista.append(user)
mylista.append(user2)
mylista.append(user3)

json_data = json.dumps([us.__dict__ for us in mylista])
# print(json_data)
# print(type(json_data))

newlist_temporal = json.loads(json_data)
# print(newlist_temporal)
# print(type(newlist_temporal))
list_dtes_news = []  # LISTA QUE SE DESERIALIZA
for i in newlist_temporal:
    print(datos(**json.loads(json.dumps(i))))
    list_dtes_news.append(datos(**json.loads(json.dumps(i))))

#! PROBANDO LA LISTA
for w in list_dtes_news:
    print(w.first_name, " --> ", w.last_name)

