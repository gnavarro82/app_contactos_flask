from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#inicializar una sesion, dentro de la memoria de la app
app.secret_key = 'mysecretkey'


#Conexion con Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'navarro'
app.config['MYSQL_DB'] = 'proyectos_flask'
mysql = MySQL(app)# 


#Rutas de la aplicacion
@app.route('/')
def Index():
	#realizar consulta a bbdd para mostrar los datos
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM contactos')
	data = cur.fetchall()
	#retornar o renderizar la plantilla, se le pasa por parametro los ddatos de l bbdd
	return render_template('index.html', contactos=data)

@app.route('/agregar_contacto', methods=['POST']) 
def agregar_contacto():
	#GUARDARA DATOS- REALIZA UNA COMPROBACION
	#si estas enviando datos a esta ruta atravez del metodo post
	if request.method =='POST':
		nombre = request.form['nombre'] #obtiene los datos del index.html
		telefono = request.form['telefono'] #obtiene los datos del index.html
		mail = request.form['mail'] #obtiene los datos del index.html
		#pasamos datos a mysql
		#utilizamos un cursor para saber donde esta la conexion
		cur = mysql.connection.cursor() # me permite ejecutar los querys de mysql
		cur.execute('INSERT INTO contactos(nombre, telefono, mail) VALUES(%s,%s,%s)',(nombre, telefono, mail))
		#espera como segundo parametro los valores en una tupla
		mysql.connection.commit() #con esto se ejecuta el query
		#enviamos mensajes entre vistas con flush()
		flash('Contacto agregado satisfactoriamente') #para verlo hay que hacer unna comprobacion en la vista
		#ahora redireccionar al index nuevamente con la funcion url_form
		return redirect(url_for('Index')) #recibe el nombre de la funcion que ejecuta la ruta princiapl

@app.route('/editar/<id>') #otra forma de recibir un parametro, sin decirle el tipo de dato que es
def editar_contacto(id):
	#se pasara a una consulta
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM contactos WHERE id = %s', (id))
	data = cur.fetchall()
	# atraves de la variable contacto, la vista editar-contacto tendra los datos 
	return render_template('editar-contacto.html', contacto=data[0])#solo la lista 0

@app.route('/actualizar/<id>', methods=['POST'])	
def actualizar_contacto(id):
	if request.method == 'POST':
		nombre = request.form['nombre'] 
		telefono = request.form['telefono'] 
		mail = request.form['mail'] 
		#se pasara a una consulta
		cur = mysql.connection.cursor()
		cur.execute('UPDATE contactos SET nombre = %s, telefono = %s, mail = %s WHERE id = %s', (nombre, telefono, mail, id))
		mysql.connection.commit()
		#se pasa la tupla con los datos
		flash('Contacto actualizado satisfactoriamente')
		return redirect(url_for('Index'))







@app.route('/eliminar/<string:id>')#recibira un parametro que es el id
#cada vez que recibas un parametro de tipo id debe tener al lado un numero y poder eliminarlo
def eliminar_contacto(id):
	#se pasara a una consulta para eliminarlo
	cur = mysql.connection.cursor()
	#se pasan los datos por interpolacion - en la posicion 0 ira el id formateado a u string
	cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id) )
	mysql.connection.commit()
	flash('Contacto eliminado satisfactoriamente') 
	return redirect(url_for('Index'))

#Iniciar la aplicacion con debug en true
#comprobar que el archivo que se ejecuta sea el princial
if __name__ == '__main__':
	app.run(port = 3030, debug = True)