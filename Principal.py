from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL

__author__ = "Lulo"

app = Flask(__name__)


#Conexion MYSQL
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="User"
app.config["MYSQL_PASSWORD"]="0110Lulo"
app.config["MYSQL_DB"]="consultorio"
mysql = MySQL(app)

#Inicializar sesion
app.secret_key = "Consultorio"

#variables importantes
def cursor():
    cur = mysql.connection.cursor()
    return cur

@app.route("/")
def index():
    cur = cursor()
    cur.execute("Select * From pacientes")
    data = cur.fetchall()
    return render_template("Index.html", pacientes = data)

@app.route("/Agregar_paciente", methods = ["POST"])
def Add_paciente():
    if request.method == "POST":
        Dni = request.form["Dni"]
        Nombre = request.form["Nombre"]
        Telefono = request.form["Telefono"]
        Proximo_turno = request.form["Proximo_turno"]
        Observaciones = request.form["Observaciones"]

        cur = cursor()
        cur.execute("INSERT INTO pacientes (Dni,Nombre,Telefono,Proximo_Turno,Observaciones) VALUES(%s,%s,%s,%s,%s)",(Dni,Nombre,Telefono,Proximo_turno,Observaciones))
        mysql.connection.commit()
        flash("Paciente agregado")
        return redirect(url_for("index"))

@app.route("/Busqueda_Dni", methods = ["POST"])
def Busqueda_Dni():#no funca
    if request.method == "POST":
        dni = request.form["Dni"]
        cur= cursor()
        cur.execute("SELECT * FROM pacientes WHERE Dni = %s",(request.form["Dni"]).format(id))
        data_busqueda = cur.fetchall()
        return render_template("Index.html",pacientes = data_busqueda)

@app.route("/Busqueda_Nombre", methods = ["POST"])
def Busqueda_nombre():#no funca
    if request.method == "POST":
        cur= cursor()
        cur.execute("SELECT * FROM pacientes WHERE Nombre LIKE %",request.form["Nombre"],"%")
        data_busqueda = cur.fetchall()
        return render_template("Index.html",pacientes = data_busqueda)

@app.route("/delete/<string:id>")
def Delete_paciente(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pacientes WHERE Dni = {0}".format(id))
    mysql.connection.commit()
    flash("paciente eliminado satisfactoriamente")
    return redirect(url_for("index"))

@app.route("/update/<id>", methods = ["POST"] )
def update(id):
    if request.method == "POST":
        Dni = request.form["Dni"]
        Nombre = request.form["Nombre"]
        telefono = request.form["telefono"]
        turno = request.form["Turno"]
        Observaciones = request.form["Observaciones"]
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE pacientes SET Dni = %s,
                            Nombre= %s,
                            telefono = %s,
                            Proximo_turno = %s,
                            Observaciones = %s
        WHERE Dni = %s                 
        """,(Dni,Nombre,telefono,turno,Observaciones,id))
        mysql.connection.commit()
        flash("paciente a sido actualizado")
        return redirect(url_for("index"))

@app.route("/edit/<id>")
def obtener_paciente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes WHERE Dni = {0}".format(id))
    data = cur.fetchall()
    return render_template("edit_paciente.html", paciente = data[0])

@app.route("/Ver/<id>")
def Ver_paciente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes WHERE Dni = {0}".format(id))
    data = cur.fetchall()

    cur = cursor()
    cur.execute("CREATE TABLE "+data[0][1]+" (Dni int, Fecha date, Trabajo varchar(255),DEBE int, HABER int, Saldo int,ID int AUTO_INCREMENT PRIMARY KEY)")
    mysql.connection.commit()
    flash("Tabla del paciente creada con exito")
    return redirect(url_for("index"))

@app.route("/Ver_tabla/<id>")
def Tabla_paciente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes WHERE Dni = {0}".format(id))
    data_paciente = cur.fetchall()

    cur = cursor()
    cur.execute("Select * From "+data_paciente[0][1])
    data = cur.fetchall()
    return render_template("tabla_paciente.html", datos = data,paciente = data_paciente[0])

@app.route("/Agregar_datos", methods = ["POST"])
def Add_datos():
    if request.method == "POST":

        Fecha = request.form["Fecha"]
        Trabajo = request.form["Trabajo"]
        Debe = request.form["Debe"]
        Haber = request.form["Haber"]
        Saldo = request.form["Saldo"]
        Dni = request.form["Dni"]
        Nombre = request.form["Nombre"]
        Nombre = Nombre.lower()
        redireccion= "/Ver_tabla/"+Dni
        print(redireccion)

        cur = cursor()
        cur.execute("INSERT INTO "+Nombre+" (Dni,Fecha,Trabajo,DEBE,HABER,Saldo) VALUES(0,%s,%s,%s,%s,%s)",(Fecha,Trabajo,Debe,Haber,Saldo))
        mysql.connection.commit()
        flash("Datos agregados")
        return redirect(redireccion)









if __name__ == "__main__":
    app.run(port=3000,debug=True)
