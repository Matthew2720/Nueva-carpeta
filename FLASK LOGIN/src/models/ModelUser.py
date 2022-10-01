from .entities.User import User, Veterinaria
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
                user = User(row[0],row[1],User.check_password(row[2],user.password),row[3],row[4],row[5])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.cursor()
            consulta = "SELECT id, username, password, fullname,rol,FNOMBREVET FROM USUARIOS where id = {}".format(id)
            cursor.execute(consulta)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],row[2],row[3],row[4],row[5])
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
            consulta = "INSERT into USUARIOS (username,password,fullname,rol,fnombrevet) VALUES ('{}','{}','{}','{}','{}')".format(user.username,contrasena,user.fullname,user.rol,user.veterinaria)
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
        
class ModelVeterinaria():
    centro = None
    @classmethod
    def registrar_vet(self,db,veterinaria):
        cursor = db.cursor()
        consulta = "INSERT INTO CENTRO(NOMBRE_VET,CIUDAD_VET,NOMBRE,APELLIDO,DOCUMENTO,TEL_CENTRO,EMAIL_CENTRO) VALUES (?,?,?,?,?,?,?);"
        cursor.execute(consulta,veterinaria.nombre_vet,veterinaria.ciudad_vet,veterinaria.nombre,veterinaria.apellido,veterinaria.documento,veterinaria.telefono,veterinaria.email)
        cursor.commit()
        cursor.close()
        
    @classmethod
    def loginV(self,db,veterinaria):
        try:
            cursor = db.cursor()
            consulta = "SELECT * FROM CENTRO where nombre_vet = '{}'".format(veterinaria.nombre_vet)
            cursor.execute(consulta)
            row = cursor.fetchone()
            if row != None:
                veterinaria = Veterinaria(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                return veterinaria
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def set_centro(self,centro):
        self.centro = centro
    
    @classmethod
    def get_centro(self):
        return self.centro
            
        
        