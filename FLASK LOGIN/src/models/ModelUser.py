from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.cursor()
            consulta = "SELECT * FROM USUARIOS where USERNAME = '{}'".format(user.username)
            cursor.execute(consulta)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],User.check_password(row[2],user.password),row[3],row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.cursor()
            consulta = "SELECT id, username, password, fullname,rol FROM USUARIOS where id = {}".format(id)
            cursor.execute(consulta)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],row[2],row[3],row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def register(self,db,user):
        try:
            cursor = db.cursor()
            contrasena = generate_password_hash(user.password)
            consulta = "INSERT into USUARIOS (username,password,fullname,rol) VALUES ('{}','{}','{}','{}')".format(user.username,contrasena,user.fullname,user.rol)
            cursor.execute(consulta)
            cursor.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_users(self,db):
        try:
            cursor = db.cursor()
            consulta = "SELECT * FROM USUARIOS"
            cursor.execute(consulta)
            encontradas = cursor.fetchall()
            cursor.close()
            return encontradas
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_users_by_id(self,db,parametro):
        try:
            cursor = db.cursor()
            consulta = "SELECT * FROM USUARIOS where id = {}".format(parametro)
            cursor.execute(consulta)
            encontradas = cursor.fetchall()
            cursor.close()
            return encontradas
        except Exception as ex:
            raise Exception(ex)
        
        