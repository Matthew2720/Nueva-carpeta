from flask import Flask,render_template,url_for,request,redirect,flash,session
from config import *
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
import pyodbc

#Modelos y entidades

from models.entities.User import User
from models.ModelUser import ModelUser

app = Flask(__name__)
db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['password'])
        loggued_user = ModelUser.login(db,user)
        if loggued_user != None:
            if loggued_user.password:
                login_user(loggued_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña invalida")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado!")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>",404

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    if current_user.rol == '1':
        return render_template('admin.html')
    elif current_user.rol == '2':
        return redirect(url_for('logout'))
    
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()