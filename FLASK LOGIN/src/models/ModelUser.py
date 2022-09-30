from .entities.User import User

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
            consulta = "INSERT into USUARIOS (username,password,fullname,rol) VALUES ('{}','{}','{}','{}')".format(user.username,user.password,user.fullname,user.rol)
            cursor.execute(consulta)
            cursor.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
        