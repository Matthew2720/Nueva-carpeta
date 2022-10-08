from flask import Flask, render_template, url_for, request, redirect, flash, session
from config import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pyodbc

# Modelos y entidades

from models.entities.User import User, Veterinaria
from models.ModelUser import ModelUser, ModelVeterinaria
from models.ModelCliente import *
from models.entities.Cliente import *

app = Flask(__name__)
db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                    direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/regVet', methods=['GET', 'POST'])
def registroVet():
    if request.method == 'POST':
        veterinaria = Veterinaria(request.form['nombre_vet'], request.form['ciudad_vet'], request.form['nombre'],
                                  request.form['apellido'], request.form['documento'], request.form['telefono'], request.form['email'])
        ModelVeterinaria.registrar_vet(db, veterinaria)
        fullname = veterinaria.nombre + veterinaria.apellido
        UserAdmin = User(veterinaria.documento, veterinaria.nombre,
                         request.form['password'], fullname, '1', veterinaria.nombre_vet, veterinaria.ciudad_vet, veterinaria.email, veterinaria.telefono)
        ModelUser.register(db, UserAdmin)
        flash("Registro realizado")
        flash("Puedes loguearte como administrador")
        return render_template('reg/regVet.html')
    else:
        return render_template('reg/regVet.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        loggued_user = ModelUser.login(db, user)
        if loggued_user != None:
            centro = ModelVeterinaria.get_centro()
            print(centro)
            if loggued_user.veterinaria == centro:
                if loggued_user.password:
                    login_user(loggued_user)
                    return redirect(url_for('home'))
                else:
                    flash("Contraseña invalida")
                    return render_template('auth/login.html')
            else:
                flash("Centro invalido")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado!")
            return render_template('auth/login.html')
    else:
        if ModelVeterinaria.get_centro() == None:
            return redirect(url_for('loginV'))
        else:
            return render_template('auth/login.html')


@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('loginV'))


@app.route('/admin')
@login_required
def admin():
    if current_user.rol == '1':
        centro = ModelVeterinaria.get_centro()
        encontradas = ModelUser.get_users(db, centro)
        return render_template('admin.html', encontradas=encontradas)
    else:
        flash('No tienes permisos para acceder a esta seccion.')
        return redirect(url_for('home'))

@app.route('/busquedaCliente' , methods=['GET','POST'])
@login_required
def busquedaCliente():
    if request.method == 'POST':
        try:
            id = request.form['idBusqueda']
            encontradas = ModelCliente.get_users_by_id(db, id, current_user.veterinaria)
            return render_template('busquedaCliente.html', encontradas=encontradas)
        except:
            flash('No encontramos ningun cliente')
            return redirect(url_for('home'))
    return render_template('busquedaCliente.html')

@app.route('/busqueda', methods=['GET', 'POST'])
@login_required
def busqueda():
    if request.method == 'POST':
        parametro = request.form['busqueda']
        if current_user.rol == '1':
            centro = ModelVeterinaria.get_centro()
            encontradas = ModelUser.get_users_by_id(db, parametro, centro)
            print(encontradas)
            return render_template('busqueda.html', encontradas=encontradas)
    elif current_user.rol != '1':
        flash('No tienes permisos para acceder a esta sesion')
        return redirect(url_for('home'))
    return render_template('busqueda.html')


@app.route('/loginV', methods=['GET', 'POST'])
def loginV():
    if request.method == 'POST':
        veterinaria = Veterinaria(
            request.form['username'], "0", "0", "0", "0", "0", "0")
        loggued_vet = ModelVeterinaria.loginV(db, veterinaria)
        if loggued_vet != None:
            centro = loggued_vet.nombre_vet
            ModelVeterinaria.set_centro(centro)
            return render_template('auth/login.html', centro=centro)
        else:
            flash("Veterinaria no registrada")
            redirect(url_for('loginV'))
    return render_template('auth/login_vet.html')


@app.route('/regUser', methods=['GET', 'POST'])
@login_required
def regUser():
    if current_user.rol == '1':
        if request.method == 'POST':
            EmpleadoNuevo = User(request.form['id'], request.form['username'], request.form['password'], request.form['fullname'],
                                request.form['rol'], current_user.veterinaria, request.form['direccion'], request.form['email'], request.form['telefono'])
            obtenerUsuario = ModelUser.get_by_id(db, EmpleadoNuevo.id)
            print(obtenerUsuario)
            if not obtenerUsuario:
                ModelUser.register(db, EmpleadoNuevo)
                print(EmpleadoNuevo.rol)
                flash("Empleado registrado")
                return render_template('reg/regUser2.html')
            else:
                flash('Ya existe un usuario con el mismo numero de id')
                return render_template('reg/regUser2.html')
        else:
            return render_template('reg/regUser2.html')
    else:
        flash('No tienes permisos para acceder a esta seccion.')
        return redirect(url_for('home'))



@app.route('/regCliente', methods=['GET', 'POST'])
@login_required
def regCliente():
    if request.method == 'POST':
        try:
            cliente = Cliente(request.form['documento'],request.form['fullname'],request.form['telefono'],request.form['direccion'],request.form['email'],current_user.veterinaria)
            ModelCliente.register(db,cliente)
            flash("Cliente creado con exito")
            return render_template('reg/regCliente.html')
        except:
            flash("El cliente ya existe")
            return render_template('reg/regCliente.html')
    else:
        return render_template('reg/regCliente.html')


@app.route('/soporte', methods=['GET', 'POST'])
def soporte():
    return render_template('soporte.html')


@app.route('/prueba')
def prueba():
    return render_template('home.html')

# Usuarioprueba = User(0,"Maria","Ma240404","Maria Rodriguez","1","Canes")
# ModelUser.register(db,Usuarioprueba)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
