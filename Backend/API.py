from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#!██████████████████   CONSULTAR DATOS    █████████████████████
#?OBTENER LOS PACIENTES
@app.route('/ConsultaDatos', methods=['GET'])
def getDatos():    
    # global Pacientes  
    # Datos=[]
    # for paciente in Pacientes:
    #     objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra()
    #     }
        # Datos.append(objeto)
    # return(jsonify(Datos))
    pass
#OBTENER UN DATO   
@app.route('/ConsultaDatos/<string:username>', methods=['GET'])
def ObtenerDato(username): 
    # global Pacientes  
    # for paciente in Pacientes:
    #     if paciente.getUsername() == username :
    #         objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra(),
    #         'tipo':0
    #         }
    #         return(jsonify(objeto))     
    # salida = { "Mensaje": "No existe el usuario con ese nombre"}

    # return(jsonify(salida))
    pass

#!██████████████████   RESUMEN IVA   █████████████████████
#?OBTENER LOS PACIENTES
@app.route('/ResumenIva', methods=['GET'])
def getIvas():    
    # global Pacientes  
    # Datos=[]
    # for paciente in Pacientes:
    #     objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra()
    #     }
        # Datos.append(objeto)
    # return(jsonify(Datos))
    pass
#OBTENER UN DATO   
@app.route('/ResumenIva/<string:username>', methods=['GET'])
def ObtenerIva(username): 
    # global Pacientes  
    # for paciente in Pacientes:
    #     if paciente.getUsername() == username :
    #         objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra(),
    #         'tipo':0
    #         }
    #         return(jsonify(objeto))     
    # salida = { "Mensaje": "No existe el usuario con ese nombre"}

    # return(jsonify(salida))
    pass


#!██████████████████   RESUMEN RANGO    █████████████████████
#?OBTENER LOS PACIENTES
@app.route('/ResumenRango', methods=['GET'])
def getResumenes():    
    # global Pacientes  
    # Datos=[]
    # for paciente in Pacientes:
    #     objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra()
    #     }
        # Datos.append(objeto)
    # return(jsonify(Datos))
    pass
#OBTENER UN DATO   
@app.route('/ResumenRango/<string:username>', methods=['GET'])
def ObtenerResumen(username): 
    # global Pacientes  
    # for paciente in Pacientes:
    #     if paciente.getUsername() == username :
    #         objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra(),
    #         'tipo':0
    #         }
    #         return(jsonify(objeto))     
    # salida = { "Mensaje": "No existe el usuario con ese nombre"}

    # return(jsonify(salida))
    pass

#!██████████████████   GRAFICA    █████████████████████
#?OBTENER LOS PACIENTES
@app.route('/Grafica', methods=['GET'])
def getGraficas():    
    # global Pacientes  
    # Datos=[]
    # for paciente in Pacientes:
    #     objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra()
    #     }
        # Datos.append(objeto)
    # return(jsonify(Datos))
    pass
#OBTENER UN DATO   
@app.route('/Grafica/<string:username>', methods=['GET'])
def ObtenerGrafica(username): 
    # global Pacientes  
    # for paciente in Pacientes:
    #     if paciente.getUsername() == username :
    #         objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra(),
    #         'tipo':0
    #         }
    #         return(jsonify(objeto))     
    # salida = { "Mensaje": "No existe el usuario con ese nombre"}

    # return(jsonify(salida))
    pass

#TODO██████████████████   PROCESO    █████████████████████
#?POSTEAR EL PROCESO
@app.route('/Procesar', methods=['POST'])
def AgregarPaciente():
    # global Pacientes
    # nombre = request.json['Nombre']
    # nombre=nombre.replace(" ","")
    # apellido= request.json['Apellido']
    # nacimiento = request.json['Fecha']
    # sexo = request.json['Sexo']
    # username = request.json['Usuario']
    # contra = request.json['Contraseña']

    # nuevo = Paciente(nombre,apellido,nacimiento,sexo,username,contra)
    # Pacientes.append(nuevo)
    # return jsonify({'Mensaje':'Se agrego el Paciente exitosamente',})
    pass

if __name__=='__main__':
    app.run(debug=True, port=5000)