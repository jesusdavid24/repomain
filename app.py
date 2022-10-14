from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen=""

@app.route("/")
def inicio():
    return render_template("login.html")

@app.route("/validarUsuario", methods=["GET", "POST"])
def validarUsuario():
    if request.method=="POST":
        usu=request.form["txtusuario"]
        usu=usu.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=request.form["txtpass"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
        
        respuesta=controlador.validar_usuario(usu, passw2)
        
        global email_origen
                
        if len(respuesta)==0:
            email_origen=""
            mensaje = "Error de autenticacion.!!! lo invitamos a verificar su usuario (correo y contrseña) "            
            return render_template("informacion.html",datas=mensaje)
           
        else:
            email_origen=usu
            respuesta2=controlador.lista_destinatario(usu)
            return render_template("principal.html", datas=respuesta2)
        
        # print("usuario= "+ usu)
        # print("password= "+ passw)
        # print("password Codificado= "+ passw2)

@app.route("/registrarUsuario", methods=["GET", "POST"])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email=request.form["txtusuario2registro"]
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=request.form["txtpassregistro"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
        
        #generar codigo activacion. 
        # replace nos sirve para eliminar los caracteres por string vacios
        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-", "")
        codigo2=codigo2.replace(" ", "")
        codigo2=codigo2.replace(":", "")
        codigo2=codigo2.replace(".", "")
        
        print(codigo2)
        
        mensaje="sr. "+nombre+" su codigo de activacion es: \n\n"+codigo2+ " \n\n Recuerdo copiarlo y pegarlo para validar su usuario "
        
        envioemail.enviar(email,mensaje, "Codigo de activacion")
        
        respuesta=controlador.registrar_usuario(nombre, email, passw2, codigo2)
        
        #mensaje = "El usuario "+nombre+", se ha registrado satisfactoriamente"           
        return render_template("informacion.html",datas=respuesta)
           
           
@app.route("/activarUsuario", methods=["GET", "POST"])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        respuesta=controlador.activar_usuario(codigo)
        
        if len(respuesta)==0:
            mensaje = "El codigo de activacion es errorneo, verifiquelo"
        else:
            mensaje = "El usuario se ha activado exitosamente"

        return render_template("informacion.html",datas=mensaje)
        
        
@app.route("/enviarMAIL", methods=["GET", "POST"])
def enviarMAIL():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]
        emailDestino=emailDestino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        asunto=request.form["asunto"]
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        mensaje=request.form["mensaje"]
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        controlador.registrar_mail(email_origen,emailDestino,asunto,mensaje)
        
        mensaje2="Señor usuario usted recibio un nuevo mensaje, por favor ingrese a la plataforma y revise el historial de mensajes \n\n Muchas gracias."
        envioemail.enviar(emailDestino,mensaje2,"Nuevo mensaje enviado")
        return "Email enviado exitosamente"
    
@app.route("/historialEnviados", methods=["GET", "POST"])
def historialEnviados():
    
    resultado=controlador.ver_enviados(email_origen)
    return render_template("respuesta.html",datas=resultado)

@app.route("/historialRecibidos", methods=["GET", "POST"])
def historialRecibidos():
    
    resultado=controlador.ver_recibidos(email_origen)
    return render_template("respuesta.html",datas=resultado)

@app.route("/actualizacionPassword", methods=["GET", "POST"])
def actualizacionPassword():
    if request.method=="POST":
        pass1=request.form["pass"]
        pass1=pass1.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        passw2=pass1.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
                
        controlador.actualiza_pass(passw2, email_origen)
        return "Actualizacion de password exitosa"
        
        